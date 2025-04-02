import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar
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

        # Create button to start processing
        self.button = QPushButton("Start Processing")
        self.button.clicked.connect(self.start_processing)

        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.button)

        # Timer for simulating processing (Delete later! )
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def start_processing(self):
        self.progress.setValue(0)
        self.timer.start(50)  # update every 50ms

    def update_progress(self):
        current_value = self.progress.value()
        if current_value < 100:
            self.progress.setValue(current_value + 1)
        else:
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBar()
    window.show()
    sys.exit(app.exec_())
