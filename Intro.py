import streamlit as st

st.set_page_config(
    page_title="WikiTalk",
    page_icon="🚩",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
logo_path = "gui/logo3.png"
st.sidebar.image(logo_path, use_column_width=True)
# st.sidebar.title("WikiTalk")
st.sidebar.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0px;'>WikiTalk</h1>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("🚩 This an interactive chatbot with a knowledge base function that can give you accurate information about your questions based on wikepedia.")
st.sidebar.markdown("📑 And you can use the knowledge base function to build your own library!")
st.sidebar.markdown("---")
st.sidebar.markdown("😼 WikiTalk is a project by [@Haokun Feng](https://github.com/HaokunFeng).")
st.sidebar.markdown("👉 [View the source code](https://github.com/HaokunFeng/wikitalk.git)")

#st.title("🚩 WikiTalk")
home_title = "🚩 WikiTalk!"
st.title(home_title)
st.caption("Get accurate information about your questions based on wikepedia!")
home_introduction = "Welcome to WikiTalk, where the power of OpenAI's GPT technology is at your fingertips. With WikiTalk, you can ask questions and get accurate information based on Wikipedia. Our system uses the power of GPT-3.5-Turbo and real_time Wikipedia to provide you with the most accurate and up-to-date information available. Whether you're looking for information on a specific topic, or just want to learn something new, WikiTalk is here to help. So go ahead, ask us anything!"
home_privacy = "At WikiTalk, your privacy is our top priority. To protect your personal information, our system only uses your questions and files data when searching and querying, and will not save the data, ensuring complete privacy and anonymity. This means you can use WikiTalk with peace of mind, knowing that your data is always safe and secure."


st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

#st.markdown(f"""#### {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)
st.markdown("#### Greetings 👋")
st.write(home_introduction)

st.markdown("---")
st.markdown("####  Features 🎯")
st.markdown("- **WikiTalk**: You can ask questions and get accurate information based on Wikipedia here. "
            "Before using this function, you need to add the related data using 'Knowledge Base' function, "
            "otherwise you will get the feedback from chatGPT-3.5 directly that might be wrong. And it might "
            "take 1-2minutes to get the feedback because it will search all the relevant information in your knowledge base.")
st.markdown("- **Knowledge Base**: Here you can add the related data to the knowledge base to build your own library. "
            "Using search, add, read and delete to modify your library.")
st.markdown("- **File Chat**: You can upload a PDF file here and ask questions about the file. ")
st.markdown("- **GPT Clone**: You can chat with the chatGPT-3.5 directly here. "
            "This chatbot does not use the knowledge base data, so it might be wrong.")

st.markdown("""\n""")
st.markdown("""\n""")
st.markdown("---")
st.markdown("#### Get Started 🥳")
st.markdown("To use WikiTalk, follow these simple steps:")
st.markdown("1. **Add Data**: Go to the 'Knowledge Base' function and use 'Search Bar' to add the related articles from Wikipedia to build your own library."
            "If adding data is successful, you can find the file name in the sidebar and in the 'Repository'.")
st.markdown("2. **Check Data**: In the 'Knowledge Base' function, you can read the .txt file in 'Repository' to check the data you added."
            "If you found the Read .txt is blank, it means you didn't add the data successfully."
            "Notice that you need to add the exact title of the article in Wikipedia to get the data, otherwise it failed to add data.")
st.markdown("3. **Ask Questions**: Go to the 'WikiTalk' function and ask questions about the data you added. ")
st.markdown("4. **File Chat and GPT Clone**: You can use GPT Clone directly, but you need to upload the file first to use the File Chat function.")

st.markdown("""\n""")
st.markdown("""\n""")
st.markdown("---")
st.markdown("#### Privacy 📂")
st.write(home_privacy)