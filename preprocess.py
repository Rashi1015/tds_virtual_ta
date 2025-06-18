import os
import json
import re

def clean_text(text):
    """Remove markdown, quotes, and extra spaces"""
    text = re.sub(r'\n+', '\n', text)  # Remove extra newlines
    text = re.sub(r'\s+', ' ', text)   # Remove extra spaces
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # Remove code blocks
    text = re.sub(r'>.*?\n', '', text)  # Remove quoted replies
    return text.strip()

def extract_posts_from_topic(file_path):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)

    topic_title = data.get("title", "Untitled")
    posts = data.get("post_stream", {}).get("posts", [])

    full_text = f"### {topic_title} ###\n\n"

    for post in posts:
        author = post.get("username", "Unknown")
        cooked = post.get("cooked", "")
        cleaned = clean_text(cooked)
        full_text += f"{author}:\n{cleaned}\n\n"

    return full_text

def preprocess_all(folder="downloaded_threads", output_file="all_threads.txt"):
    files = os.listdir(folder)
    all_data = ""

    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            text = extract_posts_from_topic(file_path)
            all_data += text + "\n" + "="*80 + "\n"

    with open(output_file, "w", encoding='utf-8') as out:
        out.write(all_data)
        print(f"✅ All threads saved to: {output_file}")

if __name__ == "__main__":
    preprocess_all()
