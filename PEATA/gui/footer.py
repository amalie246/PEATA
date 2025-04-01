import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

# Footer Class
class Footer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Horizontal line
        line = QFrame()
        line.setObjectName("footerLine")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Sub-layout just for lablels (vertical)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        
        
        copyright_label = QLabel("© 2025 PEATA Team")
        copyright_label.setObjectName("copyrightLabel")
        welcome_label = QLabel("Welcome to PEATA")
        welcome_label.setObjectName("welcomeLabel")
        
        # Center align
        copyright_label.setAlignment(Qt.AlignCenter)
        welcome_label.setAlignment(Qt.AlignCenter)
        
        text_layout.addWidget(copyright_label)
        text_layout.addWidget(welcome_label)
        
        
        layout.addLayout(text_layout)      
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(5)

        self.setLayout(layout)