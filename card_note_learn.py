from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from src.card_note_learning.node_cards import NodeCardApp

def main():
    app = QApplication()
    # w = NodeCard().get_card_detail()
    apply_stylesheet(app, theme='dark_teal.xml')
    w = NodeCardApp()
    w.show()
    app.exit(app.exec())
    # node_card_app = NodeCardApp()

if __name__ == "__main__":
    main()
