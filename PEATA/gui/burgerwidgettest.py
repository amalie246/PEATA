from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Responsive Burger Menu")
        self.setGeometry(100, 100, 800, 600)

        # Burger button (larger size at top-left)
        self.burger_button = QPushButton("☰", self)
        self.burger_button.setGeometry(20, 20, 100, 100)
        self.burger_button.setStyleSheet("""
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
        self.burger_button.clicked.connect(self.show_menu)

        # Side menu
        self.menu_width = 200
        self.menu = QWidget(self)
        self.menu.setStyleSheet("background-color: #333;")

        # Close/return button inside the menu (also large)
        self.close_button = QPushButton("←", self.menu)
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
        self.close_button.clicked.connect(self.hide_menu)

        # Initial position
        self.menu_visible = False
        self.update_menu_geometry(initial=True)

    def update_menu_geometry(self, initial=False):
        x = 0 if self.menu_visible else -self.menu_width
        self.menu.setGeometry(x, 0, self.menu_width, self.height())
        if initial:
            self.menu.move(-self.menu_width, 0)

    def resizeEvent(self, event):
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
        self.anim.setDuration(100)  # 💨 Fast animation
        self.anim.setStartValue(QRect(start_x, 0, self.menu_width, self.height()))
        self.anim.setEndValue(QRect(end_x, 0, self.menu_width, self.height()))
        self.anim.start()

        self.menu_visible = show

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
