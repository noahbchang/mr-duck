from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QHBoxLayout, QLabel, QPushButton, QMenu, QFileDialog
from ui.base_mode_window import BaseModeWindow
import os

class NotesMode(BaseModeWindow):
    def __init__(self):
        from important.mode_manager import mode_manager
        super().__init__()
        layout = QVBoxLayout(self)
        self.editor = QTextEdit()
        self.editor.setStyleSheet("""
                    background-color: rgba(225, 225, 225, 160);   
                    color: rgba(0, 0, 0, 255);                    
                    border-radius: 12px;
                    padding: 8px;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 8px;
                    """)  
        self.editor.setPlainText(mode_manager.notes_text)
        layout.addWidget(self.editor, stretch = 1)

        buttons = QHBoxLayout()
        save_as = QPushButton("Save As")
        save_as.clicked.connect(self.save_as_menu)
        open_file = QPushButton("Open")
        open_file.clicked.connect(self.open_file_menu)
        font_size = QPushButton("Font Size")
        font_size.clicked.connect(self.font_size_menu)

        buttons.addWidget(save_as)
        buttons.addWidget(open_file)
        buttons.addWidget(font_size)

        style = """
            background-color: rgba(225, 225, 225, 160);                      
            border-radius: 12px;
            padding: 8px;
         """
        save_as.setStyleSheet(style)
        open_file.setStyleSheet(style)
        font_size.setStyleSheet(style)
        layout.addLayout(buttons, stretch = 0)

        self.resize(260, 180)


    def closeEvent(self, event):
        from important.mode_manager import mode_manager
        mode_manager.notes_text = self.editor.toPlainText()
        super().closeEvent(event)

    def font_size_menu(self):
        menu = QMenu(self)
        sizes = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
        for size in sizes:
            action = menu.addAction(f"{size} px")
            action.triggered.connect(lambda _, s = size: self.change_font_size(s))
        
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    
    def change_font_size(self, size):
        self.editor.setStyleSheet(f"""
            background-color: rgba(225, 225, 225, 160);   
            color: rgba(0, 0, 0, 255);                    
            border-radius: 12px;
            padding: 8px;
            font-weight: bold;
            font-size: {size}px;
            padding: 8px;
        """)

    def save_as_menu(self):
        note_directory = os.path.join(os.getcwd(), "notes")
        os.makedirs(note_directory, exist_ok=True)
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save As", note_directory, "Text Files (*.txt)"
        )
        if filepath:
            with open(filepath, "w") as f:
                f.write(self.editor.toPlainText())

    def open_file_menu(self):
        note_directory = os.path.join(os.getcwd(), "notes")
        os.makedirs(note_directory, exist_ok=True)
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open File", note_directory, "Text Files (*.txt)"
        )
        if filepath:
            with open(filepath, "r") as f:
                self.editor.setPlainText(f.read())

        
        


