from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Burger Menu with Top-Left Return Arrow")
        self.setGeometry(100, 100, 800, 600)

        # Burger button (always visible, top-left)
        self.burger_button = QPushButton("☰", self)
        self.burger_button.setGeometry(10, 10, 40, 40)
        self.burger_button.clicked.connect(self.show_menu)

        # Side menu
        self.menu_width = 200
        self.menu = QWidget(self)
        self.menu.setGeometry(-self.menu_width, 0, self.menu_width, self.height())
        self.menu.setStyleSheet("background-color: #333;")

        # Close button inside the menu, positioned manually
        self.close_button = QPushButton("←", self.menu)
        self.close_button.setGeometry(10, 10, 40, 40)
        self.close_button.setStyleSheet("background-color: white;")
        self.close_button.clicked.connect(self.hide_menu)

        self.menu_visible = False

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
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(start_x, 0, self.menu_width, self.height()))
        self.anim.setEndValue(QRect(end_x, 0, self.menu_width, self.height()))
        self.anim.start()

        self.menu_visible = show

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
