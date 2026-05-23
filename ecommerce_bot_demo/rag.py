from openai import OpenAI

client = OpenAI()

def load_kb():
    with open("kb.txt", "r") as f:
        return f.read().split("\n")

def search(query, texts):
    query_words = query.lower().split()

    best_match = None
    best_score = 0

    for t in texts:
        score = sum(1 for w in query_words if w in t.lower())

        if score > best_score:
            best_score = score
            best_match = t

    return best_match if best_match else "I don't know"

def ask(query, texts):
    context = search(query, texts)

    prompt = f"""
Use ONLY this context:
{context}

Question: {query}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content