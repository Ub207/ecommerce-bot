import streamlit as st
from rag import load_kb, build_index, ask

st.title("AI E-Commerce Chatbot")

texts = load_kb()
index, texts = build_index(texts)

query = st.text_input("Ask something about our store")

if query:
    answer = ask(query, index, texts)
    st.write(answer)
