# main_window.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

# Header Class

class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        title = QLabel("PEATA Data Processor")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("A tool for analyzing TikTok API data easily")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.setLayout(layout)
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PEATA - Main Window")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the main window!"))
        layout.addWidget(HeaderWidget())
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())