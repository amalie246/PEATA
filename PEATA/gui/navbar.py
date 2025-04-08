from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt

class Navbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Fixed width for sidebar
        self.menu_width = 200

        if parent:
            self.setGeometry(0, 0, self.menu_width, parent.height())

        # Set background color (or use style.qss later)
        self.setStyleSheet("background-color: #333;")

        # Example button (←) inside navbar
        self.close_button = QPushButton("←", self)
        self.close_button.setGeometry(20, 20, 100, 100)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)

    def resizeEvent(self, event):
        """Keep the navbar height in sync with parent window."""
        if self.parent():
            self.setGeometry(0, 0, self.menu_width, self.parent().height())
        return super().resizeEvent(event)
