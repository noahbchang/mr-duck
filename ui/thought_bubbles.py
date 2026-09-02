import math
import random

from PySide6.QtCore import Qt, QTimer, QPoint, Property, QPropertyAnimation
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QWidget

from important.event_bus import event_bus
OPTIONS = [
    ("notes", "assets/notescloud.png"),
    ("sound", "assets/soundcloud.png"),
    ("timer", "assets/clockcloud.png"),
]
class ThoughtBubble(QWidget):
    def __init__(self, mode_name, bubble_path, base_pos):
        super().__init__()
        self.setAttribute(Qt.WA_Hover)  

        self.mode_name = mode_name
        self.base_pos = base_pos
        self.phase = random.uniform(0, math.pi * 2)
        self.t = 0.0
        self._scale = 0.3
        self.wobble_offset = 0


        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.bubble_pix = QPixmap(bubble_path).scaled(
            140, 110,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.resize(200, 200)
        self.move(base_pos)
        self.start_pop_animation()
        self.start_wobble()

    def start_pop_animation(self):
        self.setWindowOpacity(0.0)

        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(250)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)
        self.opacity_anim.start()

        self.scale_anim = QPropertyAnimation(self, b"scale")
        self.scale_anim.setDuration(300)
        self.scale_anim.setStartValue(0.3)
        self.scale_anim.setKeyValueAt(0.7, 1.05)
        self.scale_anim.setEndValue(1.0)
        self.scale_anim.start()

    def start_wobble(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.t += 0.05
        self.wobble_offset = math.sin(self.t + self.phase) * 4
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(0, self.wobble_offset)   
        painter.scale(self._scale, self._scale)
        painter.drawPixmap(15, 15, self.bubble_pix)


    def getScale(self):
        return self._scale

    def setScale(self, value):
        self._scale = value
        self.update()

    scale = Property(float, getScale, setScale)
    
    def mousePressEvent(self, event):
        event_bus.emit("mode_selected", self.mode_name)
        event_bus.emit("close_bubbles")
        self.close()

class ConnectorBubble(QWidget):
    def __init__(self, bubble_path, base_pos):
        super().__init__()
        self.setAttribute(Qt.WA_Hover)  
        self.base_pos = base_pos
        self.phase = random.uniform(0, math.pi * 2)
        self.t = 0.0
        self._scale = 0.3
        self.wobble_offset = 0

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.bubble_pix = QPixmap(bubble_path).scaled(
            32, 32,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.resize(40, 40)
        self.move(base_pos)
        self.start_pop_animation()
        self.start_wobble()

    def start_pop_animation(self):

        self.setWindowOpacity(0.0)

        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(250)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)
        self.opacity_anim.start()

        self.scale_anim = QPropertyAnimation(self, b"scale")
        self.scale_anim.setDuration(300)
        self.scale_anim.setStartValue(0.3)
        self.scale_anim.setKeyValueAt(0.7, 1.05)
        self.scale_anim.setEndValue(1.0)
        self.scale_anim.start()

    def start_wobble(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.t += 0.05
        self.wobble_offset = math.sin(self.t + self.phase) * 4
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(0, self.wobble_offset)   
        painter.scale(self._scale, self._scale)
        painter.drawPixmap(4, 4, self.bubble_pix)

    def getScale(self):
        return self._scale

    def setScale(self, value):
        self._scale = value
        self.update()

    scale = Property(float, getScale, setScale)

class ThoughtBubbleManager:
    def __init__(self):
        self.bubbles = []
        self.connectors = []

        event_bus.subscribe("close_bubbles", self.close_all)

    def open(self, assistant_pos):
        self.close_all()

        ax, ay = assistant_pos.x(), assistant_pos.y()

        # big bubbles cluster above head
        bubble_positions = [
            QPoint(ax - 120, ay - 140),
            QPoint(ax - 40 , ay - 200),
            QPoint(ax + 40, ay - 165),
        ]

        connector_positions = [
            QPoint(ax + 50, ay - 50),
            QPoint(ax + 30, ay - 80),
        ]

        # connector bubbles (decorative)
        connector_paths = [
            "assets/small_cloud.png",
            "assets/small_cloud.png",
        ]

        for pos, path in zip(connector_positions, connector_paths):
            c = ConnectorBubble(path, pos)
            c.show()
            self.connectors.append(c)

        # menu bubbles
        for (mode_name, bubble_path), pos in zip(OPTIONS, bubble_positions):
            b = ThoughtBubble(mode_name, bubble_path, pos)
            b.show()
            self.bubbles.append(b)

    def close_all(self, _=None):
        for b in self.bubbles:
            b.close()
        for c in self.connectors:
            c.close()
        self.bubbles.clear()
        self.connectors.clear()
