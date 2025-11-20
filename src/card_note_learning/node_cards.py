import uuid

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QApplication, QToolBar
)

import json
from qt_material import apply_stylesheet

from src.card_note_learning.card_creator import NodeCardCreator
from src.utils.m_logging import log
from src.card_note_learning.signal_bus import signal_bus
from src.utils.m_config import CONFIG, DATA_TOP, save_data_top, DIARY_PATH
from src.m_widgets.flow_layout import FlowLayout
from utils.utils import get_file_list


class ClassifyWidget(QWidget):
    def __init__(self, classify="",parent=None):
        super().__init__(parent)
        self.classify=classify
        self._layout = FlowLayout()
        self.cols = 6
        self.setLayout(self._layout)

    def add_cards(self, cards):
        if len(cards) <= 0:
            return
        # self.classify = cards[0].classify
        for idx, d in enumerate(cards):
            self._layout.addWidget(
                d
            )

    def add_card(self, card):
        self._layout.addWidget(
            card
        )

    def clear(self):

        def _clear(w):
            while w.count():
                item = w.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    _clear(item)
        _clear(self)


class NodeCardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        self.classifies = {}
        self.data = []
        self.node_cards = {}
        self.init_card()
        self.initUI()
        self.set_center_thumbnail()
        self.add_connects()

    def get_cards(self):
        paths = get_file_list(DIARY_PATH)
        for path in paths:
            node_card: NodeCardCreator = NodeCardCreator.mCreate(path)
            node_card.load_data()
            self.node_cards[node_card._id] = node_card

    def get_classify_thumbnail(self):
        classifies = {}
        for _id, card in self.node_cards.items():
            if card.classify not in classifies:
                classifies[card.classify] = []
            classifies[card.classify].append(card.get_card_thumbnail())

        for classify, cards in classifies.items():
            w = ClassifyWidget(classify=classify)
            w.add_cards(cards)
            if classify not in self.classifies:
                self.classifies[classify] = []
            self.classifies[classify] = w

    def init_card(self):
        self.get_cards()
        self.get_classify_thumbnail()


    def initUI(self):
        self.add_action = QAction()
        self.add_action.setText("添加日记")
        self.add_action.triggered.connect(self.add_diary)
        self.mtoolbar = QToolBar()
        self.mtoolbar.addAction(self.add_action)
        self.addToolBar(self.mtoolbar)


    def set_center_detail(self, id):
        self.takeCentralWidget()
        self.setCentralWidget(
            self.node_cards[id].get_card_detail()
        )

    def set_center_thumbnail(self):
        self.takeCentralWidget()
        self.center_w = QTabWidget()
        # self.center_w.setToolTip("afdsafs")
        self.setCentralWidget(self.center_w)
        for classify, w in self.classifies.items():
            self.center_w.addTab(w, classify)

    # def update_title(self, new_title, _id):
    #     log.info(f"更新标题{id}为{new_title}")
    #     self.node_cards[_id].title = new_title
    #     # 更新缩略图标题
    #     for card in self.data:
    #         if card["id"] == _id:
    #             card["title"] = new_title
    #             log.info(f"标题修改为：{new_title}")
    #             self.save_cards()
    #             b
    def show_edit_windows(self, id):
        self.set_center_detail(id)

    def add_diary(self):
        log.info("添加日记")
        #
        # new_card_data = {
        #     "classify": "日记",
        #     "id": str(uuid.uuid4()),
        #     "title": "新日记",
        #     "cover": "",
        #     "file_path": CONFIG["daily_path"]
        # }
        # self.data.append(new_card_data)
        classify = self.center_w.tabText(self.center_w.currentIndex())
        new_card: NodeCardCreator = NodeCardCreator.mCreate_by_default(classify=classify)

        self.node_cards[new_card._id] = new_card
        # self.classifies[classify].add_card(
        #     new_card.get_card_thumbnail()
        # )
        new_card.save_new_file()

        # self.save_cards()
        signal_bus.change2Detail.emit(new_card._id)

    # def save_cards(self):
    #     # 添加top配置文件
    #     save_data_top(self.data)

        # with open(CONFIG["data_top_path"], 'w', encoding='utf-8') as f:
        #     json.dump(self.data, f, ensure_ascii=False, indent=4)

    def back2center_thumbnail(self):
        self.takeCentralWidget()
        self.init_card()
        self.set_center_thumbnail()

    def sync_link(self, title, m_title):
        for id, card in self.node_cards.items():
            if card.title == title:  # 对侧卡片
                op_card:NodeCardCreator = self.node_cards[id]
                op_card.save_sync_links(m_title)
                break


    def add_connects(self):
        signal_bus.change2Detail.connect(self.show_edit_windows)
        signal_bus.showMainWindow.connect(self.back2center_thumbnail)
        # signal_bus.changeTitle.connect(self.update_title)
        signal_bus.getOpPath.connect(self.sync_link)



if __name__ == '__main__':
    app = QApplication()
    # w = NodeCard().get_card_detail()
    apply_stylesheet(app, theme='dark_teal.xml')
    w = NodeCardApp()
    w.show()
    app.exit(app.exec())
