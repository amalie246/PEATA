# main_window.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PEATA - Main Window")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the main window!"))
        self.setLayout(layout)
