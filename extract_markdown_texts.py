# extract_markdown_texts.py
import os

SOURCE_DIR = "tds_content"
OUTPUT_DIR = "tds_txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_all_markdown_files():
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".md"):
                input_path = os.path.join(root, file)
                text = extract_text_from_md(input_path)

                # Sanitize filename and write to output
                output_filename = file.replace(".md", ".txt")
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                with open(output_path, "w", encoding="utf-8") as out_file:
                    out_file.write(text)

                print(f"✅ Saved {output_filename}")

if __name__ == "__main__":
    process_all_markdown_files()
