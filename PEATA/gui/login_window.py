from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("PEATA-login: Enter credentials")
        self.setFixedSize(800, 600)

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Client ID = id")

        self.client_key_input = QLineEdit()
        self.client_key_input.setPlaceholderText("Client Key = key")
        self.client_key_input.setEchoMode(QLineEdit.Password)
        
        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("Client Secret = secret")
        self.client_secret_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)


        layout = QVBoxLayout()
        layout.addWidget(QLabel("Client ID"))
        layout.addWidget(self.client_id_input)
        layout.addWidget(QLabel("Client Key"))
        layout.addWidget(self.client_key_input)
        layout.addWidget(QLabel("Client Secret"))
        layout.addWidget(self.client_secret_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)
 
    def check_login(self):
        if self.client_id_input.text() == "id" and self.client_key_input.text() == "key" and            self.client_secret_input.text() == "secret":
            self.go_to_main()
        else:
            QMessageBox.warning(self, "Login failed", "Incorrect username or password")

    def go_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()  
        
