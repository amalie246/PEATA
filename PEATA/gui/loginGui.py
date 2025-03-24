import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Log in to PEATA - Pachages for Easier Access To APIs")
        
        self.button_is_checked = False
        
        button = QPushButton("Click Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)

        # Set the central widget of the Window.
        self.setCentralWidget(button) # set button in the middle of the widget

    def the_button_was_clicked(self):
        print("Clicked!")
        
    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked # save checked value (True or False)
        
        print(f"Button checked state: {self.button_is_checked}")
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()  # Execution until app terminates.


