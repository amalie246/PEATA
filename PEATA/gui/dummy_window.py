import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)
from PyQt6.QtGui import QIcon, QFontDatabase, QFont

# ───── Widgets ─────
from navbar import Navbar
from about_us import AboutUs

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window icon and title
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.jpg")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle(" Project PEATA | home")
        self.setGeometry(100, 100, 700, 700)

        # ───── Main horizontal layout (left + right) ─────
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        # ───── Left box (navbar) ─────
        self.navbar = Navbar()
        self.navbar.about_clicked.connect(self.show_about_us)  # ✅ connect signal
        main_layout.addWidget(self.navbar)

        # ───── Right box (content) ─────
        self.content_window = QVBoxLayout()
        self.content_window.addWidget(QLineEdit("Right LineEdit 1"))
        self.content_window.addWidget(QLineEdit("Right LineEdit 2"))

        content_container = QWidget()
        content_container.setLayout(self.content_window)
        main_layout.addWidget(content_container)

    def show_about_us(self):
        self.setWindowTitle("Project PEATA | about us")
        # Clear previous widgets
        while self.content_window.count():
            item = self.content_window.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Add AboutUsWidget
        self.content_window.addWidget(AboutUs())


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
        print("ERROR, failed to load font")

    window = Window()
    window.show()
    sys.exit(app.exec())
