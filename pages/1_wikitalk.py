import os
import openai
import streamlit as st
from pathlib import Path
import requests

from llama_index.core import(
    VectorStoreIndex,
    SummaryIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai_legacy import FnRetrieverOpenAIAgent
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.objects import ObjectIndex, SimpleToolNodeMapping
from dotenv import load_dotenv
from wiki_fetcher import get_wikipeida_articles
from vector_agent_builder import build_indices, create_tools


load_dotenv()

st.set_page_config(
    page_title="WikiTalk",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("💬 Chat with WikiTalk")
st.markdown("---")

llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
    temperature=0.0,
    menu_items=None,
)
Settings.llm = llm

# initialize wiki_titles
if "wiki_titles" not in st.session_state:
    st.session_state.wiki_state = {
        "wiki_titles": [file_name[:-4] for file_name in os.listdir("data") if file_name.endswith(".txt")],
    }
# access and modify wiki_titles
wiki_titles = st.session_state.wiki_state["wiki_titles"]
st.sidebar.title("Current knowledge base")
st.sidebar.markdown("\n".join(f"- {title}" for title in wiki_titles))


leagues_docs = {}
node_parser = SentenceSplitter()

# load data for each wiki title
for wiki_title in wiki_titles:
    leagues_docs[wiki_title] = SimpleDirectoryReader(
        input_files=[f"data/{wiki_title}.txt"]
    ).load_data()

# build agents, query engines, and indices
agents = {}
query_engines = {}
all_nodes = []
build_indices(wiki_titles, node_parser, agents, query_engines)

# create tools
all_tools = create_tools(wiki_titles, agents)

# define an "object" index and retriever over these tools
tool_mapping = SimpleToolNodeMapping.from_objects(all_tools)
obj_index = ObjectIndex.from_objects(
    all_tools,
    tool_mapping,
    VectorStoreIndex,
)

# define an agent that uses the object index
top_agent = FnRetrieverOpenAIAgent.from_retriever(
    obj_index.as_retriever(similarity_top_k=3),
    system_prompt="""\
    You are an agent designed to answer queries about any detailed knowledge on wikipedia.
    Please always use the tools provided to answer a question. Do not rely on prior knowledge.
    If you cannot find relevant information about the user's question in the context of data, please give back the answer based on prior knowledge.""",
    verbose=True,
)


# streamlit app
#st.title("WikiTalk")
#st.sidebar.image("path/logo.png", use_container_width=True)



# sidebar
# st.sidebar.title("WikiTalk")
# selected_page = st.sidebar.radio("Select Page", ["Chat", "Your Knowledge Base"])
#search_term = st.sidebar.text_input("Search Wikipedia", "")

# set a default model
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"

# initialize chat history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to WikiTalk! Ask me anything you want to learn!"}
    ]

# display chat messages from history on app run
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# accept user input
if prompt := st.chat_input("What's your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking...it may take 1-2 minutes to extract accurate data from wikipedia."):
            response = top_agent.query(prompt)
            response_text = str(response)
            st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})






# hide streamlit menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

