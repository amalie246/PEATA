# from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QComboBox, QTabWidget, QMessageBox
    )
from common_ui_elements import (
    create_date_range_widget, create_field_checkbox_group,
    create_progress_bar, create_result_table,
    create_collapsible_section, create_labeled_input,
    create_checkbox_with_tooltip, create_button,
    create_field_group_with_emojis, create_enum_checkbox_group, 
    create_numeric_filter_group, create_horizontal_line,
    create_scrollable_area, focus_on_query_value,
    create_multi_select_input_with_labels
    )
from region_codes import REGION_CODES
from progress_bar import ProgressBar
# from api import TikTokApi
# from file_converter import FileConverter
# from data_viewer import DataViewer
import json

""" TODO
Top Priorities
- run_query() -> TiktokApi.get_video_by_dynamic_query_body() + progress_bar.py
- download button
- Show result -> file_converter.save_jason_to_csv()
-  After saving -> progress_bar, data_viewer
- Consider Pagination (Max 100 video)

Others
- Add operation parameter in query (not, or)
- Fix Tooltip for Music ID (do broad search include Music IDs)
- Add placeholder text in the input field
- Work with Live Query Preview - update query preview()


"""

class VideoQueryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Query Builder")
        self.region_codes = REGION_CODES
        
        # # Replace with actual credentials in real usage
        # self.api = TikTokApi("your_client_key", "your_client_secret", "your_access_token")
        
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

        
        
        self.init_ui()
    
    def init_ui(self):           
        main_layout = QHBoxLayout()
        
        # Left panel : Tabs + Run/Clear buttons
        left_panel = QVBoxLayout()
        self.tabs = QTabWidget()
        left_panel.addWidget(self.tabs)
        
        self.field_tab = self.create_field_selection_tab()
        self.filter_tab = self.create_filter_tab()
        
        self.tabs.addTab(self.field_tab, "Fields")
        self.tabs.addTab(self.filter_tab, "Filters")
        
        
        self.run_button = create_button("Run Query", click_callback = self.run_query)
        self.clear_button = create_button("Clear Query", click_callback = self.clear_query)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.run_button)
        btn_layout.addWidget(self.clear_button)
        left_panel.addLayout(btn_layout)
        
        # Right panel: Scrollable Query Preview
        right_panel = QVBoxLayout()        
        right_panel.addWidget(QLabel("Live Query Preview"))
        
        self.query_preview = QTextEdit()
        self.query_preview.setReadOnly(True)
        self.query_preview.setMinimumHeight(200)
        
        
        scroll_area = create_scrollable_area(self.query_preview)
        right_panel.addWidget(scroll_area)
        
        # Wrap panels into main layout
        main_layout.addLayout(left_panel, stretch=2)
        main_layout.addLayout(right_panel, stretch=3) # Wider preview area
        
        self.setLayout(main_layout)
        
        # Link to Live Query update (with highlight effect)
        self.username_input.textChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.username_input.text().split(",")[-1].strip())          
            ))
        
        self.keyword_input.textChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.keyword_input.text().split(",")[-1].strip())          
            ))
           
        self.hashtag_input.textChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.hashtag_input.text().split(",")[-1].strip())          
            ))
        
        self.music_input.textChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.music_input.text().split(",")[-1].strip()) 
            ))
        
        self.effect_input.textChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.effect_input.text().split(",")[-1].strip())
            ))
        
        self.start_date.dateChanged.connect(lambda: (           
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.start_date.text())
            ))
        
        self.end_date.dateChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, self.end_date.text())
            ))
        
        self.length_checkboxes["SHORT"].stateChanged.connect(lambda: (
        self.update_query_preview(),
        focus_on_query_value(self.query_preview, "SHORT")
    ))
        self.length_checkboxes["MID"].stateChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, "MID")
        ))
        self.length_checkboxes["LONG"].stateChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, "LONG")
        ))
        self.length_checkboxes["EXTRA_LONG"].stateChanged.connect(lambda: (
            self.update_query_preview(),
            focus_on_query_value(self.query_preview, "EXTRA_LONG")
        ))
        
        for cb in self.main_checkboxes.values():
            cb.stateChanged.connect(self.update_query_preview)
        for cb in self.advanced_checkboxes.values():
            cb.stateChanged.connect(self.update_query_preview)
        for cb in self.length_checkboxes.values():
            cb.stateChanged.connect(self.update_query_preview)
        
        for spinbox, combo in self.numeric_inputs.values():
            spinbox.valueChanged.connect(self.update_query_preview)
            combo.currentIndexChanged.connect(self.update_query_preview)
            
        self.update_query_preview()    # Update defalt view of Live Query Preview
     
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
        
        layout.addWidget(create_field_group_with_emojis("Main Fields", MAIN_FIELDS, self.main_checkboxes, default_checked=True))
        
        adv_group = create_field_group_with_emojis("", ADVANCED_FIELDS, self.advanced_checkboxes, default_checked=True)
        adv_section = create_collapsible_section("Advanced Fields", adv_group, checked=True, on_toggle_callback=self.update_query_preview)
        layout.addWidget(adv_section)
   
        tab.setLayout(layout)
        return tab
            
    def create_filter_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 1. Username
        self.username_input = QLineEdit()
        layout.addWidget(create_labeled_input("Username(s) (comma-separated):", self.username_input))
    
        # Horizontal Line before Keyword filters        
        layout.addWidget(create_horizontal_line())
        
        # 2. Keyword
        self.keyword_input = QLineEdit()
        layout.addWidget(create_labeled_input("Keywords (comma-separated):", self.keyword_input))
    
        # Horizontal Line before Hashtag filters
        layout.addWidget(create_horizontal_line())
        
        # 3. Hashtag
        self.hashtag_input = QLineEdit()
        layout.addWidget(create_labeled_input("Hashtags (comma-separated):", self.hashtag_input))
        
        # Horizontal Line before Date Range filters
        layout.addWidget(create_horizontal_line())
    
        # 4. Date Range
        self.date_widget, self.start_date, self.end_date = create_date_range_widget()
        layout.addWidget(self.date_widget)
        
        # Horizontal Line before Region filters
        layout.addWidget(create_horizontal_line())
        
        # 5. Region Code (Multi-Select)
        self.region_widget, self.region_combo, self.region_display, self.selected_region_codes = create_multi_select_input_with_labels(
            "Select Region(s):", self.region_codes, on_add_callback=self.update_query_preview
            )
        layout.addWidget(self.region_widget)
        
        # Horizontal Line before numeric filters
        layout.addWidget(create_horizontal_line())
    
        # 6. Numeric Filters
        self.numeric_fields = ["like_count", "view_count", "comment_count", "share_count"]
        layout.addWidget(QLabel("Numeric Filters:"))
        numeric_widget, self.numeric_inputs = create_numeric_filter_group(self.numeric_fields, list(self.condition_ops.keys()), default_op = "Greater than")
        layout.addWidget(numeric_widget)
    
        # Horizontal Line after numeric filters
        layout.addWidget(create_horizontal_line())
        
        # 7. Video Length
        length_group, self.length_checkboxes = create_enum_checkbox_group("Video Length", ["SHORT", "MID", "LONG", "EXTRA_LONG"])
        layout.addWidget(length_group)
    
        # 8. Music ID
        self.music_input = QLineEdit()
        layout.addWidget(create_labeled_input("Music IDs (comma-separated):", self.music_input))
        
        # Horizontal Line before Effect ID filters
        layout.addWidget(create_horizontal_line())
    
        # 9. Effect ID
        self.effect_input = QLineEdit()
        layout.addWidget(create_labeled_input("Effect IDs (comma-separated):", self.effect_input))

      
        tab.setLayout(layout)
        return tab

    def build_query(self):
        
        # Selected Fields
        included_fields = [f for f, cb in self.main_checkboxes.items() if cb.isChecked()] + \
                          [f for f, cb in self.advanced_checkboxes.items() if cb.isChecked()]
    
        # Filter conditions
        conditions = []
        add_condition = lambda f, vals: conditions.append({
            "field_name": f,
            "operation": "IN",
            "field_values": vals
        }) if vals else None
    
        add_condition("username", [s.strip() for s in self.username_input.text().split(',') if s.strip()])
        add_condition("keyword", [s.strip() for s in self.keyword_input.text().split(',') if s.strip()])
        add_condition("hashtag_name", [s.strip() for s in self.hashtag_input.text().split(',') if s.strip()])
        add_condition("music_id", [s.strip() for s in self.music_input.text().split(',') if s.strip()])
        add_condition("effect_id", [s.strip() for s in self.effect_input.text().split(',') if s.strip()])
        add_condition("video_length", [k for k, cb in self.length_checkboxes.items() if cb.isChecked()])
    
        # region_code (Select all if nothing has selected)
        region_codes_to_use = self.selected_region_codes if self.selected_region_codes else list(self.region_codes.values())
        add_condition("region_code", region_codes_to_use)
            
        # Numeric filters
        for field, (spinbox, combo) in self.numeric_inputs.items():
            val = spinbox.value()
            op_label = combo.currentText()
            op_code = self.condition_ops.get(op_label, "GT")
            if val > 0:
                conditions.append({
                    "field_name": field,
                    "operation": op_code,
                    "field_values": [str(val)]
                })
    
        # Date Range
        start_date = self.start_date.date().toString("yyyyMMdd")
        end_date = self.end_date.date().toString("yyyyMMdd")
    
        # Final Query
        query = {
            "fields": included_fields,
            "query": {"and": conditions},
            "start_date": start_date,
            "end_date": end_date
        }
    
        return query    
    
    def update_query_preview(self):    
        query = self.build_query()
        self.query_preview.setPlainText(json.dumps(query, indent=2))
    
    def run_query(self):
        query = self.build_query()
        self.query_preview.setPlainText(json.dumps(query, indent=2)) # Just for checking
        
        def fetch_videos():
            return self.api.get_video_by_dynamic_query_body(
                {"query": query["query"]},
                query["start_date"],
                query["end_date"]
                )
        
        def after_fetch(result):
            if not result:
                QMessageBox.information(self, "No Results", "No videos found.")
                return
            FileConverter().save_jason_to_csv(result, "video_result.csv")
            self.viewer = DataViewer()
            self.viewer.show()
        
        ProgressBar.run_with_progress(self, fetch_videos, after_fetch)
        
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
        
        # Clear region codes
        self.selected_regions_codes.clear()
        self.region_display.setText("Selected: ")
        self.region_combo.setCurrentIndex(0)
    
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
