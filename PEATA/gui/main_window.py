import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from header import Header
from widget_navbar import WidgetNavbar

from main_section import MainSection
from footer import Footer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PEATA project")
        self.setGeometry(100, 100, 1200, 800)
        
        # Navigation bar
        self.navbar = WidgetNavbar(self)
        self.navbar.setGeometry(0, 0, self.width(), self.height())
        self.navbar.show()


        # Create central widget and layout (Important!)
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        
        self.load_stylesheet()
        
    def load_stylesheet(self):
        try:
            with open("style.qss", "r") as file:
                self.setStyleSheet(file.read())
        except:
            print("style.qss not found")

# for testing

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())