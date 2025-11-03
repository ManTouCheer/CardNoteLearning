from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.card_note_learning.signal_bus import signal_bus
from src.utils.m_logging import log


class CardThumbnail(QLabel):

    def __init__(self, id, title, parent=None):
        super().__init__(parent)
        self.id = id
        self.setFixedSize(100, 80)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px dashed gray")
        self.setText(title)
        self.setWordWrap(True)
        self.add_connects()

    def add_connects(self):
        signal_bus.changeTitle.connect(self.update_title)

    def mouseReleaseEvent(self, e):
        """鼠标释放事件处理"""
        super().mouseReleaseEvent(e)
        # 可以在这里添加其他鼠标释放后的处理逻辑
        signal_bus.change2Detail.emit(self.id)

    def update_title(self, title, id):
        log.info(f"CardThumbnail 收到更新标题信号: {title}, {id}")
        if id == self.id:
            self.setText(title)
