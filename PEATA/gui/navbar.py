from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class Navbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # Style
        button_height = 50
        style = """
        QPushButton {
            background-color: #0078d7;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #005a9e;
            font-style: italic;
        }
        QPushButton:pressed {
        background-color: #003f7d;
        padding-left: 12px;  /* Simulate a press-in effect */
        padding-top: 12px;
        }
        """

        # Buttons
        btn_users = QPushButton("USERS")
        btn_users.setFixedHeight(button_height)
        btn_users.setStyleSheet(style)

        btn_videos = QPushButton("VIDEOS")
        btn_videos.setFixedHeight(button_height)
        btn_videos.setStyleSheet(style)

        btn_comments = QPushButton("COMMENTS")
        btn_comments.setFixedHeight(button_height)
        btn_comments.setStyleSheet(style)

        btn_about = QPushButton("ABOUT US")
        btn_about.setFixedHeight(button_height)
        btn_about.setStyleSheet(style)

        # Add to layout
        layout.addWidget(btn_users)
        layout.addWidget(btn_videos)
        layout.addWidget(btn_comments)
        layout.addWidget(btn_about)

        self.setLayout(layout)
        self.setFixedWidth(150)
