# 

import streamlit as st
from agent import ask_ai

st.title("Finance AI Bot 💰")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask a finance question:")

if user_input:
    reply = ask_ai(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("Bot", reply))

for role, msg in st.session_state.chat:
    st.write(f"**{role}:** {msg}")