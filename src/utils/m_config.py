import json

from src.utils.m_logging import log

## diary 文件结构
TITLE_BEGIN = "===TITLE_BEGIN==="
TITLE_END = "===TITLE_END==="
HTML_BEGIN = "===BEGIN_HTML==="
HTML_END = "===END_HTML==="
LINK_BEGIN = "===BEGIN_TEXT==="
LINK_END = "===END_TEXT==="
LINK_LIST_BEGIN = "===BEGIN_LINKS==="
LINK_LIST_END = "===END_LINKS==="
BEFGIN_CONFIG = "===BEFGIN_CONFIG==="
END_CONFIG = "===END_CONFIG==="


with open(r"data/config.json", 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)
DIARY_PATH = CONFIG["daily_path"]


with open(f"{CONFIG['data_top_path']}", 'r', encoding='utf-8') as f:
    DATA_TOP = json.load(f)["cards"]

def save_data_top(data_top):
    with open(f"{CONFIG['data_top_path']}", 'w', encoding='utf-8') as f:
        json.dump({"cards": data_top}, f, ensure_ascii=False, indent=4)
        log.info("保存卡片数据完成")

if __name__ == "__main__":
    print(CONFIG["data_top_path"])
