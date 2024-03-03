# 🚩 WikiTalk

Build your own knowledge base and get accurate information using WikiTalk!

## App Overview 🔍

Welcome to WikiTalk, where the power of OpenAI's GPT technology is at your fingertips. With WikiTalk, you can ask questions and get accurate information based on Wikipedia. 

As we know, chatGPT sometimes give wrong answers based on users' questions, because GPT-3.5's last knowledge update is in January 2022, which means it can't provide real-time information.

Our system uses the power of GPT-3.5-Turbo and real_time Wikipedia to provide you with the most accurate and up-to-date information available. Whether you're looking for information on a specific topic, or just want to learn something new, WikiTalk is here to help. So go ahead, ask us anything!

## Demo App 👏
[**WikiTalk**](https://github.com/HaokunFeng/wikitalk.git)

## Features of the App 🎯
- **WikiTalk**:  You can ask questions and get accurate information based on Wikipedia here. Before using this function, you need to add the related data using 'Knowledge Base' function, otherwise you will get the feedback from chatGPT-3.5 directly that might be wrong. And it might take 1-2minutes to get the feedback because it will search all the relevant information in your knowledge base.
- **Knowledge Base**:  Here you can add the related data to the knowledge base to build your own library. Using search, add, read and delete to modify your library.
- **File Chat**:  You can upload a PDF file here and ask questions about the file.
- **GPT Clone**: You can chat with the chatGPT-3.5 directly here. This chatbot does not use the knowledge base data, so it might be wrong.


## Get Started 🥳
To use this program in your local environment, follow these simple steps:

- Clone this repository.
- ``python -m venv vent``
- ``.\venv\Scripts\Activate`` (Or use a proper command based on your OS to activate the environment)
- ``pip install -r requirements.txt``
- Replace the .env.apikey with your own OpenAI API Key
- ``cp .env.apikey .env``
- Change the ``.env`` file to match your environment
- ``streamlit run intro.py`` to run the WikiTalk App


## Get an OpenAI API key 🅰️

You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.


# Technologies Usesd 🤖
Llama-Index, Streamlit, OpenAI API, WikiPedia API


## Privacy 📂

At WikiTalk, your privacy is our top priority. To protect your personal information, our system only uses your questions and files data when searching and querying, and will not save the data, ensuring complete privacy and anonymity. This means you can use WikiTalk with peace of mind, knowing that your data is always safe and secure.