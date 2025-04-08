import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from main_section import MainSection
from header import Header
from footer import Footer

# Main_window.py divided into header.py, main_window.py and footer.py. Might move all balck into main_window.py for simpler code & structure.

       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Icon for window
        #self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("Project PEATA")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout (Important!)
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Add custom sections
        self.header = Header()
        self.main_section = MainSection()
        self.footer = Footer()
        
       
        layout.addWidget(self.header)
        layout.addWidget(self.main_section)
        layout.addWidget(self.footer)
      
        # Apply layout to central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Navigation bar as overlay
        self.navbar = Navbar(self)
        self.navbar.show()
        self.navbar.raise_()  # Only needed if overlapping other widgets


        self.load_stylesheet()
        
    def resizeEvent(self, event):
        self.navbar.setGeometry(0, 0, 200, self.height())
        self.main_section.setGeometry(200, 0, self.width() - 200, self.height())
        return super().resizeEvent(event)

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