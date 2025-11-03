import json

with open(r"data/config.json", 'r', encoding='utf-8') as f:
    config = json.load(f)

if __name__ == "__main__":
    print(config["data_top_path"])
