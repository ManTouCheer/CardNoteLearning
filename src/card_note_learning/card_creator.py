import json
import os
import uuid

from PySide6.QtGui import QPixmap, QTextImageFormat
from PySide6.QtWidgets import QTextEdit, QMessageBox, QWidget, QLabel, QVBoxLayout, QPlainTextEdit, QPushButton, \
    QHBoxLayout, QFileDialog

from src.card_note_learning.signal_bus import signal_bus
from src.card_note_learning.card_detail import CardDetail
from src.card_note_learning.card_thumbnail import CardThumbnail
from utils.diary_file_processer import DiaryFileProcesser
from utils.m_config import DIARY_PATH
from utils.m_logging import log


class NodeCardCreator(QWidget):
    def __init__(self,classify="", path=None):
        super().__init__()
        self._id = uuid.uuid4().hex
        self.title = ""
        self.classify = ""
        self.cover=""
        self.file_path = ""
        self.file_processer = None

    @classmethod
    def mCreate(self, path):
        obj = NodeCardCreator()
        obj.file_path = path
        obj.check_file_struct()
        # obj.load_data()
        return obj

    @classmethod
    def mCreate_by_default(cls, classify=""):
        ## 创建默认文件
        obj = NodeCardCreator()
        obj.file_path = os.path.join(DIARY_PATH, f"{obj._id}.txt")
        obj.classify = classify
        obj.check_file_struct()
        return obj


    def load_data(self):
        self.file_processer = DiaryFileProcesser(self.file_path)
        config = self.file_processer.get_config()
        self._id = config["id"]
        self.title = self.file_processer.get_title()
        self.classify = config["classify"]

    # @classmethod
    # def mCreate(cls, data_dict:dict):
    #     obj = NodeCardCreator(classify=data_dict.get("classify", ""))
    #     obj._id = data_dict.get("id", uuid.uuid4())
    #     obj.title = data_dict.get("title", "")
    #     obj.cover = data_dict.get("cover", "")
    #     obj.file_path = data_dict.get("file_path", "")
    #
    #     return obj

    def get_card_thumbnail(self):
        self.card_thumbnail = CardThumbnail(self._id, self.title,self.classify, self)
        return self.card_thumbnail

    def get_card_detail(self):
        log.info(f"展示窗口{self.title}  {self.file_path}")
        self.card_d = CardDetail(
            self._id,
            self.title,
            self.file_path,
            self
        )
        return self.card_d

    def save_new_file(self):
        self.check_file_struct()

    def save_sync_links(self, op_title):

        file = DiaryFileProcesser(self.file_path)
        links = file.get_links()
        if op_title not in links:
            links.append(op_title)
        else:
            links.remove(op_title)

        file.save_file(
            title=file.get_title(),
            html_content=file.get_content_html(),
            links_text=file.get_links_text(),
            links_list=links,
            config=file.get_config()
        )


    def check_file_struct(self):
        if not os.path.isfile(self.file_path):
            log.info(f"文件{self.file_path} 不存在")
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write("")
            log.info(f"已创建文件{self.file_path}")
        file = DiaryFileProcesser(self.file_path)
        new_config = {
            "classify": self.classify,
            "id": self._id,
            "title": self.title,
            "cover": self.cover,
            "file_path": os.path.join(DIARY_PATH, f"{self._id}.txt"),
        }
        config = file.get_config()
        if not config:
            file.save_file(
                title=file.get_title(),
                html_content=file.get_content_html(),
                links_text=file.get_links_text(),
                links_list="\n".join(file.get_links()),
                config=new_config if not config else config
            )


