from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import os
import requests
from dotenv import load_dotenv
load_dotenv()


HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
 # or another GPT-like model

app = FastAPI()

def load_all_content():
    data_parts = []

    if os.path.exists("all_threads.txt"):
        with open("all_threads.txt", "r", encoding='utf-8') as f:
            data_parts.append(f.read())

    markdown_folder = "tds_content"
    if os.path.exists(markdown_folder):
        for filename in os.listdir(markdown_folder):
            if filename.endswith(".md"):
                with open(os.path.join(markdown_folder, filename), "r", encoding="utf-8") as f:
                    data_parts.append(f"### {filename} ###\n\n" + f.read())

    return "\n\n".join(data_parts)

content = load_all_content()

@app.get("/")
def read_root():
    return {"message": "Welcome to the TDS Virtual TA API 👋"}

@app.get("/ask")
def ask_question(q: str = Query(..., description="Enter your question")):
    q_lower = q.lower().split()
    matches = [para for para in content.split("\n\n") if all(word in para.lower() for word in q_lower)]

    if not matches:
        return JSONResponse({"message": "No relevant content found."})

    context = "\n\n".join(matches[:3])
    prompt = f"""You are a helpful assistant for students. Use the following context to answer the question:\n\nContext:\n{context}\n\nQuestion: {q}\n\nAnswer:"""

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        result = response.json()
        if isinstance(result, dict) and "generated_text" in result:
            answer = result["generated_text"]
        elif isinstance(result, list):
            answer = result[0]["generated_text"]
        else:
            answer = str(result)
        return JSONResponse({"question": q, "answer": answer.strip()})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
