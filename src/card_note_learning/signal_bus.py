import uuid

from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """信号总线，用于跨组件通信"""
    change2Detail = Signal(uuid.UUID)
    showMainWindow = Signal(uuid.UUID)
    changeTitle = Signal(str, uuid.UUID)

signal_bus = SignalBus()
