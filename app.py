# this project is a simpliciation of this project: https://github.com/romilandc/streamlit-ollama-llm and woudnt be possible with out that starter
# main difference is its not using torch, which gives the option of selecting between using the gpu or cpu in the example from romilandc
# all credits goes to: https://github.com/romilandc/streamlit-ollama-llm

import streamlit as st
import ollama

st.title("Ollama Python Chatbot")

modelSessionKey = "model"
messagesSessionKey = "messages"

if messagesSessionKey not in st.session_state:
    st.session_state[messagesSessionKey] = []

# ------------------------
# ------------------------
# OBS OBS OBS OBS OBS
# you need to download and install ollama from https://ollama.com/
# download desired models from the models browser https://ollama.com/search
# install them via the terminal 
# on windodes: open powershell or cmd
# write ollama pull llama2
# then it downloads the model, and then you can use whatever models you downloaded this way in the streamlit app
# ------------------------
# ------------------------

# get a list of the models installed on your drive
allLocalModels = [model.model for model in ollama.list().models]


# init models in session state
if modelSessionKey not in st.session_state:
    st.session_state[modelSessionKey] = ""

# select a model
st.session_state[modelSessionKey] = st.selectbox("Select a model from your local drive", allLocalModels)

# function to chat with the ollama model
# everytime the user is submitting a promt, we provide the full msg history in the st.session_state["messages"], so the LLM knows the full history of the current chat, so it can use context from the preivous chats messages
def ask_llm_model():

    # Use ollama's API to generate responses for each message in the session state
    # the reason the entire message history is provided and not just the latest is due to give the LLM the full context of the users chat. Then the model can figoure out where you left of from your last msg
    stream = ollama.chat(
        model=st.session_state[modelSessionKey],
        messages=st.session_state[messagesSessionKey],
        stream=True,
    )
    
    # this is the models response, yield is writing word by word on the screen as the models is ready to show it 
    for word in stream:
        yield word["message"]["content"]

# show the entire chat history
for message in st.session_state[messagesSessionKey]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# when a promt is sent this is triggered
userChatPromt = st.chat_input("Ask ma dude")

if userChatPromt: 
    # role: user will give a icon with a person in the chat history
    st.session_state[messagesSessionKey].append({"role": "user", "content": userChatPromt})

    # the user promt msg is written here: 
    with st.chat_message("user"):
        st.markdown(userChatPromt)

    # the llm/ai response
    with st.chat_message("assistant"):
        message = st.write_stream(ask_llm_model())
        # role assistent will give a icon of a robot in the chat history
        st.session_state["messages"].append({"role": "assistant", "content": message})
