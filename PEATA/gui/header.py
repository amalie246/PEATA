import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

# Header Class
class Header(QWidget):
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
        
# For quick test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    header = Header()
    header.show()
    sys.exit(app.exec())