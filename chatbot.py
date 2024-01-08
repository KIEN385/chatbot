import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key="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")

# Function to interact with the GPT-3.5-turbo model with tunable parameters
def generate_response(prompt, temperature=0.7, max_tokens=256, top_p=0.9, n=2, stop=None, frequency_penalty=0.9, presence_penalty=0.9, chat_history=None):
    if chat_history is None:
        chat_history = []

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    messages.extend(chat_history)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        n=n,
        stop=stop,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return response.choices[0].message.content

# Streamlit app header and title
 # tattooed geek logo
logo1 = 'https://miro.medium.com/v2/resize:fit:180/1*ypRBA86IBBbZbti76vm4Hg.png'
# Streamlit app header and title
st.set_page_config(page_title="ChatGPT Chatbot", page_icon=logo1 , layout="wide")


st.write("# Chatbot with GPT-3.5-turbo")
st.write("Welcome ! Type your message below:")

# HTML sidebar to fine-tune model's parameters to customize the bot's responses.
st.sidebar.markdown("# Model Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.number_input("Max Tokens", 50, 500, 256, step=50)
top_p = st.sidebar.slider("Top P", 0.1, 1.0, 0.9, 0.1)
n = st.sidebar.number_input("N", 1, 5, 2, step=1)
stop = st.sidebar.text_input("Stop", "")
frequency_penalty = st.sidebar.slider("Frequency Penalty", 0.0, 1.0, 0.9, 0.1)
presence_penalty = st.sidebar.slider("Presence Penalty", 0.0, 1.0, 0.9, 0.1)

# Main app where user enters prompt and gets the response
user_input = st.text_area("You:", "", key="user_input")
generate_button = st.button("Generate Response")


# Chat history
messages = []
if user_input.strip() != "":
    messages.append({"role": "user", "content": user_input})
    response = generate_response(user_input, temperature, max_tokens, top_p, n, stop, frequency_penalty, presence_penalty)
    messages.append({"role": "assistant", "content": response})

st.subheader("Chat History")
for message in messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=50, max_chars=200, key="user_history", disabled=True)
    else:
        st.text_area("Reply:", value=message["content"], height=500, key="chatbot_history")

# Additional styling to make the app visually appealing
st.markdown(
    """
    <style>
        body {
            font-family: Montserrat, sans-serif;
        }
        .stTextInput>div>div>textarea {
            background-color: #f0f0f0;
            color: #000;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stTextArea>div>textarea {
            resize: none;
        }
        .st-subheader {
            margin-top: 20px;
            font-size: 16px;
        }
        .stTextArea>div>div>textarea {
            height: 100px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)