from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt6.QtGui import QIcon
import sys

class Window(QWidget):
    def __init___(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("dummy window")
        self.setContentsMargin(20, 20, 20, 20)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())