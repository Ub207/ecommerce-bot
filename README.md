# 🛒 AI E-Commerce Chatbot

A RAG-powered AI chatbot for e-commerce stores — answers customer questions about products, shipping, returns, and more using a custom knowledge base and the Groq LLM API.

## ✨ Features

- 🔍 **RAG (Retrieval-Augmented Generation)** — finds the most relevant info from your knowledge base before answering
- ⚡ **Groq LLM** — fast inference using `llama-3.3-70b-versatile`
- 🧠 **Local embeddings** — uses `sentence-transformers` + `faiss` for semantic search (no OpenAI needed)
- 🌐 **Streamlit UI** — clean, simple chat interface

## 📁 Project Structure

```
ecommerce-bot/
├── app.py                 ← Streamlit UI
├── rag.py                 ← RAG pipeline (embeddings, FAISS index, Groq LLM)
├── ecommerce_kb.txt       ← Knowledge base (edit this with your store's info)
├── requirements.txt       ← Python dependencies
└── .streamlit/
    └── secrets.toml       ← API key storage (never commit this!)
```

## 🚀 Deploy to Streamlit Cloud (Free)

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select this repo → set main file to `app.py`
4. Under **Settings → Secrets**, paste:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Get a free Groq API key at [console.groq.com](https://console.groq.com)
6. Click **Deploy** 🎉

## 🖥️ Run Locally

```powershell
# Clone the repo
git clone https://github.com/Ub207/ecommerce-bot.git
cd ecommerce-bot

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
# Create .streamlit/secrets.toml and add:
# GROQ_API_KEY = "your_key_here"

# Run the app
streamlit run app.py
```

## 📝 Customize the Knowledge Base

Edit `ecommerce_kb.txt` — add one fact per line about your store:

```
We sell shoes, shirts, and accessories.
Return policy is 7 days with original receipt.
Shipping takes 3-5 business days.
We are located in Karachi, Pakistan.
Free shipping on orders above Rs. 3000.
```

The chatbot will only answer based on what's in this file.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| LLM | Groq (`llama-3.3-70b-versatile`) |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Vector Search | FAISS |
| Language | Python 3.10+ |
