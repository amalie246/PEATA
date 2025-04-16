from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QCheckBox, QComboBox
# from api import TikTokApi
# from data_viewer import DataViewer
# from FileProcessor import FileProcessor
from progress_bar import ProgressBar
from common_ui_elements import focus_on_query_value, create_button, create_scrollable_area, create_labeled_input
import json

# # Replace with actual values or pass dynamically
# CLIENT_KEY = "your_client_key"
# CLIENT_SECRET = "your_client_secret"
# ACCESS_TOKEN = "your_access_token"

# api = TikTokApi(CLIENT_KEY, CLIENT_SECRET, ACCESS_TOKEN)

"""
TODO:
- Test Max Result option

Comment query ui work flow

- Input: Video ID
- Call API: get_video_comments(video_id) + Progress bar 
- Treat result: save CSV, show comments in the view
- Additional: show result with DataViewer
"""

class CommentQueryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comment Query")
        self.init_ui()
        self.update_preview()  # Show default preview on load

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left panel
        left_panel = QVBoxLayout()
        self.input_field = QLineEdit()      
        self.input_field.setPlaceholderText("Enter a TikTok Video ID (e.g., 702874395068494965)")
        self.input_field.textChanged.connect(self.update_preview)
        
        # Give user hint (style added in style.qss)
        self.helper_label = QLabel(
        "Example URL: https://www.tiktok.com/@username/video/702874395068494965\n"
        "→ Copy only the last number as Video ID: 702874395068494965"
        )
        self.helper_label.setObjectName("HelperLabel")
        self.helper_label.setWordWrap(True)

        # Live Query Preview
        self.preview_box = QTextEdit()
        self.preview_box.setReadOnly(True)
        self.preview_box.setMinimumHeight(150)
        preview_area = create_scrollable_area(self.preview_box)

        # Buttons
        self.run_button = create_button("Run Query", click_callback=self.run_query)
        self.clear_button = create_button("Clear Query", click_callback=self.clear_all)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.run_button)
        btn_layout.addWidget(self.clear_button)
        
        # Max results option
        self.max_results_selector = QComboBox()
        self.max_results_selector.addItems(["100", "500", "1000", "ALL"])
        self.max_results_selector.setCurrentText("500")
        self.over_limit_warning_checkbox = QCheckBox("Warn if result count exceeds 1000")
        self.over_limit_warning_checkbox.setChecked(True)
        self.over_limit_warning_checkbox.setToolTip("Disable this if you want to skip warnings for large requests (over 1000 results).")

        left_panel.addWidget(create_labeled_input("Enter Video ID:", self.input_field))
        left_panel.addWidget(self.helper_label)
        left_panel.addWidget(QLabel("Live Query Preview:"))
        left_panel.addWidget(preview_area)
        left_panel.addWidget(create_labeled_input("Max Results:", self.max_results_selector))
        left_panel.addWidget(self.over_limit_warning_checkbox)
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
        video_id = self.input_field.text().strip() or "example_video_id"
       
        preview = {
            "query": {
               "and": [
                   {
                       "operation": "EQ",
                       "field_name": "video_id",
                       "field_values": [video_id]
                   }
               ]
           }
        }
        self.preview_box.setPlainText(json.dumps(preview, indent=2))
        focus_on_query_value(self.preview_box, video_id)

    def run_query(self):
        video_id = self.input_field.text().strip()
        if not video_id:
            QMessageBox.warning(self, "Input Error", "Please enter a Video ID.")
            return
        
        selected_text = self.max_results_selector.currentText()
        limit = None if selected_text == "ALL" else int(selected_text)       
        max_allowed = 2000 
        if limit is None:
            limit = max_allowed
            
# Note: TikTok API may allow larger values.
# This 2000 is a tentative upper bound based on similar endpoints.

        if limit and limit > 1000 and self.over_limit_warning_checkbox.isChecked():
            QMessageBox.warning(self, "Warning", "You are requesting more than 1000 comments. This may take time and could hit rate limits.")
        
        self.setWindowOpacity(0.3) # UI dim effect

        def fetch_comments():
            return api.get_video_comments(video_id, limit=limit)
        
        def after_fetch(comments):
            self.setWindowOpacity(1.0) # restore full opacity
            if not comments:
                QMessageBox.information(self, "No Results", "No comments found.")
                return

            FileProcessor().save_json_to_csv(comments, "comments_result.csv")
            self.result_box.setPlainText(f"{len(comments)} comments fetched and saved.")   
            self.viewer = DataViewer()
            self.viewer.show()
        
        ProgressBar.run_with_progress(self, fetch_comments, after_fetch)
        
    def clear_all(self):
       self.input_field.clear()
       self.preview_box.clear()
       self.result_box.setPlainText("Result will show here")
        
# For testing
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = CommentQueryUI()
    window.show()
    sys.exit(app.exec())
