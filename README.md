# Finance Literacy AI Chatbot

RAG-powered AI chatbot focused on personal finance literacy, budgeting, and investment basics.

## Project Structure

```
finance-bot/
├── index.html             <- Demo website with integrated chatbot
├── app.py                 <- AI chatbot (Streamlit + Groq RAG)
├── finance_kb.txt         <- Chatbot knowledge base
├── requirements.txt       <- Python dependencies
└── .streamlit/
    └── secrets.toml       <- API key storage
```

## Deploy the AI Chatbot

1. Go to https://streamlit.io/cloud and sign in with GitHub
2. Click New app, select this repo, set Main file path to app.py
3. Under Advanced settings > Secrets, paste:
   GROQ_API_KEY = "your_key_here"
4. Get a free Groq API key at https://console.groq.com
5. Click Deploy

## Connect Chatbot to Website

After deploying, open index.html and update the CHATBOT URL with your real Streamlit Cloud URL.

## Run Locally

```powershell
pip install -r requirements.txt
streamlit run app.py
```
