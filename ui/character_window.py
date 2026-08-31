from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from important.event_bus import event_bus


ASSISTANT_SIZE = (160, 160)
BOTTOM_RIGHT_OFFSET = (20, 0)
BUBBLE_CLUSTER_OFFSET_Y = 140

class CharacterWindow(QLabel):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setWindowFlag(Qt.WindowTransparentForInput, False)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus)

        pix = QPixmap("assets/mrduck.png").scaled(
            ASSISTANT_SIZE[0],
            ASSISTANT_SIZE[1],
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.setPixmap(pix)
        self.move_to_bottom_right()

    def mousePressEvent(self, event):
        event_bus.emit("character_clicked")
        self.clearFocus()

    def move_to_bottom_right(self):
        screen = self.screen().geometry()
        x = screen.width() - ASSISTANT_SIZE[0] - BOTTOM_RIGHT_OFFSET[0]
        y = screen.height() - ASSISTANT_SIZE[1] - BOTTOM_RIGHT_OFFSET[1]
        self.move(x, y)

