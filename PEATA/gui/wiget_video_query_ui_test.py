# from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QComboBox, QTabWidget
)
from common_ui_elements import (
    create_date_range_widget, create_field_checkbox_group,
    create_progress_bar, create_result_table,
    create_collapsible_section, create_labeled_input,
    create_checkbox_with_tooltip, create_button,
    create_field_group_with_emojis, create_enum_checkbox_group, 
    create_numeric_filter_group, create_horizontal_line
)
from region_codes import REGION_CODES

class VideoQueryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Query Builder")
        
        # self.logic_ops = {
        #     "AND (All must match)": "and",
        #     "OR (Any can match)": "or",
        #     "NOT (Exclude)": "not"
        # }
        
        self.condition_ops = {
            "Equals": "EQ",
            "Greater than": "GT",
            "Greater or equal": "GTE",
            "Less than": "LT",
            "Less or equal": "LTE"
        }

        self.region_codes = REGION_CODES
        self.init_ui()
    
    def init_ui(self):           
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        self.field_tab = self.create_field_selection_tab()
        self.filter_tab = self.create_filter_tab()
        
        self.tabs.addTab(self.field_tab, "Fields")
        self.tabs.addTab(self.filter_tab, "Filters")
        
        self.query_preview = QTextEdit()
        self.query_preview.setReadOnly(True)
        self.run_button = create_button("Run Query", click_callback = self.run_query)
        self.clear_button = create_button("Clear Query", click_callback = self.clear_query)
        
        main_layout.addWidget(self.tabs)
        
        # Add buttons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.run_button)
        btn_layout.addWidget(self.clear_button)
        main_layout.addLayout(btn_layout)
        
        main_layout.addWidget(QLabel("Generated Query Preview"))
        main_layout.addWidget(self.query_preview)
        self.setLayout(main_layout)

    def create_field_selection_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        MAIN_FIELDS = {
            "username": ("\U0001F464", "Creator's name"),
            "create_time": ("\U0001F552", "Video post time"),
            "view_count": ("\U0001F441\uFE0F", "Views"),
            "like_count": ("\u2764\uFE0F", "Likes"),
            "comment_count": ("\U0001F4AC", "Comments"),
            "share_count": ("\U0001F501", "Shares"),
            "video_description": ("\U0001F4DD", "Caption"),
            "region_code": ("\U0001F30D", "Country code")
        }
        
        ADVANCED_FIELDS = {
            "music_id": ("\U0001F3B5", "Music used in the video"),
            "is_stem_verified": ("\U0001F9EA", "STEM verified"),
            "effect_ids": ("\U0001F57A", "Effect IDs"),
            "hashtag_names": ("\U0001F3F7\uFE0F", "Hashtags"),
            "video_label": ("\U0001F4CB", "Video tags"),
            "video_duration": ("\u23F1\uFE0F", "Duration (sec)"),
            "favourites_count": ("\u2B50", "Favorites count"),
            "video_mention_list": ("\U0001F465", "Mentioned users"),
            "playlist_id": ("\U0001F4D6", "Playlist ID")
        }
        
        
        self.main_checkboxes = {}
        self.advanced_checkboxes = {}
        
        layout.addWidget(create_field_group_with_emojis("Main Fields", MAIN_FIELDS, self.main_checkboxes))
        adv_group = create_field_group_with_emojis("", ADVANCED_FIELDS, self.advanced_checkboxes)
        layout.addWidget(create_collapsible_section("Advanced Fields", adv_group))
   
        tab.setLayout(layout)
        return tab
            
    def create_filter_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 1. Username
        self.username_input = QLineEdit()
        layout.addWidget(create_labeled_input("Username(s) (comma-separated):", self.username_input))
    
        # 2. Keyword
        self.keyword_input = QLineEdit()
        layout.addWidget(create_labeled_input("Keywords (comma-separated):", self.keyword_input))
    
        # 3. Hashtag
        self.hashtag_input = QLineEdit()
        layout.addWidget(create_labeled_input("Hashtags (comma-separated):", self.hashtag_input))
    
        # 4. Date Range
        self.date_widget, self.start_date, self.end_date = create_date_range_widget()
        layout.addWidget(self.date_widget)
        
        # Horizontal Line before numeric filters
        layout.addWidget(create_horizontal_line())
    
        # 5. Numeric Filters
        self.numeric_fields = ["like_count", "view_count", "comment_count", "share_count"]
        layout.addWidget(QLabel("Numeric Filters:"))
        numeric_widget, self.numeric_inputs = create_numeric_filter_group(self.numeric_fields, list(self.condition_ops.keys()), default_op = "Greater than")
        layout.addWidget(numeric_widget)
    
        # Horizontal Line after numeric filters
        layout.addWidget(create_horizontal_line())
        
        # 6. Video Length
        length_group, self.length_checkboxes = create_enum_checkbox_group("Video Length", ["SHORT", "MID", "LONG", "EXTRA_LONG"])
        layout.addWidget(length_group)
    
        # 7. Music ID
        self.music_input = QLineEdit()
        layout.addWidget(create_labeled_input("Music IDs (comma-separated):", self.music_input))
    
        # 8. Effect ID
        self.effect_input = QLineEdit()
        layout.addWidget(create_labeled_input("Effect IDs (comma-separated):", self.effect_input))

      
        tab.setLayout(layout)
        return tab

    def run_query(self):
        import json
        included_fields = [f for f, cb in self.main_checkboxes.items() if cb.isChecked()] + \
                          [f for f, cb in self.advanced_checkboxes.items() if cb.isChecked()]

        conditions = []
        add_condition = lambda f, vals: conditions.append({
       "field_name": f, "operation": "IN", "field_values": vals
   }) if vals else None
        
        # logic_op = self.logic_ops[self.logic_selector.currentText()]
        # add_condition = lambda f, vals: conditions.append({
        #     "field_name": f, "operation": "IN", "field_values": vals
        # }) if vals else None
        
        # -------------Add by order------------------
        add_condition("username", [s.strip() for s in self.username_input.text().split(',') if s.strip()])
        add_condition("keyword", [s.strip() for s in self.keyword_input.text().split(',') if s.strip()])
        add_condition("hashtag_name", [s.strip() for s in self.hashtag_input.text().split(',') if s.strip()])
    
        for field, (spinbox, combo) in self.numeric_inputs.items():
            val = spinbox.value()
            op = combo.currentText()
            if val > 0:
                conditions.append({
                    "field_name": field,
                    "operation": op,
                    "field_values": [str(val)]
                })
    
        selected_lengths = [k for k, cb in self.length_checkboxes.items() if cb.isChecked()]
        add_condition("video_length", selected_lengths)
    
        add_condition("music_id", [s.strip() for s in self.music_input.text().split(',') if s.strip()])
        add_condition("effect_id", [s.strip() for s in self.effect_input.text().split(',') if s.strip()])
    
        query = {
            "fields": included_fields,
            "query": {"and": conditions},
            "start_date": self.start_date.date().toString("yyyyMMdd"),
            "end_date": self.end_date.date().toString("yyyyMMdd")
        }
        self.query_preview.setPlainText(json.dumps(query, indent=2))
        
    def clear_query(self):
        # Clear QLineEdit fields
        self.username_input.clear()
        self.keyword_input.clear()
        self.hashtag_input.clear()
        self.music_input.clear()
        self.effect_input.clear()  
        
        # Reset data pickers
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.end_date.setDate(QDate.currentDate())

        # Uncheck advanced field checkboxes only
        for field, cb in self.main_checkboxes.items():
            cb.setChecked(True)
        for cb in self.advanced_checkboxes.values():
            cb.setChecked(False)
        for cb in self.length_checkboxes.values():
            cb.setChecked(False)
    
        # Reset numeric filters
        for spinbox, combo in self.numeric_inputs.values():
            spinbox.setValue(0)
            combo.setCurrentText("Greater than")  # default value

        # Clear preview
        self.query_preview.clear()


# For testing
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = VideoQueryUI()
    window.show()
    sys.exit(app.exec())
