from PySide6.QtWidgets import QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt
from ui.base_mode_window import BaseModeWindow
from controllers.sound_controller import sound_controller


class SoundMode(BaseModeWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.label = QLabel("Master volume")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.on_change)

        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        self.resize(260, 120)

    def on_change(self, value):
        sound_controller.set_volume(value / 100.0)
