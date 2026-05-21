import streamlit as st
import os
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

# ======================
# ENV LOAD
# ======================
load_dotenv()

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="Finance Literacy Assistant", page_icon="💰")

# ======================
# SESSION STATE
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# LOAD KB + EMBEDDINGS (NO FAISS)
# ======================
@st.cache_resource(show_spinner="Loading Knowledge Base...")
def load_knowledge_base():
    from sentence_transformers import SentenceTransformer

    kb_path = Path(__file__).parent / "finance_kb.txt"

    if not kb_path.exists():
        st.error("KB file missing: finance_kb.txt")
        st.stop()

    text = kb_path.read_text(encoding="utf-8")

    # chunking
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = embedder.encode(chunks)
    embeddings = np.array(embeddings)

    return chunks, embeddings, embedder


# ======================
# RETRIEVAL (COSINE SIMILARITY)
# ======================
def retrieve_context(query, chunks, embeddings=None, embedder=None):
    # SIMPLE TEXT MATCH (NO ML)
    query = query.lower()

    scored = []
    for c in chunks:
        score = sum(1 for w in query.split() if w in c.lower())
        scored.append((score, c))

    scored.sort(reverse=True, key=lambda x: x[0])

    top = [c for _, c in scored[:3]]
    return "\n\n".join(top)


# ======================
# GROQ RESPONSE
# ======================
def get_groq_response(user_message, context, chat_history):
    from groq import Groq

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            return "❌ GROQ API key missing. Add it in .env or Streamlit secrets."

    client = Groq(api_key=api_key)

    system_prompt = f"""
You are a Finance AI Assistant.

ROLE:
Help users with budgeting, saving, investing basics, and financial literacy.

RULES:
- Simple language
- Real-life examples
- Short answers
- If unknown, say you don't know

CONTEXT:
{context}
"""

    messages = [{"role": "system", "content": system_prompt}]

    for m in chat_history[-6:]:
        messages.append(m)

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=600,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ API Error: {str(e)}"


# ======================
# UI
# ======================
st.title("💰 Finance Literacy AI Assistant")

chunks, embeddings, embedder = load_knowledge_base()

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input
prompt = st.chat_input("Ask anything about personal finance...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    context = retrieve_context(prompt, chunks, embeddings, embedder)

    response = get_groq_response(prompt, context, st.session_state.messages)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

# import streamlit as st

# st.title("Finance Bot")
# st.write("App is running successfully 🚀")

# user_input = st.text_input("Ask something")

# if user_input:
#     st.write("You said:", user_input)