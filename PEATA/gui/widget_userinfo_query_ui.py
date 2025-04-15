from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
#from api import TikTokApi
from data_viewer import DataViewer
#from file_converter import FileConverter
from progress_bar import ProgressBar
from common_ui_elements import focus_on_query_value, create_button
import json

# # Replace with actual values or pass dynamically
# CLIENT_KEY = "your_client_key"
# CLIENT_SECRET = "your_client_secret"
# ACCESS_TOKEN = "your_access_token"

# api = TikTokApi(CLIENT_KEY, CLIENT_SECRET, ACCESS_TOKEN)

"""
Todo:
- Consider better file name

UserInfo Query Ui flow   
- Input : Username
- Call Api : get_public_user_info(username)
- Treat result: Print result with JSON on text view
"""

class UserInfoQueryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Info Query")
        self.init_ui()
        self.update_preview() # Show default preview on load

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left panel
        left_panel = QVBoxLayout()
        self.label = QLabel("Enter Username:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(
            "Enter a TikTok username: e.g., lizzo, jxdn, tai_verdes, mxmtoon, chrisudalla, kingxsosa, itsjojosiwa"
)
        self.input_field.textChanged.connect(self.update_preview)

        
        # Live Query Preview
        self.preview_box = QTextEdit()
        self.preview_box.setReadOnly(True)
        self.preview_box.setMinimumHeight(150)
        
        # Buttons
        self.run_button = create_button("Run Query", click_callback=self.run_query)
        self.clear_button = create_button("Clear Query", click_callback=self.clear_all)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.run_button)
        btn_layout.addWidget(self.clear_button)
        
        left_panel.addWidget(self.label)
        left_panel.addWidget(self.input_field)
        left_panel.addWidget(QLabel("Live Query Preview:"))
        left_panel.addWidget(self.preview_box)
        left_panel.addLayout(btn_layout)
        
        # Right panel
        right_panel = QVBoxLayout()
        self.result_box = QTextEdit("Result will show here")
        self.result_box.setReadOnly(True)
        right_panel.addWidget(self.result_box)
        
        main_layout.addLayout(left_panel, 2)
        main_layout.addLayout(right_panel, 3)
        self.setLayout(main_layout)


    def update_preview(self):
        username = self.input_field.text().strip() or "example_user_id"
       
        preview = {
            "query": {
                "and": [
                    {
                        "operation": "EQ",
                        "field_name": "username",
                        "field_values": [username]
                    }
                ]
            },
            "fields": [
                "display_name",
                "bio_description",
                "avatar_url",
                "is_verified",
                "follower_count",
                "following_count",
                "likes_count",
                "video_count"
            ]
        }
        self.preview_box.setPlainText(json.dumps(preview, indent=2))
        
    def run_query(self):
        username = self.input_field.text().strip()
        if not username:
            QMessageBox.warning(self, "Input Error", "Please enter a username.")
            return
        
        info = api.get_public_user_info(username)
        if not info:
            QMessageBox.information(self, "No Results", "No user found.")
            return

        self.result_box.setPlainText(json.dumps(info, indent=2))
    
    def clear_all(self):
       self.input_field.clear()
       self.preview_box.clear()
       self.result_box.setPlainText("Result will show here") 
    
       
# For testing
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = UserInfoQueryUI()
    window.show()
    sys.exit(app.exec())