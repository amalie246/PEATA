from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor


class AboutUs(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(30)

        # ───── Title and Intro Message ─────
        title = QLabel("{ About This App }")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        intro = QLabel(
            "PEATA is a Python-based desktop application designed to help users interact with "
            "and explore data collected from social platforms like TikTok. It provides intuitive "
            "query tools and a clean user interface for analysing users, videos, and comments."
        )
        intro.setWordWrap(True)
        intro.setAlignment(Qt.AlignmentFlag.AlignCenter)

        copyright = QLabel("v1.0 © 2025 PEATA Team")

        def create_link(url):
            label = QLabel(f'<a href="{url}">{url}</a>')
            label.setOpenExternalLinks(True)
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            return label

        main_layout.addWidget(title)
        main_layout.addWidget(intro)
        main_layout.addWidget(copyright)

        # ───── Developer List ─────
        dev_form = QFormLayout()
        dev_form.setSpacing(10)
        dev_form.addRow("Ibrahim Khan:", create_link("https://github.com/DR4G0N101"))
        dev_form.addRow("Elin Eunjung Park:", create_link("https://github.com/ElinEunjung"))
        dev_form.addRow("Oda Nøstdahl:", create_link("https://github.com/Odanostdahl"))
        dev_form.addRow("Amalie Nilsen:", create_link("https://github.com/amalie246"))

        main_layout.addLayout(dev_form)

        # ───── How to use ─────
        howto_title = QLabel("{How to use this app}")
        howto_title.setStyleSheet("font-size: 24px; font-weight: bold;")
        howto_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(howto_title)

        self.setLayout(main_layout)