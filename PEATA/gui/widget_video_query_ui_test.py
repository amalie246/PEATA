from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QTextEdit, QDateEdit, QComboBox, QScrollArea, QGroupBox, QFrame, QSpinBox, QLineEdit, QListWidget, QListWidgetItem, QTabWidget
)
from PyQt5.QtCore import QDate, Qt
from region_codes import REGION_CODES
#from queryFormatter import QueryFormatter

# This handels only the visual interface and form inputs for building a video query, missing connection to backend logic (queryFormatter, Api, etc)

#TODO
# 1. Accept user input from GUI (condition, logic, data range)
# 2. Format query
# 3. Send query to backend
# 4. Return data (as pandas DataFrame or list of dicts)
# 5. Expose status to GUI (for progress bar)


def create_checkbox_with_tooltip(label_text: str, emoji: str, tooltip_text: str, checked=True):
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    checkbox = QCheckBox(f"{emoji} {label_text}")
    checkbox.setChecked(checked)
    checkbox.setToolTip(tooltip_text)
    layout.addWidget(checkbox)
    layout.addStretch()
    container = QWidget()
    container.setLayout(layout)
    return container, checkbox

class VideoQueryUI(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Video Query Builder")

        self.logic_ops = {
            "Equals": "EQ",
            "Greater than": "GT",
            "Greater or equal": "GTE",
            "Less than": "LT",
            "Less or equal": "LTE",
            "One of (multi-select)": "IN"
        }

        self.region_codes = REGION_CODES

        main_layout = QVBoxLayout()

        # Split main layout into top (fields+filters) and bottom (preview)
        top_layout = QHBoxLayout()
        left_side = QVBoxLayout()
        right_side = QVBoxLayout()

        # ---------- Main Fields ----------
        main_fields_group = QGroupBox("Main Fields")
        main_fields_layout = QVBoxLayout()

        MAIN_FIELDS = {
            "username": ("\U0001F464", "TikTok handle of the content creator"),
            "create_time": ("\U0001F552", "Time the video was posted"),
            "view_count": ("\U0001F441\uFE0F", "Number of views"),
            "like_count": ("\u2764\uFE0F", "Number of likes"),
            "comment_count": ("\U0001F4AC", "Number of comments"),
            "share_count": ("\U0001F501", "Number of shares"),
            "video_description": ("\U0001F4DD", "Caption or description of the video"),
            "region_code": ("\U0001F30D", "2-letter country code of the creator")
        }

        self.main_checkboxes = {}
        for field, (emoji, tip) in MAIN_FIELDS.items():
            box, cb = create_checkbox_with_tooltip(field.replace("_", " ").title(), emoji, tip)
            main_fields_layout.addWidget(box)
            self.main_checkboxes[field] = cb

        main_fields_group.setLayout(main_fields_layout)
        left_side.addWidget(main_fields_group)

        # ---------- Filter Options ----------
        filter_group = QGroupBox("Filter Options")
        filter_layout = QVBoxLayout()

        date_layout = QHBoxLayout()
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.start_date.setCalendarPopup(True)
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date)
        filter_layout.addLayout(date_layout)

        self.logic_selector = QComboBox()
        self.logic_selector.addItems(list(self.logic_ops.keys()))
        logic_label = QLabel("Logic Operation (applied to all filters): ❓")
        logic_label.setToolTip("Controls how filter conditions are combined. AND = all must match, OR = any match, NOT = exclude match.")
        filter_layout.addWidget(logic_label)
        filter_layout.addWidget(self.logic_selector)

        # Hashtag filter
        hashtag_layout = QVBoxLayout()
        hashtag_layout.addWidget(QLabel("Hashtag Name(s):"))
        self.hashtag_input = QLineEdit()
        self.hashtag_input.setPlaceholderText("e.g. climate, politics")
        self.hashtag_input.setToolTip("Separate multiple hashtags with commas")
        hashtag_layout.addWidget(self.hashtag_input)
        filter_layout.addLayout(hashtag_layout)

        # Keyword filter
        keyword_layout = QVBoxLayout()
        keyword_layout.addWidget(QLabel("Keywords (multiple allowed, comma separated):"))
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("e.g. climate, protest, covid")
        self.keyword_input.setToolTip("Separate multiple keywords with commas")
        keyword_layout.addWidget(self.keyword_input)
        filter_layout.addLayout(keyword_layout)

        # Music ID filter
        music_layout = QVBoxLayout()
        music_label = QLabel("Music ID(s): ❓")
        music_label.setToolTip("Run a broad video query with 'music_id' field checked. You'll get music IDs used in each video.")
        music_layout.addWidget(music_label)
        self.music_input = QLineEdit()
        self.music_input.setPlaceholderText("e.g. 1111, 2222")
        self.music_input.setToolTip("Separate multiple music IDs with commas")
        music_layout.addWidget(self.music_input)
        filter_layout.addLayout(music_layout)

        # Effect ID filter
        effect_layout = QVBoxLayout()
        effect_label = QLabel("Effect ID(s): ❓")
        effect_label.setToolTip("Run a broad video query with 'effect_ids' field checked. You'll get effect IDs used in each video.")
        effect_layout.addWidget(effect_label)
        self.effect_input = QLineEdit()
        self.effect_input.setPlaceholderText("e.g. 123, 456")
        self.effect_input.setToolTip("Separate multiple effect IDs with commas")
        effect_layout.addWidget(self.effect_input)
        filter_layout.addLayout(effect_layout)

        # Video length
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Video Length:"))
        self.length_selector = QListWidget()
        self.length_selector.setSelectionMode(QListWidget.MultiSelection)
        self.length_selector.setMaximumHeight(60)
        for val in ["SHORT", "MID", "LONG", "EXTRA_LONG"]:
            self.length_selector.addItem(val)
        self.length_selector.setToolTip("Hold Ctrl (or Cmd) to select multiple lengths")
        length_layout.addWidget(self.length_selector)
        filter_layout.addLayout(length_layout)

        # Date Range (already included)

        # Username filter
        username_layout = QVBoxLayout()
        username_layout.addWidget(QLabel("Username(s):"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g. user1, user2")
        self.username_input.setToolTip("Separate multiple usernames with commas")
        username_layout.addWidget(self.username_input)
        filter_layout.addLayout(username_layout)

        # Region filter (multi-select with flag emojis)
        region_layout = QVBoxLayout()
        region_label = QLabel("Select Region(s):")
        region_label.setToolTip("Select one or more countries. If none are selected, all regions will be included by default.")
        region_layout.addWidget(region_label)
        self.region_selector = QComboBox()
        self.region_selector.setEditable(True)
        self.region_selector.setInsertPolicy(QComboBox.NoInsert)
        self.region_selector.setToolTip("Type to filter countries, hold Ctrl (Cmd) to multi-select")
        self.region_selector.setMaxVisibleItems(10)

        model = QStandardItemModel()
        for label, code in self.region_codes.items():
            flag = ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in code)
            item = QStandardItem(f"{flag} {label}")
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            model.appendRow(item)
        self.region_selector.setModel(model)
        region_layout.addWidget(self.region_selector)
        filter_layout.addLayout(region_layout)

        # Video ID filter
        video_id_layout = QVBoxLayout()
        video_id_layout.addWidget(QLabel("Video ID(s):"))
        self.video_id_input = QLineEdit()
        self.video_id_input.setPlaceholderText("e.g. 1234, 5678")
        self.video_id_input.setToolTip("Separate multiple video IDs with commas")
        video_id_layout.addWidget(self.video_id_input)
        filter_layout.addLayout(video_id_layout)

        # Hashtag filter
        hashtag_layout = QVBoxLayout()
        hashtag_layout.addWidget(QLabel("Hashtag Name(s):"))
        self.hashtag_input = QLineEdit()
        self.hashtag_input.setPlaceholderText("e.g. climate, politics")
        self.hashtag_input.setToolTip("Separate multiple hashtags with commas")
        hashtag_layout.addWidget(self.hashtag_input)
        filter_layout.addLayout(hashtag_layout)

        # Music ID filter
        music_layout = QVBoxLayout()
        music_label = QLabel("Music ID(s): ❓")
        music_label.setToolTip("Run a broad video query with 'music_id' field checked. You'll get music IDs used in each video.")
        music_layout.addWidget(music_label)
        self.music_input = QLineEdit()
        self.music_input.setPlaceholderText("e.g. 1111, 2222")
        self.music_input.setToolTip("Separate multiple music IDs with commas")
        music_layout.addWidget(self.music_input)
        filter_layout.addLayout(music_layout)

        # Effect ID filter
        effect_layout = QVBoxLayout()
        effect_label = QLabel("Effect ID(s): ❓")
        effect_label.setToolTip("Run a broad video query with 'effect_ids' field checked. You'll get effect IDs used in each video.")
        effect_layout.addWidget(effect_label)
        self.effect_input = QLineEdit()
        self.effect_input.setPlaceholderText("e.g. 123, 456")
        self.effect_input.setToolTip("Separate multiple effect IDs with commas")
        effect_layout.addWidget(self.effect_input)
        filter_layout.addLayout(effect_layout)

        filter_group.setLayout(filter_layout)
        right_side.addWidget(filter_group)

        # ---------- Advanced Fields (Collapsible) ----------
        advanced_group = QGroupBox("Advanced Options")
        advanced_group.setCheckable(True)
        advanced_group.setChecked(False)
        advanced_layout = QVBoxLayout()

        ADVANCED_FIELDS = {
            "music_id": ("\U0001F3B5", "ID of the music used in the video"),
            "is_stem_verified": ("\U0001F9EA", "Whether video is verified STEM content"),
            "effect_ids": ("\U0001F57A", "Effect IDs used in the video"),
            "hashtag_names": ("\U0001F3F7\uFE0F", "Hashtags used in the video"),
            "video_label": ("\U0001F4CB", "Labels like election tags"),
            "video_duration": ("\u23F1\uFE0F", "Video duration in seconds"),
            "favourites_count": ("\u2B50", "Number of times video was favorited"),
            "video_mention_list": ("\U0001F465", "Users tagged in the video"),
            "playlist_id": ("\U0001F4D6", "Playlist to which the video belongs")
        }

        self.advanced_checkboxes = {}
        for field, (emoji, tip) in ADVANCED_FIELDS.items():
            box, cb = create_checkbox_with_tooltip(field.replace("_", " ").title(), emoji, tip, checked=False)
            advanced_layout.addWidget(box)
            self.advanced_checkboxes[field] = cb

        advanced_group.setLayout(advanced_layout)
        left_side.addWidget(advanced_group)

        # ---------- Run Button ----------
        self.run_button = QPushButton("Run Query")
        

        # ---------- Query Preview ----------
        self.query_preview = QTextEdit()
        self.query_preview.setReadOnly(True)
        main_layout.addWidget(self.run_button)
        main_layout.addSpacing(10)
        main_layout.addWidget(QLabel("Generated Query Preview:"))
        main_layout.addWidget(self.query_preview, stretch=1)

        top_layout.addLayout(left_side, 1)
        top_layout.addLayout(right_side, 2)
        main_layout.insertLayout(0, top_layout)
        self.setLayout(main_layout)

        # Connect run button to query execution
        self.run_button.clicked.connect(self.run_query)

    def run_query(self):
        included_fields = []
        conditions = []

        # Collect checked main fields
        for field, checkbox in self.main_checkboxes.items():
            if checkbox.isChecked():
                included_fields.append(field)

        # Collect checked advanced fields
        for field, checkbox in self.advanced_checkboxes.items():
            if checkbox.isChecked():
                included_fields.append(field)

        # Keyword filter
        if self.main_checkboxes.get("video_description") and self.main_checkboxes["video_description"].isChecked():
            keywords = [kw.strip() for kw in self.keyword_input.text().split(',') if kw.strip()]
            if keywords:
                conditions.append(("keyword", keywords, "IN"))

        # Region filter
        if self.main_checkboxes.get("region_code") and self.main_checkboxes["region_code"].isChecked():
            selected_regions = []
        for i in range(self.region_selector.model().rowCount()):
            item = self.region_selector.model().item(i)
            if item.checkState() == Qt.Checked:
                label = item.text().split(' ', 1)[1]  # Remove flag
                if label in self.region_codes:
                    selected_regions.append(self.region_codes[label])
            if selected_regions:
                conditions.append(("region_code", selected_regions, "IN"))

        # Video length (if checked)
        if self.advanced_checkboxes.get("video_duration") and self.advanced_checkboxes["video_duration"].isChecked():
            selected_lengths = [item.text() for item in self.length_selector.selectedItems()]
            if selected_lengths:
                conditions.append(("video_length", selected_lengths, "IN"))

        # Prepare dates
        start_date = self.start_date.date().toString("yyyyMMdd")
        end_date = self.end_date.date().toString("yyyyMMdd")

        # Logic operator
        logic_text = self.logic_selector.currentText()
        logic_op = self.logic_ops[logic_text]

        # Simulate query formatting (replace with real handler later)
        import json
        query = {
            "fields": included_fields,
            "query": {logic_op.lower(): [
                {"field_name": f, "field_values": v, "operation": op}
                for (f, v, op) in conditions
            ]},
            "start_date": start_date,
            "end_date": end_date
        }

        # Show JSON in preview
        # Username filter
        usernames = [u.strip() for u in self.username_input.text().split(',') if u.strip()]
        if usernames:
            conditions.append(("username", usernames, "IN"))

        # Video ID filter
        video_ids = [v.strip() for v in self.video_id_input.text().split(',') if v.strip()]
        if video_ids:
            conditions.append(("video_id", video_ids, "IN"))

        # Hashtag filter
        hashtags = [h.strip() for h in self.hashtag_input.text().split(',') if h.strip()]
        if hashtags:
            conditions.append(("hashtag_name", hashtags, "IN"))

        # Music ID filter
        music_ids = [m.strip() for m in self.music_input.text().split(',') if m.strip()]
        if music_ids:
            conditions.append(("music_id", music_ids, "IN"))

        # Effect ID filter
        effect_ids = [e.strip() for e in self.effect_input.text().split(',') if e.strip()]
        if effect_ids:
            conditions.append(("effect_id", effect_ids, "IN"))

        self.query_preview.setPlainText(json.dumps(query, indent=2))


# For testing
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = VideoQueryUI()
    window.setWindowTitle("Video Query Builder")
    window.show()
    sys.exit(app.exec())
