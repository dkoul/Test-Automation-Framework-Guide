import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import random
import string

# Function to generate a random user ID
def random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Session state to store user info
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = random_id()

st.title("Anonymous Chat App")
st.write("Chat with strangers anonymously!")

# Placeholder for WebRTC chat
st.write("### Live Chat Room")
webrtc_streamer(key="chat", mode=WebRtcMode.SENDRECV)
st.write("You are chatting as: `" + st.session_state['user_id'] + "`")

st.info("Simply refresh the page to get a new chat partner!")
