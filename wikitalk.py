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
llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
    temperature=0.0,
    menu_items=None,
)
Settings.llm = llm

# define wikipedia titles
wiki_titles = []

# fetch wikipedia articles and build indices
get_wikipeida_articles(wiki_titles)

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
    You are an agent designed to answer queries about the European top football leagues.
    Please always use the tools provided to answer a question. Do not rely on prior knowledge.""",
    verbose=True,
)


# streamlit app
#st.title("WikiTalk")
#st.sidebar.image("path/logo.png", use_container_width=True)



# sidebar
st.sidebar.title("WikiTalk")
search_term = st.sidebar.text_input("Search Wikipedia", "")
if st.sidebar.button("Chat"):
    st.subheader("Chat with WikiTalk")
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
            with st.spinner("Thinking..."):
                response = top_agent.query(prompt)
                st.write_stream(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    




if st.sidebar.button("Your Knowledge Base"):
    st.subheader("Your Knowledge Base")
    for wiki_title in wiki_titles:
        st.write(f"### {wiki_title}")
        st.text(leagues_docs[wiki_title])


# hide streamlit menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

