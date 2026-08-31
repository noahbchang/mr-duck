from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, QTime

class TimerMode(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.Window | 
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)

        self.label = QLabel()
        self.label.setStyleSheet("""
            background-color: rgba(225, 225, 225, 160);
            color: rgba(0, 0, 0, 255);
            border-radius: 12px;
            padding: 8px;
            font-weight: bold;
            font-size: 20px;
        """)
        layout.addWidget(self.label)
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = QTime.currentTime()
        self.label.setText(now.toString("hh:mm:ss AP"))
