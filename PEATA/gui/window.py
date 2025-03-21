from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv) # Config for OS
    win = QMainWindow()
    win.setGeometry(200, 200, 1024, 768)
    win.setWindowTitle("Project PEATA v0.1")

    win.show()
    sys.exit(app.exec())

window()