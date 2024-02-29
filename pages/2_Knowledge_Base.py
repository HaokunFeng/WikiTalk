import streamlit as st

st.subheader("Your Knowledge Base")
for wiki_title in wiki_titles:
    st.write(f"### {wiki_title}")
    st.text(leagues_docs[wiki_title])