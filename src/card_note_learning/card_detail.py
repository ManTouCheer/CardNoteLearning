import os
import re

from PySide6.QtGui import QTextImageFormat, QPixmap, QPainter, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QPushButton, QMessageBox, QTextEdit, \
    QLineEdit, QComboBox, QListWidget, QSizePolicy, QStyle, QStyleOption, QStyleOptionFrame

from src.card_note_learning.signal_bus import signal_bus
from src.utils.m_logging import log
from utils.diary_file_processer import DiaryFileProcesser, get_op_file_path, load_all_diary_title
from utils.m_config import DATA_TOP


class EditTextForImage(QTextEdit):
    """
    支持图像 文本 编辑的文本编辑器
    """
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        # self.parent_edit = parent
        # self.content_path = ""

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

    # def paintEvent(self, event):
    #     # 1. 创建画家对象，开启抗锯齿
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    #
    #     # 2. 创建QTextEdit对应的样式选项（关键：传递控件状态给样式系统）
    #     option = QStyleOptionFrame()
    #     # 从当前控件初始化选项（自动获取状态：焦点、悬停、禁用等）
    #     option.initFrom(self)
    #     # 设置绘制区域为控件整个可视区域
    #     option.rect = self.rect()
    #     # 确保样式选项包含正确的状态标识（如焦点状态）
    #     if self.hasFocus():
    #         option.state |= QStyle.StateFlag.State_HasFocus
    #
    #     # 3. 调用样式系统绘制基础样式（核心：让样式表生效）
    #     #    CE_TextEdit 是QTextEdit对应的绘制类型
    #     self.style().drawControl(
    #         QStyle.ControlElement.CE_ShapedFrame,  # 绘制类型：文本编辑框
    #         option,                             # 样式选项（含状态和区域）
    #         painter,                            # 画家对象
    #         self                                # 当前控件
    #     )

        # 4. （可选）添加自定义绘制内容（在样式表基础上叠加）
        #    示例：在右上角绘制一个小图标（如果需要）
        # self.drawCustomImage(painter)
    #     # 1. 创建画家对象
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿
    #
    #     # 2. 创建样式选项对象（关键：用于传递控件状态和样式信息）
    #     option = QStyleOption()
    #     option.initFrom(self)  # 从当前控件初始化选项（自动获取状态：hover、pressed等）
    #     option.rect = self.rect()  # 设置绘制区域
    #
    #     # 3. 调用样式系统绘制控件（使用正确的参数格式）
    #     # 参数说明：
    #     # - 第一个：绘制类型（如通用控件CE_Widget）
    #     # - 第二个：样式选项（包含状态和区域等信息）
    #     # - 第三个：画家对象
    #     # - 第四个：当前控件（可选）
    #     self.style().drawControl(
    #         QStyle.ControlElement.CE_CustomBase,  # 绘制类型
    #         option,  # 样式选项（必须是QStyleOption类型）
    #         painter,  # 画家
    #         self  # 当前控件
    #     )
    #
    #     # 4. （可选）叠加自定义绘制内容（如文本）
    #     painter.drawText(
    #         self.rect(),
    #         Qt.AlignmentFlag.AlignCenter,
    #         "样式表生效的自定义控件"
    #     )

class TitleWin(QLineEdit):
    """
    可双击编辑标题的单行文本框
    """
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setText(self.title)
        self.setReadOnly(True)
        self.editingFinished.connect(
            lambda :self.setReadOnly(True))


    def mouseDoubleClickEvent(self, event):
        log.info(f"正在编辑标题")
        self.setReadOnly(False)
        # 若需要保留默认双击行为（如选中单词），则调用父类方法
        super().mouseDoubleClickEvent(event)


