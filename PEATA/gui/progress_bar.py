import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar
)

from PyQt5.QtCore import Qt, QTimer

class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Processing Progress")
        self.setGeometry(100, 100, 500, 150)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create progress bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setAlignment(Qt.AlignCenter)

        # Buttons (start, cancle btns)
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Processing")
        self.cancel_button = QPushButton("Cancel")
        
        
        self.start_button.clicked.connect(self.start_processing)
        self.cancel_button.clicked.connect(self.cancel_processing)
        self.cancel_button.setEnabled(False)
  
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)
        
        # Add to layout
        self.layout.addWidget(self.progress)
        self.layout.addLayout(button_layout)
        
        # Timer for simulating processing (Delete later! )
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def start_processing(self):
        self.progress.setValue(0)
        self.timer.start(50)  # update every 50ms
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        
    def cancel_processing(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def update_progress(self):
        current_value = self.progress.value()
        if current_value < 100:
            self.progress.setValue(current_value + 1)
        else:
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.cancle_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBar()
    window.show()
    sys.exit(app.exec_())
