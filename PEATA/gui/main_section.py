import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton
from PyQt5.QtCore import Qt
<<<<<<< Updated upstream
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
=======
from progress_bar import ProgressBar
>>>>>>> Stashed changes

# Main Content Class
class MainSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Placeholder for now
        content = QLabel("Main content goes here (file viewer, search bar, etc.)")
        content.setAlignment(Qt.AlignCenter)
        layout.addWidget(content)

        button = QPushButton()
        button.setIcon(QIcon("assets/icon_video.svg"))
        
        self.progressBar = ProgressBar()        
        layout.addWidget(self.progressBar)
        
        self.setLayout(layout)