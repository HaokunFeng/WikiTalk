from tempfile import NamedTemporaryFile
import os

import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv
#from openai import OpenAI

load_dotenv()

st.set_page_config(
    page_title="Chat with File",
    page_icon="📂",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("📂 Chat with File")
st.caption("Upload a PDF file first and ask questions about the file.")
st.markdown("---")

# set api key and model
llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    #base_url=os.getenv("OPENAI_API_BASE"),
    model="gpt-3.5-turbo",
    temperature=0.0,
    system_prompt="You are an excellent writer on the content of resume, provide detailed advice and feedback to optimize the resume. Use the uploaded document to support your answers.",
)

# set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# initialize chat history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about your resume!"}
    ]


# display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



uploaded_file = st.file_uploader("Upload your resume in PDF version")
if uploaded_file:
    bytes_data = uploaded_file.read()
    #to do: 1.the assistant can give me response based on the PDF uploaded by a user; 2. use system_prompt to optimize the assistant response answer
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(bytes_data)
        with st.spinner(text="Loading and indexing the streamlit docs. This should take 1-2 minutes."):
            reader = PDFReader()
            docs = reader.load_data(tmp.name)
            index = VectorStoreIndex.from_documents(docs)
    os.remove(tmp.name)

    if "chat_engine" not in st.session_state.keys():
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=False, llm=llm
        )


# accept user input
if prompt := st.chat_input("What's your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response.response_gen)
            message = {"role": "assistant", "content": response.response}
    st.session_state.messages.append({"role": "assistant", "content": response})