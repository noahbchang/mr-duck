from PySide6.QtWidgets import QVBoxLayout, QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from ui.base_mode_window import BaseModeWindow
import ctypes


# Windows media key codes
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1

def send_media_key(vk_code):
    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)


class SoundMode(BaseModeWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.button_style = """
            font-size: 22px;
            background-color: rgba(255, 255, 255, 160);
            border-radius: 10px;
            padding: 6px;
        """
        btn_prev = QPushButton("⏮️")
        btn_pause = QPushButton("▶️")
        btn_next = QPushButton("⏭️")

        btn_prev.setStyleSheet(self.button_style)
        btn_pause.setStyleSheet(self.button_style)
        btn_next.setStyleSheet(self.button_style)

        layout.addWidget(btn_prev)
        layout.addWidget(btn_pause)
        layout.addWidget(btn_next)
        btn_prev.clicked.connect(lambda: (self.animate_press(btn_prev), send_media_key(VK_MEDIA_PREV_TRACK)))
        btn_pause.clicked.connect(lambda: (self.animate_press(btn_pause), send_media_key(VK_MEDIA_PLAY_PAUSE)))
        btn_next.clicked.connect(lambda: (self.animate_press(btn_next), send_media_key(VK_MEDIA_NEXT_TRACK)))

        self.resize(260, 200)

    def animate_press(self, button):
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(80)
        r = button.geometry()
        anim.setStartValue(r)
        anim.setEndValue(r.adjusted(-2, -2, 2, 2))
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()
