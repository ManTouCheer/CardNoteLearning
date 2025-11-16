import json

from src.utils.m_logging import log

with open(r"data/config.json", 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

with open(f"{CONFIG['data_top_path']}", 'r', encoding='utf-8') as f:
    DATA_TOP = json.load(f)["cards"]

def save_data_top(data_top):
    with open(f"{CONFIG['data_top_path']}", 'w', encoding='utf-8') as f:
        json.dump({"cards": data_top}, f, ensure_ascii=False, indent=4)
        log.info("保存卡片数据完成")

if __name__ == "__main__":
    print(CONFIG["data_top_path"])
