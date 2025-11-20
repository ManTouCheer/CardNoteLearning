import uuid

from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """信号总线，用于跨组件通信"""
    change2Detail = Signal(uuid.UUID)
    showMainWindow = Signal(uuid.UUID)
    # changeTitle = Signal(str, uuid.UUID)
    getOpPath = Signal(str, str)  # 对侧标题  本侧标题
signal_bus = SignalBus()
