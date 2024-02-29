import os
import streamlit as st
import shutil
from wiki_fetcher import get_wikipeida_articles

st.set_page_config(
    page_title="Your Knowledge Base",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)


# initialize wiki_titles
if "wiki_titles" not in st.session_state:
    st.session_state.wiki_state = {
        "wiki_titles": [file_name[:-4] for file_name in os.listdir("data") if file_name.endswith(".txt")],
    }
# Access and modify wiki_titles
wiki_titles = st.session_state.wiki_state["wiki_titles"]
st.sidebar.title("Current knowledge base")
st.sidebar.markdown("\n".join(f"- {title}" for title in wiki_titles))


# Function to add a new entry to wiki_titles
def add_to_wiki_titles(entry):
    wiki_titles.append(entry)
    st.session_state.wiki_state["wiki_titles"] = wiki_titles

# Function to delete a file and its corresponding name from wiki_titles
def delete_file(file_name):
    if file_name in wiki_titles:
        wiki_titles.remove(file_name)
    file_path = f"data/{file_name}"
    if os.path.exists(file_path):
        os.remove(file_path)
    directory_path = f"data/{file_name[:-4]}"
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


# Function to display the content of a file
def display_file_content(file_name):
    file_path = f"data/{file_name}"
    
    # Use st.expander to create a collapsible section
    # with st.expander(f"Read {file_name}"):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    st.markdown(content)

# Streamlit app
st.title("📚 Knowledge Base")
st.caption("📚 This is your knowledge base data." )

st.markdown("---")

st.subheader("❓ How to use this knowledge base?")
st.markdown('''
    🚀 You can check all of the information by clicking read.
            
    🚀 If you want to add new data to your knowledge base, type the name of the data and click add.
            
    🚀 If you want to delete any of the data, click delete.
    '''
)

st.markdown("---")

st.subheader("🔍 Search Bar")
search_term = st.text_input("Search Wikipedia", "")
if st.button("Add"):
    add_to_wiki_titles(search_term)
    get_wikipeida_articles([search_term])

st.markdown("---")

# Display all .txt files and provide options to read and delete
st.subheader("🔀 Repository")
for file_name in os.listdir("data"):
    if file_name.endswith(".txt"):
        with st.expander(f"##### {file_name}"):
            # Use st.beta_columns to create two columns
            col1, col2 = st.columns(2)
            
            # Button in the first column
            if col1.button(f"Read {file_name}"):
                display_file_content(file_name)
            
            # Button in the second column
            if col2.button(f"Delete {file_name}"):
                delete_file(file_name)