import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow



# Exteral stylesheet (QSS-file)
def load_stylesheet(path):
    with open(path, "r") as file:
        return file.read()
      
def main():
    app = QApplication(sys.argv)
    
    stylesheet = load_stylesheet("style.qss")
    app.setStyleSheet(stylesheet)
    
    # Create and show login window
    login = LoginWindow(on_login_success=lambda: None)
    login.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()