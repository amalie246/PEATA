from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import QPropertyAnimation, QRect

class WidgetNavbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set initial geometry based on parent's current size
        if parent:
            self.setGeometry(0, 0, parent.width(), parent.height())

        # Burger button (top-left)
        self.burger_button = QPushButton("☰", self)
        self.burger_button.setGeometry(20, 20, 100, 100)
        self.burger_button.clicked.connect(self.show_menu)

        # Side menu panel
        self.menu_width = 200
        self.menu = QWidget(self)
        self.menu.setStyleSheet("background-color: #333;")

        # Close button inside menu
        self.close_button = QPushButton("←", self.menu)
        self.close_button.setGeometry(20, 20, 100, 100)
        # NB: Let this QSS style be, the global values don't work here
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
        self.close_button.clicked.connect(self.hide_menu)

        self.menu_visible = False
        self.update_menu_geometry()

    def update_menu_geometry(self):
        """Adjust side menu position and height."""
        x = 0 if self.menu_visible else -self.menu_width
        self.menu.setGeometry(x, 0, self.menu_width, self.height())

    def resizeEvent(self, event):
        """Update navbar to match parent size when main window resizes."""
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.update_menu_geometry()
        return super().resizeEvent(event)

    def show_menu(self):
        if not self.menu_visible:
            self.animate_menu(show=True)

    def hide_menu(self):
        if self.menu_visible:
            self.animate_menu(show=False)

    def animate_menu(self, show=True):
        start_x = -self.menu_width if show else 0
        end_x = 0 if show else -self.menu_width

        self.anim = QPropertyAnimation(self.menu, b"geometry")
        self.anim.setDuration(100)
        self.anim.setStartValue(QRect(start_x, 0, self.menu_width, self.height()))
        self.anim.setEndValue(QRect(end_x, 0, self.menu_width, self.height()))
        self.anim.start()

        self.menu_visible = show
