import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
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
      
# Main Content Class
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Placeholder for now
        content = QLabel("Main content goes here (file viewer, search bar, etc.)")
        content.setAlignment(Qt.AlignCenter)
        layout.addWidget(content)
        
        self.setLayout(layout)

# Footer Class
class FooterWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        
        copyright_label = QLabel("© 2025 PEATA Team")
        copyright_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(copyright_label)
        self.setLayout(layout)
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PEATA - Main Window")
        self.setGeometry(100, 100, 1200, 800)

        layout = QVBoxLayout()

        layout.addWidget(HeaderWidget())
        layout.addWidget(MainWidget())
        layout.addWidget(FooterWidget())
        self.setLayout(layout)
        
        self.load_stylesheet()
        
    def load_stylesheet(self):
        try:
            with open("style.qss", "r") as file:
                self.setStyleSheet(file.read())
        except:
            print("style.qss not found")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())