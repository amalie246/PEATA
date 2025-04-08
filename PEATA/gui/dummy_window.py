import sys
import os

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)
from PyQt6.QtGui import QIcon

# ───── Widgets ─────
from navbar import Navbar

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window icon and title
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.jpg")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle(" Project PEATA")
        self.setGeometry(100, 100, 700, 700)

        # ───── Main horizontal layout (left + right) ─────
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        # ───── Left box (navbar) ─────
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)

        # ───── Right box (content) ─────
        content_window = QVBoxLayout()
        content_window.addWidget(QLineEdit("Right LineEdit 1"))
        content_window.addWidget(QLineEdit("Right LineEdit 2"))
        main_layout.addLayout(content_window)


# FOR TESTING
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ───── Load TikTok Font from Assets ─────
    font_path = os.path.join(os.path.dirname(__file__), "assets", "font_tiktok.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(family, 11))  # Optional: adjust point size
    else:
        print("⚠️ Failed to load font_tiktok.ttf")

    window = Window()
    window.show()
    sys.exit(app.exec())
