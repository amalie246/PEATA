from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class AboutUs(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(20)

        # ───── Header ─────
        header = QLabel("Project PEATA")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ───── About the app ─────
        about_us = QLabel("Thank you for using this application!")
        about_us.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ───── Author and link ─────
        author = QLabel("Created by: Ibrahim")
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ───── GitHub Link ─────
        github = QLabel('<a href="https://github.com/yourusername">Visit GitHub Repository</a>')
        github.setOpenExternalLinks(True)
        github.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # ───── Add All to Layout ─────
        layout.addWidget(header)
        layout.addWidget(about_us)
        layout.addWidget(author)
        layout.addWidget(github)

        # Optional Spacer
        layout.addSpacerItem(QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)
