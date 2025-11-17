import os
import re

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

from utils.m_config import CONFIG, DATA_TOP
from utils.m_logging import log

TITLE_BEGIN = "===TITLE_BEGIN==="
TITLE_END = "===TITLE_END==="
HTML_BEGIN = "===BEGIN_HTML==="
HTML_END = "===END_HTML==="
LINK_BEGIN = "===BEGIN_TEXT==="
LINK_END = "===END_TEXT==="
LINK_LIST_BEGIN = "===BEGIN_LINKS==="
LINK_LIST_END = "===END_LINKS==="


class DiaryFileProcesser(QObject):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.load_file()

    def load_file(self):
        if not os.path.exists(self.file_path):
            log.critical(f"错误 文件{self.file_path} 不存在")
            QMessageBox.critical(None, "错误", f"文件{self.file_path} 不存在")
            return
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.content = f.read()

    def get_title(self):
        # 用正则表达式匹配分隔符之间的内容（保留原格式）
        title_pattern = re.compile(
            f"{re.escape(TITLE_BEGIN)}(.*?){re.escape(TITLE_END)}",
            re.DOTALL  # 让.匹配换行符
        )
        title_match = title_pattern.search(self.content)
        title_content = title_match.group(1).strip() if title_match else ""
        return title_content

    def get_content_html(self):
        html_pattern = re.compile(
            f"{re.escape(HTML_BEGIN)}(.*?){re.escape(HTML_END)}",
            re.DOTALL  # 让.匹配换行符
        )
        html_match = html_pattern.search(self.content)
        html_content = html_match.group(1).strip() if html_match else ""
        return html_content

    def get_links_text(self):
        link_pattern = re.compile(
            f"{re.escape(LINK_BEGIN)}(.*?){re.escape(LINK_END)}",
            re.DOTALL
        )
        link_match = link_pattern.search(self.content)
        link_content = link_match.group(1).strip() if link_match else ""
        return link_content

    def get_links(self):
        link_list_pattern = re.compile(
            f"{re.escape(LINK_LIST_BEGIN)}(.*?){re.escape(LINK_LIST_END)}",
            re.DOTALL
        )
        link_list_match = link_list_pattern.search(self.content)
        link_list_content = link_list_match.group(1).strip() if link_list_match else ""
        links = [line.strip() for line in link_list_content.splitlines() if line.strip()]
        return links


    def save_file(self, title, html_content, links_text, links_list):
        try:
            html = html_content
            links_str = "\n".join(links_list)
            content = (
                f"{TITLE_BEGIN}\n{title}\n{TITLE_END}\n"
                f"{HTML_BEGIN}\n{html}\n{HTML_END}\n"
                f"{LINK_BEGIN}\n{links_text}\n{LINK_END}\n"
                f"{LINK_LIST_BEGIN}\n{links_str}\n{LINK_LIST_END}\n"
            )

            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            log.info(f"文件{self.file_path} 已保存")
            return True
        except Exception as e:
            log.critical(f"错误 无法保存文件: {str(e)}")
            QMessageBox.critical(None, "错误", f"无法保存文件: {str(e)}")

            return False

    def combo_links(self, link, add=True):
        """
        组合当前的全部链接
        """
        links = self.get_links()
        if add:
            if link in links:
                return  False, ""# 已存在，无需添加
            links.append(link)
            return True, links
        else:
            if link not in links:
                return False, ""  # 不存在
            links.remove(link)
            return True, links


    def sync_links(self, link, add=True):
        pattern = f'({LINK_LIST_BEGIN})\n.*?({LINK_LIST_END})'
        is_change, links = self.combo_links(link, add=add)
        links_str = "\n".join(links)
        new_content = replace_links_content(self.content, links_str, pattern)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        if add:
            log.info(f"文件{self.file_path} 已同步添加 {link}")
        else:
            log.info(f"文件{self.file_path} 已同步删除 {link}")

def get_op_file_path(file_name):
    base_path = CONFIG["daily_path"]
    for card in DATA_TOP:
        if card["title"] == file_name:
            return os.path.join(base_path, card["id"] + '.txt')
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