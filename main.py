import sys

from PySide6.QtWidgets import QApplication
from important.event_bus import event_bus
from important.mode_manager import mode_manager
from ui.character_window import CharacterWindow
from ui.thought_bubbles import ThoughtBubbleManager
from ui.windows.note_mode import NotesMode
from ui.windows.sound_mode import SoundMode
from ui.windows.timer_mode import TimerMode


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.character = CharacterWindow()
        self.bubbles = ThoughtBubbleManager()

        event_bus.subscribe("character_clicked", self.toggle_menu)
        event_bus.subscribe("mode_selected", self.activate_mode)

        self.character.show()

    def toggle_menu(self, _=None):
        from important.mode_manager import mode_manager
        if mode_manager.active_mode is not None:
            mode_manager.clear_mode()
            return
        if self.bubbles.bubbles or self.bubbles.connectors:
            self.bubbles.close_all()
        else:
            pos = self.character.pos()
            self.bubbles.open(pos)


    def activate_mode(self, mode_name):
        mode_map = {
            "notes": NotesMode,
            "sound": SoundMode,
            "timer": TimerMode,
        }
        cls = mode_map.get(mode_name)
        if not cls:
            return
        mode_window = cls()
        x = self.character.x() - 260
        y = self.character.y() - 40
        if mode_name == "timer":
            x = self.character.x() - 180
            y = self.character.y() + 60
        mode_window.move(x, y)
        mode_manager.set_mode(mode_window)

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    App().run()
