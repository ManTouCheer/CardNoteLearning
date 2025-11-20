import json
import os
import re

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

from utils.m_config import CONFIG, DATA_TOP, DIARY_PATH, TITLE_BEGIN, TITLE_END, HTML_BEGIN, HTML_END, LINK_BEGIN, \
    LINK_END, LINK_LIST_BEGIN, LINK_LIST_END, BEFGIN_CONFIG, END_CONFIG
from utils.m_logging import log




class DiaryFileProcesser(QObject):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.load_file()

    def load_file(self):
        if not os.path.exists(self.file_path):
            # with open(self.file_path, "w", encoding="utf-8") as f:
            #     self.save_file("", "", "", [])
            #     log.info(f"文件{self.file_path} 不存在，已创建")
            log.critical(f"错误 文件{self.file_path} 不存在")
            QMessageBox.critical(None, "错误", f"文件{self.file_path} 不存在")
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.content = f.read()


    def get_title(self):
        # 用正则表达式匹配分隔符之间的内容（保留原格式）
        _, title_content = match_text(TITLE_BEGIN, TITLE_END, self.content)
        # title_pattern = re.compile(
        #     f"{re.escape(TITLE_BEGIN)}(.*?){re.escape(TITLE_END)}",
        #     re.DOTALL  # 让.匹配换行符
        # )
        # title_match = title_pattern.search(self.content)
        # title_content = title_match.group(1).strip() if title_match else ""
        return title_content

    def get_content_html(self):
        _, html_content = match_text(HTML_BEGIN, HTML_END, self.content)
        # html_pattern = re.compile(
        #     f"{re.escape(HTML_BEGIN)}(.*?){re.escape(HTML_END)}",
        #     re.DOTALL  # 让.匹配换行符
        # )
        # html_match = html_pattern.search(self.content)
        # html_content = html_match.group(1).strip() if html_match else ""
        return html_content

    def get_links_text(self):
        _, link_content = match_text(LINK_BEGIN, LINK_END, self.content)
        # link_pattern = re.compile(
        #     f"{re.escape(LINK_BEGIN)}(.*?){re.escape(LINK_END)}",
        #     re.DOTALL
        # )
        # link_match = link_pattern.search(self.content)
        # link_content = link_match.group(1).strip() if link_match else ""
        return link_content

    def get_links(self):
        _, link_list_content = match_text(LINK_LIST_BEGIN, LINK_LIST_END, self.content)
        # link_list_pattern = re.compile(
        #     f"{re.escape(LINK_LIST_BEGIN)}(.*?){re.escape(LINK_LIST_END)}",
        #     re.DOTALL
        # )
        # link_list_match = link_list_pattern.search(self.content)
        # link_list_content = link_list_match.group(1).strip() if link_list_match else ""
        links = [line.strip() for line in link_list_content.splitlines() if line.strip()]
        return links

    def get_config(self):
        ## TODO 未来可能会用到
        has_file, config = match_text(BEFGIN_CONFIG, END_CONFIG, self.content)
        # config_pattern = re.compile(
        #     f"{re.escape(BEFGIN_CONFIG)}(.*?){re.escape(END_CONFIG)}",
        #     re.DOTALL
        # )
        # config_match = config_pattern.search(self.content)
        # link_list_content = config_match.group(1).strip() if config_match else ""
        config = eval(config) if has_file else {}
        return config


    def save_file(self, title, html_content, links_text, links_list, config={}):
        try:
            html = html_content
            links_str = "\n".join(links_list)
            config = str(config)
            content = (
                f"{TITLE_BEGIN}\n{title}\n{TITLE_END}\n"
                f"{HTML_BEGIN}\n{html}\n{HTML_END}\n"
                f"{LINK_BEGIN}\n{links_text}\n{LINK_END}\n"
                f"{LINK_LIST_BEGIN}\n{links_str}\n{LINK_LIST_END}\n"
                f"{BEFGIN_CONFIG}\n{config}\n{END_CONFIG}\n"
            )

            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            log.info(f"文件{self.file_path} 已保存")
            return True
        except Exception as e:
            log.critical(f"错误 无法保存文件: {str(e)}")
            QMessageBox.critical(None, "错误", f"无法保存文件: {str(e)}")

            return False

    # def combo_links(self, link, add=True):
    #     """
    #     组合当前的全部链接
    #     """
    #     links = self.get_links()
    #     if add:
    #         if link in links:
    #             return  False, ""# 已存在，无需添加
    #         links.append(link)
    #         return True, links
    #     else:
    #         if link not in links:
    #             return False, ""  # 不存在
    #         links.remove(link)
    #         return True, links


    # def sync_links(self, link, add=True):
    #     pattern = f'({LINK_LIST_BEGIN})\n.*?({LINK_LIST_END})'
    #     is_change, links = self.combo_links(link, add=add)
    #     links_str = "\n".join(links)
    #     new_content = replace_links_content(self.content, links_str, pattern)
    #     with open(self.file_path, 'w', encoding='utf-8') as f:
    #         f.write(new_content)
    #     if add:
    #         log.info(f"文件{self.file_path} 已同步添加 {link}")
    #     else:
    #         log.info(f"文件{self.file_path} 已同步删除 {link}")

def get_op_file_path(file_name):
    base_path = DIARY_PATH
    for card in DATA_TOP:
        if card["title"] == file_name:
            return os.path.join(DIARY_PATH, card["id"] + '.txt')
    return None


def replace_links_content(original_text, new_content, pattern):
    ## TODO 本判断在下一次升级时删除
    if not re.search(pattern, original_text, flags=re.DOTALL):
        return original_text + f"{LINK_LIST_BEGIN}\n{new_content}\n{LINK_LIST_END}\n"
    # 替换为：起始标记 + 新内容 + 结束标记（保持标记不变，仅替换中间内容）
    replaced_text = re.sub(
        pattern,
        lambda m: f"{m.group(1)}\n{new_content}\n{m.group(2)}",  # 保留原始标记，插入新内容
        original_text,
        flags=re.DOTALL  # 让 . 匹配换行符
    )
    return replaced_text

def load_all_diary_title():
    if not os.path.exists(DIARY_PATH):
        os.makedirs(DIARY_PATH)
        log.info(f"创建日记文件夹 {DIARY_PATH} ")
    diary_files = []
    for file_name in os.listdir(DIARY_PATH):
        if file_name.endswith('.txt'):
            diary_files.append(os.path.join(DIARY_PATH, file_name))
    return [DiaryFileProcesser(x).get_title() for x in diary_files]


def match_text(begin, end, content):
    """
    用正则表达式匹配分隔符之间的内容（保留原格式）
    """
    config_pattern = re.compile(
        f"{re.escape(begin)}(.*?){re.escape(end)}",
        re.DOTALL
    )
    config_match = config_pattern.search(content)
    if config_match:
        link_list_content = config_match.group(1).strip()
        return True, link_list_content
    else:
        return False, ""