# login_widget.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QFormLayout, QMessageBox, QHBoxLayout
)

class LoginWidget(QWidget):
    def __init__(self, on_login_success_callback):
        super().__init__()
        self.on_login_success = on_login_success_callback

        # ───── Form Fields ─────
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Client ID = id")

        self.client_key_input = QLineEdit()
        self.client_key_input.setPlaceholderText("Client Key = key")
        self.client_key_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("Client Secret = secret")
        self.client_secret_input.setEchoMode(QLineEdit.EchoMode.Password)

        # ───── Buttons ─────
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        # ───── Form Layout ─────
        form_layout = QFormLayout()
        form_layout.addRow("Client ID", self.client_id_input)
        form_layout.addRow("Client Key", self.client_key_input)
        form_layout.addRow("Client Secret", self.client_secret_input)

        # ───── Button Row Layout ─────
        button_row = QHBoxLayout()
        button_row.addWidget(self.login_button)
        button_row.addWidget(self.exit_button)

        form_layout.addRow(button_row)
        self.setLayout(form_layout)

    def check_login(self):
        if (
            self.client_id_input.text() == "id"
            and self.client_key_input.text() == "key"
            and self.client_secret_input.text() == "secret"
        ):
            self.on_login_success()  # Call back to main window
        else:
            QMessageBox.warning(self, "Login failed", "Incorrect username or password")