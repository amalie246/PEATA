import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtGui import QIcon

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window icon and title
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.jpg")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Dummy Window")
        self.setGeometry(100, 100, 700, 700)

        # ───── Main horizontal layout (left + right) ─────
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setStretch(0,0)
        main_layout.setStretch(1,1)

        # ───── Left box (navbar) ─────
        navbar = QVBoxLayout()
        navbar.addWidget(QPushButton("USERS"))
        navbar.addWidget(QPushButton("VIDEOS"))
        navbar.addWidget(QPushButton("COMMENTS"))
        main_layout.addLayout(navbar)

        # ───── Right box (content) ─────
        content_window = QVBoxLayout()
        content_window.addWidget(QLineEdit("Right LineEdit 1"))
        content_window.addWidget(QLineEdit("Right LineEdit 2"))
        main_layout.addLayout(content_window)


# FOR TESTING
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
