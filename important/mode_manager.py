class ModeManager:
    def __init__(self):
        self.active_mode = None
        self.notes_text = ""
    def set_mode(self, mode_window):
        if self.active_mode:
            self.active_mode.close()
        self.active_mode = mode_window
        self.active_mode.show()

    def clear_mode(self):
        if self.active_mode:
            self.active_mode.close()
        self.active_mode = None


mode_manager = ModeManager()
