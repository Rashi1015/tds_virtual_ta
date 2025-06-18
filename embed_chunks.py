import os
import json
import sqlite3
import re
import httpx
import hashlib
import requests
from dotenv import load_dotenv

import google.generativeai as genai


load_dotenv()


# ========== 1. Cleaning & Chunking ==========

def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'>.*?\n', '', text)
    return text.strip()

def chunk_text(text, max_tokens=300):
    words = text.split()
    return [" ".join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]

# ========== 2. Extractors ==========

def extract_from_threads(folder="downloaded_threads"):
    chunks = []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file), encoding="utf-8") as f:
                data = json.load(f)
                title = data.get("title", "Untitled")
                posts = data.get("post_stream", {}).get("posts", [])
                full_text = f"### {title} ###\n\n"
                for post in posts:
                    user = post.get("username", "user")
                    cooked = clean_text(post.get("cooked", ""))
                    full_text += f"{user}:\n{cooked}\n\n"
                chunks.extend([(chunk, f"Discourse: {title}") for chunk in chunk_text(full_text)])
    return chunks

def extract_from_markdown(folder="tds_content"):
    chunks = []
    for file in os.listdir(folder):
        if file.endswith(".md"):
            with open(os.path.join(folder, file), encoding="utf-8") as f:
                raw = f.read()
                cleaned = clean_text(raw)
                chunks.extend([(chunk, f"CourseContent: {file}") for chunk in chunk_text(cleaned)])
    return chunks

# ========== 3. Generate Embeddings via HuggingFace Inference API ==========

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str):
    model = genai.GenerativeModel("gemini-embedding-exp-03-07")
    response = model.embed_content(contents=text)
    return response["embedding"]


# ========== 4. Save to DB ==========

def create_knowledge_base(chunks, db_path="knowledge_base.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id TEXT PRIMARY KEY,
            source TEXT,
            content TEXT,
            embedding BLOB
        )
    ''')
    for content, source in chunks:
        embedding = get_embedding(content)
        if embedding:
            content_id = hashlib.sha256(content.encode()).hexdigest()
            c.execute(
                "INSERT OR IGNORE INTO knowledge (id, source, content, embedding) VALUES (?, ?, ?, ?)",
                (content_id, source, content, json.dumps(embedding))
            )
            print(f"✅ Stored: {source[:30]}...")
    conn.commit()
    conn.close()
    print(f"\n🎉 All chunks stored in {db_path}")

# ========== 5. Run Everything ==========

if __name__ == "__main__":
    print("🔍 Extracting Discourse...")
    discourse_chunks = extract_from_threads()

    print("📘 Extracting Markdown...")
    markdown_chunks = extract_from_markdown()

    all_chunks = discourse_chunks + markdown_chunks
    print(f"📦 Total chunks: {len(all_chunks)}")

    create_knowledge_base(all_chunks)
