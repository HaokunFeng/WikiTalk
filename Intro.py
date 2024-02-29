import streamlit as st

st.set_page_config(
    page_title="Intro_WikiTalk",
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
st.sidebar.markdown("This is a rag app, and also an interactive chatbot with knowledge base function that combined wikipedia with GPT.")

st.title("🚩 WikiTalk")
home_title = "welcome to WikiTalk!📣"
st.caption("This is a rag app, and also an interactive chatbot with knowledge base function that combined wikipedia with GPT.")
home_introduction = "Welcome to WikiTalk, where the power of OpenAI's GPT technology is at your fingertips. Socialize with pre-trained AI Assistants in the Lounge or create your own custom AI companions in the Lab. Whether you need a personal helper, writing partner, or more, GPT Lab has you covered. Join now and start exploring the endless possibilities!"
home_privacy = "At GPT Lab, your privacy is our top priority. To protect your personal information, our system only uses the hashed value of your OpenAI API Key, ensuring complete privacy and anonymity. Your API key is only used to access AI functionality during each visit, and is not stored beyond that time. This means you can use GPT Lab with peace of mind, knowing that your data is always safe and secure."

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

#st.title(home_title)
st.markdown(f"""#### {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)

st.markdown("""\n""")
st.markdown("#### Greetings")
st.write(home_introduction)

st.markdown("---")

st.markdown("#### Privacy")
st.write(home_privacy)

st.markdown("""\n""")
st.markdown("""\n""")

st.markdown("---")

st.markdown("#### Get Started")