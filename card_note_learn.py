from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

# from data.css import dark_stylesheet
from src.card_note_learning.node_cards import NodeCardApp

from PySide6.QtCore import QFile, QTextStream

from utils.m_logging import log


def load_stylesheet(file_path):
    """加载QSS样式表文件"""
    # 创建文件对象
    file = QFile(file_path)
    # 以只读方式打开文件
    if file.open(QFile.ReadOnly | QFile.Text):
        # 读取文件内容
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        # 关闭文件
        file.close()
        return stylesheet
    else:
        # 打印错误信息（文件不存在或无法打开）
        print(f"无法加载样式表文件: {file.errorString()}")
        return ""


def main():
    app = QApplication()
    # w = NodeCard().get_card_detail()
    # 加载并应用样式表（确保dark_style.qss与脚本在同一目录，或使用绝对路径）
    stylesheet = load_stylesheet("data/dark_style.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)
        log.info(f"加载样式表成功")
    w = NodeCardApp()

    w.show()
    app.exit(app.exec())
    # node_card_app = NodeCardApp()

if __name__ == "__main__":
    main()
