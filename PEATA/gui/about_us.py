from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor


class AboutUs(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(30)

        # ───── Title and Message ─────
        title = QLabel("About This App")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        thank_you = QLabel("Thank you for using this application!")
        thank_you.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(title)
        main_layout.addWidget(thank_you)

        # ───── Developer List ─────
        dev_form = QFormLayout()
        dev_form.setSpacing(10)

        def create_link(url):
            label = QLabel(f'<a href="{url}">{url}</a>')
            label.setOpenExternalLinks(True)
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            return label

        dev_form.addRow("Ibrahim Khan:", create_link("https://github.com/DR4G0N101"))
        dev_form.addRow("Elin Eunjung Park:", create_link("https://github.com/ElinEunjung"))
        dev_form.addRow("Oda Nøstdahl:", create_link("https://github.com/Odanostdahl"))
        dev_form.addRow("Amalie Nilsen:", create_link("https://github.com/amalie246"))

        main_layout.addLayout(dev_form)

        self.setLayout(main_layout)
