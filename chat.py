import streamlit as st
import random
import string

# Function to generate a random user ID
def random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Session state to store user info
if 'username' not in st.session_state:
    st.session_state['username'] = ""

st.title("Anonymous Text Chat App")
st.write("Chat with strangers anonymously!")

# Ask user for a name
st.session_state['username'] = st.text_input("Enter your name:", st.session_state['username'])

# Chat message storage
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display chat messages
st.write("### Chat Room")
chat_box = st.empty()
chat_box.markdown("\n".join(st.session_state['messages']))

# Input field for new messages
new_message = st.text_input("Type a message:")
if st.button("Send") and new_message:
    st.session_state['messages'].append(f"{st.session_state['username']}: {new_message}")
    chat_box.markdown("\n".join(st.session_state['messages']))

st.info("Simply refresh the page to clear the chat!")
