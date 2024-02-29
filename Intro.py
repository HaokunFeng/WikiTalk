import streamlit as st


# st.title("Welcome to WikiTalk")
# st.write("This is an interactive chatbot and knowledge base application.")




st.set_page_config(
    page_title="GPT Lab",
    page_icon="https://api.dicebear.com/5.x/bottts-neutral/svg?seed=gptLAb"#,
    #menu_items={"About": "GPT Lab is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT-3 language model. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.", "Get help": None, "Report a Bug": None}
)



# copies 
home_title = "GPT Lab"
home_introduction = "Welcome to GPT Lab, where the power of OpenAI's GPT technology is at your fingertips. Socialize with pre-trained AI Assistants in the Lounge or create your own custom AI companions in the Lab. Whether you need a personal helper, writing partner, or more, GPT Lab has you covered. Join now and start exploring the endless possibilities!"
home_privacy = "At GPT Lab, your privacy is our top priority. To protect your personal information, our system only uses the hashed value of your OpenAI API Key, ensuring complete privacy and anonymity. Your API key is only used to access AI functionality during each visit, and is not stored beyond that time. This means you can use GPT Lab with peace of mind, knowing that your data is always safe and secure."

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

#st.title(home_title)
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)

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