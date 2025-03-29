from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from main_window import MainWindow 

class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("PEATA-login: Enter credentials")
        self.setFixedSize(800, 600)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username = admin")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password = password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)


        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

        

    def check_login(self):
        if self.username_input.text() == "admin" and self.password_input.text() == "password":
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login failed", "Incorrect username or password")

