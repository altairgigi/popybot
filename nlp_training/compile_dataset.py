import os
import json

DATA_DIR = "intents_data"
OUTPUT_FILE = "intents.json"

def compile_intents():
    dataset = {"intents": []}

    if not os.path.exists(DATA_DIR):
        print(f"Error: directory {DATA_DIR} not found!")
        return

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            tag_name = os.path.splitext(filename)[0]
            file_path = os.path.join(DATA_DIR, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    pattern = data.get("patterns", [])

                    intent_entry = {
                        "tag": tag_name,
                        "patterns": pattern
                    }

                    dataset["intents"].append(intent_entry)
                    print(f"File {filename} loaded!")
                except json.JSONDecodeError:
                    print(f"File {filename} loading failed!")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(dataset, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    compile_intents()