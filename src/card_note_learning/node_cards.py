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
from src.utils.m_config import config
from src.m_widgets.flow_layout import FlowLayout


class ClassifyWidget(QWidget):
    def __init__(self, classify="",parent=None):
        super().__init__(parent)
        self.classify=classify
        self._layout = FlowLayout()
        self.cols = 6
        self.setLayout(self._layout)


    def injection_cards(self, data):
        self.classify = "全部"
        # self.h_layout = QHBoxLayout()
        for idx, d in enumerate(data):
            # if idx % self.cols == 0 and idx != 0:
            #     self._layout.addLayout(
            #         self.h_layout
            #     )
            #     self.h_layout = QHBoxLayout()
            self._layout.addWidget(
                d
            )
        # self._layout.addStretch()

    def add_card(self, card):
        self._layout.addWidget(
            card
        )


class NodeCardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        self.classifies = []
        self.data = {}
        self.node_cards = {}
        self.init_data()
        self.initUI()
        self.add_connects()

    def init_data(self):
        with open(config["data_top_path"], 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        w = ClassifyWidget()
        for d in self.data["cards"]:
            d["file_path"] = config["daily_path"]
            node_card: NodeCardCreator = NodeCardCreator.create(d)
            self.node_cards[node_card._id] = node_card
        w.injection_cards([x.get_card_thumbnail() for _, x in self.node_cards.items()])
        self.classifies.append(w)

    def initUI(self):
        self.add_action = QAction()
        self.add_action.setText("添加日记")
        self.add_action.triggered.connect(self.add_diary)
        self.mtoolbar = QToolBar()
        self.mtoolbar.addAction(self.add_action)
        self.addToolBar(self.mtoolbar)
        self.set_center_thumbnail()

    def set_center_detail(self, id):
        self.takeCentralWidget()
        self.setCentralWidget(
            self.node_cards[id].get_card_detail()
        )

    def set_center_thumbnail(self, id=None):
        self.takeCentralWidget()
        self.center_w = QTabWidget()
        self.setCentralWidget(self.center_w)
        for classify in self.classifies:
            self.center_w.addTab(
                classify, classify.classify
            )



    def update_title(self, new_title, _id):
        log.info(f"更新标题{id}为{new_title}")
        self.node_cards[_id].title = new_title
        # 更新缩略图标题
        for card in self.data["cards"]:
            if card["id"] == _id:
                card["title"] = new_title
                log.info(f"标题修改为：{new_title}")
                self.save_cards()
                break

    def show_edit_windows(self, id):
        log.info(f"显示编辑窗口{id}")
        self.set_center_detail(id)

    def add_diary(self):
        log.info("添加日记")

        new_card_data = {
            "classify": "日记",
            "id": str(uuid.uuid4()),
            "title": "新日记",
            "cover": "",
            "file_path": config["daily_path"]
        }
        self.data["cards"].append(new_card_data)
        new_card: NodeCardCreator = NodeCardCreator.create(new_card_data)
        self.node_cards[new_card._id] = new_card
        self.classifies[0].add_card(
            new_card.get_card_thumbnail()
        )
        self.save_cards()
        signal_bus.change2Detail.emit(new_card._id)

    def save_cards(self):
        with open(config["data_top_path"], 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        log.info("保存卡片数据完成")

    def add_connects(self):
        signal_bus.change2Detail.connect(self.show_edit_windows)
        signal_bus.showMainWindow.connect(self.set_center_thumbnail)
        signal_bus.changeTitle.connect(self.update_title)

if __name__ == '__main__':
    app = QApplication()
    # w = NodeCard().get_card_detail()
    apply_stylesheet(app, theme='dark_teal.xml')
    w = NodeCardApp()
    w.show()
    app.exit(app.exec())
