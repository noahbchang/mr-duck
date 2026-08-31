from PySide6.QtWidgets import QVBoxLayout, QTextEdit
from ui.base_mode_window import BaseModeWindow




class NotesMode(BaseModeWindow):
    def __init__(self):
        from important.mode_manager import mode_manager
        self.editor = QTextEdit()
        self.editor.setPlainText(mode_manager.notes_text)  
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)
        self.resize(260, 180)
        self.editor.setStyleSheet("""
            background-color: rgba(255, 255, 255, 160);   
            color: rgba(0, 0, 0, 255);                    
            border-radius: 12px;
            padding: 8px;
            font-weight: bold;
            font-size: 15px;
            padding: 8px;
            """)

    def closeEvent(self, event):
        from important.mode_manager import mode_manager
        mode_manager.notes_text = self.editor.toPlainText()
        super().closeEvent(event)


