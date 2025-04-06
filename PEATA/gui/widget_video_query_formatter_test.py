from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QDateEdit, QCheckBox, QSpinBox, QTextEdit
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon

# # Path for testing (Not working yet!)
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
# from queryFormatter import QueryFormatter


class VideoQueryFormatter(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Username
        self.username_input = QLineEdit()
        layout.addLayout(self._labeled_row("Username:", self.username_input))

        # Keyword
        self.keyword_input = QLineEdit()
        layout.addLayout(self._labeled_row("Keyword:", self.keyword_input))

        # Date Range
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-7))

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())

        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("Start Date:"))
        date_row.addWidget(self.start_date)
        date_row.addWidget(QLabel("End Date:"))
        date_row.addWidget(self.end_date)
        layout.addLayout(date_row)

        # Logic Operation Selector
        self.logic_selector = QComboBox()
        self.logic_selector.addItems(["AND", "OR", "NOT"])
        layout.addLayout(self._labeled_row("Logic Type:", self.logic_selector))

        # Minimum view count
        self.min_views = QSpinBox()
        self.min_views.setMaximum(1_000_000_000)
        layout.addLayout(self._labeled_row("Minimum Views:", self.min_views))

        # Extra filters
        self.voice_checkbox = QCheckBox("Has Voice-to-Text")
        stem_layout, self.stem_checkbox = self.create_stem_verified_row_help_icon()
        self.music_checkbox = QCheckBox("Has Music")
        layout.addWidget(self.voice_checkbox)
        layout.addLayout(stem_layout)
        layout.addWidget(self.music_checkbox)
    
        # Run query button
        self.run_button = QPushButton("Run Query")
        self.run_button.clicked.connect(self.run_query)
        layout.addWidget(self.run_button)

        # Preview area (Optional)
        self.query_preview = QTextEdit()
        self.query_preview.setReadOnly(True)
        layout.addWidget(QLabel("Generated Query JSON:"))
        layout.addWidget(self.query_preview)

        self.setLayout(layout)
        
    def create_stem_verified_row_help_icon(self):
        layout = QHBoxLayout()
        
        stem_checkbox = QCheckBox("Is Stem Verified")
        layout.addWidget(stem_checkbox)
        
        # Create help icon label
        help_icon = QLabel("❓")
        help_icon.setToolTip(
            "‘Is Stem Verified’ indicates whether the video’s audio/music has been analyzed and verified by TikTok's machine learning system, often related to licensed or original content."
            )
        help_icon.setCursor(Qt.CursorShape.WhatsThisCursor)
        layout.addWidget(help_icon)
        
        return layout, stem_checkbox    

    def _labeled_row(self, label_text, widget):
        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))
        row.addWidget(widget)
        return row

    def run_query(self):
        # This function builds a query preview using form inputs
        username = self.username_input.text()
        keyword = self.keyword_input.text()
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        logic = self.logic_selector.currentText()

        conditions = []
        if username:
            conditions.append(("username", username, "EQ"))
        if keyword:
            conditions.append(("keyword", keyword, "EQ"))
        if self.min_views.value() > 0:
            conditions.append(("view_count", str(self.min_views.value()), "GT"))
        if self.voice_checkbox.isChecked():
            conditions.append(("voice_to_text", "true", "EQ"))
        if self.stem_checkbox.isChecked():
            conditions.append(("is_stem_verified", "true", "EQ"))
        if self.music_checkbox.isChecked():
            conditions.append(("music_id", "", "NE"))  # example logic

        # Simulate queryFormatter logic
        query_formatter = QueryFormatter()
        if logic == "AND":
            clause = query_formatter.query_AND_clause(conditions)
        elif logic == "OR":
            clause = query_formatter.query_OR_clause(conditions)
        else:
            clause = query_formatter.query_NOT_clause(conditions)

        query_body = query_formatter.query_builder(start, end, clause)

        # Show the query preview
        import json
        self.query_preview.setPlainText(json.dumps(query_body, indent=2))

# For testing
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = VideoQueryFormatter()
    window.setWindowTitle("Video Query Builder")
    window.show()
    sys.exit(app.exec())
