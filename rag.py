import faiss
import numpy as np
from groq import Groq
import streamlit as st
from sentence_transformers import SentenceTransformer

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize SentenceTransformer model (local embeddings)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load KB
def load_kb():
    try:
        with open("ecommerce_kb.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return ["No knowledge base found."]

# Create embeddings
def embed(texts):
    return embed_model.encode(texts)

# Build vector DB
def build_index(texts):
    vectors = embed(texts)
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype("float32"))
    return index, texts

# Search
def search(query, index, texts):
    q_vec = embed([query])
    D, I = index.search(np.array(q_vec).astype("float32"), k=1)
    return texts[I[0][0]]

# Generate answer
def ask(query, index, texts):
    context = search(query, index, texts)

    prompt = f"""
    Answer ONLY from this context:
    {context}

    Question: {query}
    """

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
