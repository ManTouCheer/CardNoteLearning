import os
import re

from PySide6.QtGui import QTextImageFormat, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QPushButton, QMessageBox, QTextEdit, QLineEdit

from src.card_note_learning.signal_bus import signal_bus
from src.utils.m_logging import log


class EditTextForImage(QTextEdit):
    """
    支持图像 文本 编辑的文本编辑器
    """
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.parent_edit = parent
        self.content_path = ""

    def dragEnterEvent(self, e):
        """拖拽进入事件处理"""
        # 检查是否有图片文件被拖拽进来
        if not e.mimeData().hasUrls():
            e.ignore()
            return

        for url in e.mimeData().urls():
            if not url.isLocalFile():
                continue
            file_path = url.toLocalFile()
            if self.is_image_file(file_path):
                self.insert_dropped_image(file_path)

    def is_image_file(self, file_path: str) -> bool:
        """检查文件是否为图片格式"""
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']
        ext = os.path.splitext(file_path)[1].lower()
        return ext in image_extensions

    def insert_dropped_image(self, file_path: str):
        """插入拖拽的图片"""
        # 获取图片尺寸
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "错误", f"无法加载图片: {os.path.basename(file_path)}")
            return
        pixmap = pixmap.scaledToWidth(200)
        # 插入图片到当前光标位置
        cursor = self.textCursor()
        image_format = QTextImageFormat()
        image_format.setName(file_path)
        # 保持原始尺寸
        image_format.setWidth(pixmap.width())
        image_format.setHeight(pixmap.height())
        cursor.insertImage(image_format)


class TitleWin(QLineEdit):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setText(self.title)
        self.setReadOnly(True)
        self.editingFinished.connect(
            lambda :self.setReadOnly(True))


    def mouseDoubleClickEvent(self, event):
        log.info(f"开始编辑标题")
        self.setReadOnly(False)
        # 若需要保留默认双击行为（如选中单词），则调用父类方法
        super().mouseDoubleClickEvent(event)



class CardDetail(QWidget):
    TITLE_BEGIN = "===TITLE_BEGIN==="
    TITLE_END = "===TITLE_END==="
    HTML_BEGIN = "===BEGIN_HTML==="
    HTML_END = "===END_HTML==="
    LINK_BEGIN = "===BEGIN_TEXT==="
    LINK_END = "===END_TEXT==="
    def __init__(self,_id, title, data_path, parent=None):
        super().__init__()
        self._id = _id
        self.title = title
        self.content_path = os.path.join(data_path, f"content_{self._id}.html")
        self.link_path = os.path.join(data_path, f"links_{self._id}.txt")
        self.file_path = os.path.join(data_path, f"{self._id}.txt")
        self.initUI()
        self.load_file()

    def initUI(self):
        self.setWindowTitle("test")
        self.card_l = QVBoxLayout()
        self.setLayout(self.card_l)

        self.title_edit = TitleWin(self.title, self)
        self.title_edit.editingFinished.connect(
            self.change_title
        )

        self.content = EditTextForImage()
        self.content.setAcceptRichText(True)
        self.links = QPlainTextEdit()
        self.links.setMaximumHeight(150)

        self.layout_btn = QHBoxLayout()
        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_file)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(
            lambda: signal_bus.showMainWindow.emit(self._id)
        )
        self.layout_btn.addWidget(self.save_btn)
        self.layout_btn.addWidget(self.cancel_btn)

        self.card_l.addWidget(self.title_edit)
        self.card_l.addWidget(self.content)
        self.card_l.addWidget(self.links)
        self.card_l.addLayout(self.layout_btn)

    def load_file(self):
        if not os.path.exists(self.file_path):
            return

        # 读取文件内容
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 用正则表达式匹配分隔符之间的内容（保留原格式）
        title_pattern = re.compile(
            f"{re.escape(CardDetail.TITLE_BEGIN)}(.*?){re.escape(CardDetail.TITLE_END)}",
            re.DOTALL  # 让.匹配换行符
        )
        html_pattern = re.compile(
            f"{re.escape(CardDetail.HTML_BEGIN)}(.*?){re.escape(CardDetail.HTML_END)}",
            re.DOTALL  # 让.匹配换行符
        )
        link_pattern = re.compile(
            f"{re.escape(CardDetail.LINK_BEGIN)}(.*?){re.escape(CardDetail.LINK_END)}",
            re.DOTALL
        )

        # 提取内容（去除首尾空白）
        title_match = title_pattern.search(content)
        html_match = html_pattern.search(content)
        link_match = link_pattern.search(content)

        title_content = title_match.group(1).strip() if title_match else ""
        html_content = html_match.group(1).strip() if html_match else ""
        link_content = link_match.group(1).strip() if link_match else ""

        self.title_edit.setText(title_content)
        self.content.setHtml(html_content)
        self.links.setPlainText(link_content)


    # def load_content(self):
    #     if not os.path.isfile(self.content_path):
    #         log.info(f"内容文件不存在: {self.content_path}")
    #         return
    #     with open(self.content_path, 'r', encoding='utf-8') as f:
    #         html = f.read()
    #         self.content.setHtml(html)
    #
    # def load_links(self):
    #     if not os.path.isfile(self.link_path):
    #         log.info(f"链接文件不存在: {self.link_path}")
    #         return
    #     with open(self.link_path, 'r', encoding='utf-8') as f:
    #         links_text = f.read()
    #         self.links.setPlainText(links_text)


    # def save_file_as(self):
    #     """另存为文件"""
    #     file_path, _ = QFileDialog.getSaveFileName(
    #         self, "另存为", "",
    #         "富文本文件 (*.html);;所有文件 (*)")
    #     if file_path:
    #         # 确保文件有.html扩展名
    #         if not file_path.endswith('.html'):
    #             file_path += '.html'
    #         self.content_path = file_path
    #         self.setWindowTitle(f"文档编辑器 - {os.path.basename(file_path)}")
    #         return self.save_file()
    #     return False

    def save_file(self):
        """保存文件"""
        # if not self.content_path:
        #     return self.save_file_as()

        try:
            html = self.content.toHtml()
            # with open(self.content_path, 'w', encoding='utf-8') as f:
            #     f.write(html)
            # self.content.document().setModified(False)
            # with open(self.link_path, "w", encoding="utf-8") as f:
            #     f.write(self.links.toPlainText())

            content = (
                f"{CardDetail.TITLE_BEGIN}\n{self.title_edit.text()}\n{CardDetail.TITLE_END}\n"
                f"{CardDetail.HTML_BEGIN}\n{html}\n{CardDetail.HTML_END}\n"
                f"{CardDetail.LINK_BEGIN}\n{self.links.toPlainText()}\n{CardDetail.LINK_END}\n"
            )

            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True
        except Exception as e:
            log.critical(f"错误 无法保存文件: {str(e)}")
            QMessageBox.critical(self, "错误", f"无法保存文件: {str(e)}")

            return False


    def change_title(self):
        self.title = self.title_edit.text()
        self.save_file()
        signal_bus.changeTitle.emit(self.title, self._id)

