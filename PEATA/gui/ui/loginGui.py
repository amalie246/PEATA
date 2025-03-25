import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Log in to PEATA - Pachages for Easier Access To APIs")       
        
        self.button = QPushButton("Click Me!")
        
        self.setFixedSize(QSize(400, 300))
        
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        self.button.clicked.connect(self.the_button_was_toggled)

        # Set the central widget of the Window.
        self.setCentralWidget(self.button) # set button in the middle of the widget

    def the_button_was_clicked(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)
        
    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked # save checked value (True or False)
        
        print(f"Button checked state: {self.button_is_checked}")
        
    
      
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()  # Execution until app terminates.


