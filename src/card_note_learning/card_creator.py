import os
import uuid

from PySide6.QtGui import QPixmap, QTextImageFormat
from PySide6.QtWidgets import QTextEdit, QMessageBox, QWidget, QLabel, QVBoxLayout, QPlainTextEdit, QPushButton, \
    QHBoxLayout, QFileDialog

from src.card_note_learning.signal_bus import signal_bus
from src.card_note_learning.card_detail import CardDetail
from src.card_note_learning.card_thumbnail import CardThumbnail





class NodeCardCreator(QWidget):
    def __init__(self,classify=""):
        super().__init__()
        self._id = uuid.uuid4()
        self.title = ""
        self.classify = classify
        self.cover=""
        self.file_path = ""

    @classmethod
    def create(cls, data_dict:dict):
        obj = NodeCardCreator(classify=data_dict.get("classify", ""))
        obj._id = data_dict.get("id", uuid.uuid4())
        obj.title = data_dict.get("title", "")
        obj.cover = data_dict.get("cover", "")
        obj.file_path = data_dict.get("file_path", "")
        return obj

    def get_card_thumbnail(self):
        self.card_thumbnail = CardThumbnail(self._id, self.title, self)
        return self.card_thumbnail

    def get_card_detail(self):
        self.card_d = CardDetail(
            self._id,
            self.title,
            self.file_path,
            self
        )
        return self.card_d