class LinkList(QListWidget):
    """
    关联链接列表
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cur_item = None
        self.doubleClicked.connect(self.doubleClicked_delete_item)

    # def addItem(self, item, /):
    #     self.addItem(item)

    def doubleClicked_delete_item(self, index):
        self.cur_item = self.takeItem(index.row())





class CardDetail(QWidget):
    def __init__(self,_id, title, file_path, parent=None):
        super().__init__(parent)
        self._id = _id
        self.title = title
        self.file_path = file_path
        self.html_content = ""
        self.link_text_content = ""
        self.link_content = []
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

        self.content = EditTextForImage(self)
        self.content.setAcceptRichText(True)
        self.links_combo = QComboBox(self)
        self.links_combo_btn = QPushButton("确定",parent=self)
        self.links_combo_btn.clicked.connect(self.add_link)
        self.links_combo_btn.setMaximumWidth(150)
        combo_layout = QHBoxLayout(self)
        combo_layout.addWidget(self.links_combo)
        combo_layout.addWidget(self.links_combo_btn)
        self.links_related = LinkList(self)
        self.links_related.doubleClicked.connect(self.delete_link)
        link_layout_l = QVBoxLayout(self)
        link_layout_l.addLayout(combo_layout)
        link_layout_l.addWidget(self.links_related)
        self.links = QPlainTextEdit(self)
        self.links.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

        link_layout_r = QHBoxLayout(self)
        link_layout_r.addLayout(link_layout_l)
        link_layout_r.addWidget(self.links)

        self.layout_btn = QHBoxLayout(self)
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
        self.card_l.addLayout(link_layout_r)
        self.card_l.addLayout(self.layout_btn)

    @property
    def links_related_list(self):
        return [self.links_related.item(idx).text() for idx in range(self.links_related.count())]

    def load_file(self):
        if os.path.exists(self.file_path):
            file_processer = DiaryFileProcesser(self.file_path)
            self.title = file_processer.get_title()
            self.html_content = file_processer.get_content_html()
            self.link_text_content = file_processer.get_links_text()
            self.link_content = file_processer.get_links()
        else:
            self.create_file()

        for title in load_all_diary_title():
            self.links_combo.addItem(title)
        # if not os.path.exists(self.file_path):
        #     return
        #
        # # 读取文件内容
        # with open(self.file_path, "r", encoding="utf-8") as f:
        #     content = f.read()
        #
        # # 用正则表达式匹配分隔符之间的内容（保留原格式）
        # title_pattern = re.compile(
        #     f"{re.escape(CardDetail.TITLE_BEGIN)}(.*?){re.escape(CardDetail.TITLE_END)}",
        #     re.DOTALL  # 让.匹配换行符
        # )
        # html_pattern = re.compile(
        #     f"{re.escape(CardDetail.HTML_BEGIN)}(.*?){re.escape(CardDetail.HTML_END)}",
        #     re.DOTALL  # 让.匹配换行符
        # )
        # link_pattern = re.compile(
        #     f"{re.escape(CardDetail.LINK_BEGIN)}(.*?){re.escape(CardDetail.LINK_END)}",
        #     re.DOTALL
        # )
        #
        # # 提取内容（去除首尾空白）
        # title_match = title_pattern.search(content)
        # html_match = html_pattern.search(content)
        # link_match = link_pattern.search(content)
        #
        # title_content = title_match.group(1).strip() if title_match else ""
        # html_content = html_match.group(1).strip() if html_match else ""
        # link_content = link_match.group(1).strip() if link_match else ""

        self.title_edit.setText(self.title)
        self.content.setHtml(self.html_content)
        self.links.setPlainText(self.link_text_content)
        for link in self.link_content:
            self.links_related.addItem(link)

    def save_file(self):
        """保存文件"""
        processer = DiaryFileProcesser(self.file_path)
        processer.save_file(
            self.title_edit.text(),
            self.content.toHtml(),
            self.links.toPlainText(),
            self.links_related_list,
            str(processer.get_config())
        )

    def create_file(self):
        """创建文件"""
        processer = DiaryFileProcesser(self.file_path)
        processer.save_file(
            self.title,
            self.html_content,
            self.link_text_content,
            self.link_content
        )

    def change_title(self):
        self.title = self.title_edit.text()
        # self.save_file()
        # signal_bus.changeTitle.emit(self.title, self._id)

    def add_link(self):

        link = self.links_combo.currentText()
        if link in self.links_related_list:
            return
        self.links_related.addItem(link)
        self.save_file()
        # 添加链接 同时对侧也需要添加链接
        signal_bus.getOpPath.emit(link, self.title)
        # op_path = get_op_file_path(link)
        # if op_path is not None:
        #     processer = DiaryFileProcesser(op_path)
        #     processer.sync_links(self.title)

    def delete_link(self,index):
        link = self.links_related.cur_item.text()
        self.save_file()
        signal_bus.getOpPath.emit(link, self.title)
        # 删除链接 同时对侧也需要删除链接
        # op_path = get_op_file_path(link)
        # if op_path is not None:
        #     processer = DiaryFileProcesser(op_path)
        #     processer.sync_links(self.title, add=False)

