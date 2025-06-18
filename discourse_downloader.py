import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("DISCOURSE_BASE_URL")
SESSION_COOKIE = os.getenv("DISCOURSE_SESSION_COOKIE")
DISCOURSE_USER = os.getenv("DISCOURSE_USER")

HEADERS = {
    "Cookie": f"_t={SESSION_COOKIE}",
    "User-Agent": "Mozilla/5.0"
}

def fetch_latest_topics(limit=10):
    url = f"{BASE_URL}/latest.json"
    response = requests.get(url, headers=HEADERS)

    print("Status Code:", response.status_code)
    data = response.json()
    
    if 'errors' in data:
        print("❌ Error from server:", data['errors'])
        return []

    topics = data["topic_list"]["topics"][:limit]
    return topics


def fetch_full_topic(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Could not fetch topic {topic_id}")
        return None
    return response.json()



def save_topics_to_file(topics, folder="downloaded_threads"):
    os.makedirs(folder, exist_ok=True)
    for topic in topics:
        topic_id = topic["id"]
        full_topic = fetch_full_topic(topic_id)
        if full_topic:
            with open(f"{folder}/{topic_id}.json", "w", encoding="utf-8") as f:
                json.dump(full_topic, f, indent=2)
                print(f"✅ Saved topic {topic_id}")



if __name__ == "__main__":
    print("Username:", DISCOURSE_USER)
    topics = fetch_latest_topics(20)
    save_topics_to_file(topics)
