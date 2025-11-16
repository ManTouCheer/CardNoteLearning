

#  创建文件夹data
import os
import uuid

from src.utils.m_logging import log


if not os.path.exists("data") :
    os.makedirs("data")
    log.info(f"创建文件夹 data ")
else:
    log.info(f"文件夹 data 已存在 ")

# 创建配置文件 config.json
import json
config_path = "data/config.json"
if os.path.isfile(config_path):
    log.info(f"配置文件 {config_path} 已存在 ")
else:
    with open(config_path, 'w', encoding='utf-8') as f:
        default_config = {
            "data_top_path": "data/node_cards_top.json",
            "daily_path": "data/diary",
        }
        json.dump(default_config, f, indent=4, ensure_ascii=False)
    log.info(f"创建配置文件 {config_path} ")

# 创建app top配置文件
node_cards_top_path = "data/node_cards_top.json"
data_struct = {
            "cards": [{
                "classify": "全部",
                "id": uuid.uuid4().hex,
                "title": "",
                "cover": " ",
                "file_path": "../../data/diary",
                "related_links": []
            }]
        }
if os.path.isfile(node_cards_top_path):
    # 检查文件的完整性
    missing_keys = []
    re_write_all = False
    orginal_data = {}
    with open(node_cards_top_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        re_write_all = True if "cards" not in data else False
        # exits_keys = list(data["cards"][0].keys())
        for key, value in data_struct["cards"][0].items():
            if key not in data["cards"][0]:
                missing_keys.append(key)
        if len(missing_keys) > 0:
            orginal_data = data.copy()

    if re_write_all:
        with open(node_cards_top_path, 'w', encoding='utf-8') as f_w:
            json.dump(data_struct, f_w, indent=4, ensure_ascii=False)
            log.info(f"重新创建配置文件 {node_cards_top_path} ")
    elif len(missing_keys) > 0:
        for card in orginal_data["cards"]:
            for key in list(card.keys()):
                for miss_key in missing_keys:
                    card[miss_key] = data_struct["cards"][0][miss_key]
        with open(node_cards_top_path, 'w', encoding='utf-8') as f_w:
            json.dump(orginal_data, f_w, indent=4, ensure_ascii=False)
            log.info(f"重新创建配置文件 {node_cards_top_path} ")
    else:
        log.info(f"配置文件 {node_cards_top_path} 已存在 ")
else:
    with open(node_cards_top_path, 'w', encoding='utf-8') as f:
        json.dump(data_struct, f, indent=4, ensure_ascii=False)

    log.info(f"创建配置文件 {node_cards_top_path} ")