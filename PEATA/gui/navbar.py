import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt

class Navbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # ───── Style and Paths ─────
        button_height = 70
        icon_size = QSize(32, 32)
        icon_path = lambda name: os.path.join(os.path.dirname(__file__), "assets", f"{name}.svg")

        style = """
        QToolButton {
            background-color: #0078d7;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }

        QToolButton:hover {
            background-color: #005a9e;
            font-style: italic;
        }

        QToolButton:pressed {
            background-color: #003f7d;
        }
        """

        def create_button(label, icon_file):
            btn = QToolButton()
            btn.setText(label)
            btn.setIcon(QIcon(icon_path(icon_file)))
            btn.setIconSize(icon_size)
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setFixedHeight(button_height)
            btn.setStyleSheet(style)
            return btn

        # ───── Buttons ─────
        layout.addWidget(create_button("USERS", "icon_user"))
        layout.addWidget(create_button("VIDEOS", "icon_video"))
        layout.addWidget(create_button("COMMENTS", "icon_comments"))
        layout.addWidget(create_button("ABOUT US", "icon_info"))

        self.setLayout(layout)
        self.setFixedWidth(150)
