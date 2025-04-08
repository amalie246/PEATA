from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QTextEdit,
    QDateEdit, QComboBox, QScrollArea, QGroupBox, QFrame, QSpinBox, QLineEdit, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import QDate, Qt
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

        self.logic_ops = {
            "Equals": "EQ",
            "Greater than": "GT",
            "Greater or equal": "GTE",
            "Less than": "LT",
            "Less or equal": "LTE",
            "One of (multi-select)": "IN"
        }

        self.region_codes = {
            'France (FR)': 'FR', 'Thailand (TH)': 'TH', 'Myanmar (MM)': 'MM', 'Bangladesh (BD)': 'BD', 'Italy (IT)': 'IT', 'Nepal (NP)': 'NP', 'Iraq (IQ)': 'IQ',
            'Brazil (BR)': 'BR', 'USA (US)': 'US', 'Kuwait (KW)': 'KW', 'Vietnam (VN)': 'VN', 'Argentina (AR)': 'AR', 'Kazakhstan (KZ)': 'KZ', 'UK (GB)': 'GB',
            'Ukraine (UA)': 'UA', 'Turkey (TR)': 'TR', 'Indonesia (ID)': 'ID', 'Pakistan (PK)': 'PK', 'Nigeria (NG)': 'NG', 'Cambodia (KH)': 'KH', 'Philippines (PH)': 'PH',
            'Egypt (EG)': 'EG', 'Qatar (QA)': 'QA', 'Malaysia (MY)': 'MY', 'Spain (ES)': 'ES', 'Jordan (JO)': 'JO', 'Morocco (MA)': 'MA', 'Saudi Arabia (SA)': 'SA',
            'Taiwan (TW)': 'TW', 'Afghanistan (AF)': 'AF', 'Ecuador (EC)': 'EC', 'Mexico (MX)': 'MX', 'Botswana (BW)': 'BW', 'Japan (JP)': 'JP', 'Lithuania (LT)': 'LT',
            'Tunisia (TN)': 'TN', 'Romania (RO)': 'RO', 'Libya (LY)': 'LY', 'Israel (IL)': 'IL', 'Algeria (DZ)': 'DZ', 'Congo (CG)': 'CG', 'Ghana (GH)': 'GH',
            'Germany (DE)': 'DE', 'Benin (BJ)': 'BJ', 'Senegal (SN)': 'SN', 'Slovakia (SK)': 'SK', 'Belarus (BY)': 'BY', 'Netherlands (NL)': 'NL', 'Laos (LA)': 'LA',
            'Belgium (BE)': 'BE', 'Dominican Republic (DO)': 'DO', 'Tanzania (TZ)': 'TZ', 'Sri Lanka (LK)': 'LK', 'Nicaragua (NI)': 'NI', 'Lebanon (LB)': 'LB',
            'Ireland (IE)': 'IE', 'Serbia (RS)': 'RS', 'Hungary (HU)': 'HU', 'Portugal (PT)': 'PT', 'Guadeloupe (GP)': 'GP', 'Cameroon (CM)': 'CM', 'Honduras (HN)': 'HN',
            'Finland (FI)': 'FI', 'Gabon (GA)': 'GA', 'Brunei (BN)': 'BN', 'Singapore (SG)': 'SG', 'Bolivia (BO)': 'BO', 'Gambia (GM)': 'GM', 'Bulgaria (BG)': 'BG',
            'Sudan (SD)': 'SD', 'Trinidad and Tobago (TT)': 'TT', 'Oman (OM)': 'OM', 'Faroe Islands (FO)': 'FO', 'Mozambique (MZ)': 'MZ', 'Mali (ML)': 'ML',
            'Uganda (UG)': 'UG', 'Reunion (RE)': 'RE', 'Paraguay (PY)': 'PY', 'Guatemala (GT)': 'GT', 'Ivory Coast (CI)': 'CI', 'Suriname (SR)': 'SR', 'Angola (AO)': 'AO',
            'Azerbaijan (AZ)': 'AZ', 'Liberia (LR)': 'LR', 'Congo (CD)': 'CD', 'Croatia (HR)': 'HR', 'El Salvador (SV)': 'SV', 'Maldives (MV)': 'MV', 'Guyana (GY)': 'GY',
            'Bahrain (BH)': 'BH', 'Togo (TG)': 'TG', 'Sierra Leone (SL)': 'SL', 'North Macedonia (MK)': 'MK', 'Kenya (KE)': 'KE', 'Malta (MT)': 'MT', 'Madagascar (MG)': 'MG',
            'Mauritania (MR)': 'MR', 'Panama (PA)': 'PA', 'Iceland (IS)': 'IS', 'Luxembourg (LU)': 'LU', 'Haiti (HT)': 'HT', 'Turkmenistan (TM)': 'TM', 'Zambia (ZM)': 'ZM',
            'Costa Rica (CR)': 'CR', 'Norway (NO)': 'NO', 'Albania (AL)': 'AL', 'Ethiopia (ET)': 'ET', 'Guinea-Bissau (GW)': 'GW', 'Australia (AU)': 'AU',
            'South Korea (KR)': 'KR', 'Uruguay (UY)': 'UY', 'Jamaica (JM)': 'JM', 'Denmark (DK)': 'DK', 'United Arab Emirates (AE)': 'AE', 'Moldova (MD)': 'MD',
            'Sweden (SE)': 'SE', 'Mauritius (MU)': 'MU', 'Somalia (SO)': 'SO', 'Colombia (CO)': 'CO', 'Austria (AT)': 'AT', 'Greece (GR)': 'GR', 'Uzbekistan (UZ)': 'UZ',
            'Chile (CL)': 'CL', 'Georgia (GE)': 'GE', 'Poland (PL)': 'PL', 'Canada (CA)': 'CA', 'Czech Republic (CZ)': 'CZ', 'South Africa (ZA)': 'ZA',
            'Anguilla (AI)': 'AI', 'Venezuela (VE)': 'VE', 'Kyrgyzstan (KG)': 'KG', 'Peru (PE)': 'PE', 'Switzerland (CH)': 'CH', 'Latvia (LV)': 'LV', 'Puerto Rico (PR)': 'PR',
            'New Zealand (NZ)': 'NZ', 'Timor-Leste (TL)': 'TL', 'Bhutan (BT)': 'BT', 'Mongolia (MN)': 'MN', 'Fiji (FJ)': 'FJ', 'Eswatini (SZ)': 'SZ', 'Vanuatu (VU)': 'VU',
            'Burkina Faso (BF)': 'BF', 'Tajikistan (TJ)': 'TJ', 'Bosnia and Herzegovina (BA)': 'BA', 'Armenia (AM)': 'AM', 'Chad (TD)': 'TD', 'Slovenia (SI)': 'SI',
            'Cyprus (CY)': 'CY', 'Malawi (MW)': 'MW', 'Estonia (EE)': 'EE', 'Kosovo (XK)': 'XK', 'Montenegro (ME)': 'ME', 'Cayman Islands (KY)': 'KY',
            'Yemen (YE)': 'YE', 'Lesotho (LS)': 'LS', 'Zimbabwe (ZW)': 'ZW', 'Monaco (MC)': 'MC', 'Guinea (GN)': 'GN', 'Bahamas (BS)': 'BS', 'French Polynesia (PF)': 'PF',
            'Namibia (NA)': 'NA', 'US Virgin Islands (VI)': 'VI', 'Barbados (BB)': 'BB', 'Belize (BZ)': 'BZ', 'Curaçao (CW)': 'CW', 'Palestine (PS)': 'PS',
            'Micronesia (FM)': 'FM', 'Papua New Guinea (PG)': 'PG', 'Burundi (BI)': 'BI', 'Andorra (AD)': 'AD', 'Tuvalu (TV)': 'TV', 'Greenland (GL)': 'GL',
            'Comoros (KM)': 'KM', 'Aruba (AW)': 'AW', 'Turks and Caicos (TC)': 'TC', 'Cape Verde (CV)': 'CV', 'Macau (MO)': 'MO', 'Saint Vincent (VC)': 'VC',
            'Niger (NE)': 'NE', 'Samoa (WS)': 'WS', 'Northern Mariana Islands (MP)': 'MP', 'Djibouti (DJ)': 'DJ', 'Rwanda (RW)': 'RW', 'Antigua and Barbuda (AG)': 'AG',
            'Gibraltar (GI)': 'GI', 'Equatorial Guinea (GQ)': 'GQ', 'American Samoa (AS)': 'AS', 'Åland Islands (AX)': 'AX', 'Tonga (TO)': 'TO',
            'Saint Kitts and Nevis (KN)': 'KN', 'Saint Lucia (LC)': 'LC', 'New Caledonia (NC)': 'NC', 'Liechtenstein (LI)': 'LI', 'South Sudan (SS)': 'SS',
            'Iran (IR)': 'IR', 'Syria (SY)': 'SY', 'Isle of Man (IM)': 'IM', 'Seychelles (SC)': 'SC', 'British Virgin Islands (VG)': 'VG', 'Solomon Islands (SB)': 'SB',
            'Dominica (DM)': 'DM', 'Kiribati (KI)': 'KI', 'U.S. Minor Outlying Islands (UM)': 'UM', 'Sint Maarten (SX)': 'SX', 'Grenada (GD)': 'GD',
            'Marshall Islands (MH)': 'MH', 'Caribbean Netherlands (BQ)': 'BQ', 'Mayotte (YT)': 'YT', 'São Tomé and Príncipe (ST)': 'ST', 'Central African Republic (CF)': 'CF',
            'Bermuda (BM)': 'BM', 'San Marino (SM)': 'SM', 'Palau (PW)': 'PW', 'Guam (GU)': 'GU', 'Hong Kong (HK)': 'HK', 'India (IN)': 'IN', 'Cook Islands (CK)': 'CK',
            'Antarctica (AQ)': 'AQ', 'Wallis and Futuna (WF)': 'WF', 'Jersey (JE)': 'JE', 'Martinique (MQ)': 'MQ', 'China (CN)': 'CN', 'French Guiana (GF)': 'GF',
            'Montserrat (MS)': 'MS', 'Guernsey (GG)': 'GG', 'Tokelau (TK)': 'TK', 'Falkland Islands (FK)': 'FK', 'Saint Pierre and Miquelon (PM)': 'PM',
            'Niue (NU)': 'NU', 'Saint Martin (MF)': 'MF', 'Eritrea (ER)': 'ER', 'Norfolk Island (NF)': 'NF', 'Vatican (VA)': 'VA', 'British Indian Ocean Territory (IO)': 'IO',
            'Saint Helena (SH)': 'SH', 'Saint Barthélemy (BL)': 'BL', 'Cuba (CU)': 'CU', 'Nauru (NR)': 'NR', 'East Timor (TP)': 'TP', 'Bouvet Island (BV)': 'BV',
            'Western Sahara (EH)': 'EH', 'Pitcairn Islands (PN)': 'PN', 'French Southern Territories (TF)': 'TF', 'Russia (RU)': 'RU'
        }

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
        filter_layout.addWidget(QLabel("Logic Operation (applied to all filters):"))
        filter_layout.addWidget(self.logic_selector)

        # Keyword filter (multi-entry)
        keyword_layout = QVBoxLayout()
        keyword_layout.addWidget(QLabel("Keywords (multiple allowed, comma separated):"))
        self.keyword_input = QLineEdit()
        self.keyword_input.setToolTip("Separate multiple keywords with commas, e.g. climate, protest, covid")
        self.keyword_input.setPlaceholderText("e.g. climate, protest, covid")
        keyword_layout.addWidget(self.keyword_input)
        filter_layout.addLayout(keyword_layout)

        # Region filter (multi-select list)
        region_layout = QVBoxLayout()
        region_label = QLabel("Select Region(s):")
        region_label.setToolTip("Hold Ctrl (or Cmd on Mac) to select multiple regions")
        region_layout.addWidget(region_label)
        self.region_selector = QComboBox()
        self.region_selector.setEditable(True)
        self.region_selector.setInsertPolicy(QComboBox.NoInsert)
        self.region_selector.setToolTip("Type to filter countries, hold Ctrl (Cmd) to multi-select")
        self.region_selector.setMaxVisibleItems(10)

        # Populate with flags and labels
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

        # Video length
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Video Length:"))
        self.length_selector = QListWidget()
        self.length_selector.setSelectionMode(QListWidget.MultiSelection)
        for val in ["SHORT", "MID", "LONG", "EXTRA_LONG"]:
            self.length_selector.addItem(val)
        self.length_selector.setToolTip("Hold Ctrl (or Cmd) to select multiple lengths")
        length_layout.addWidget(self.length_selector)
        filter_layout.addLayout(length_layout)

        # Username filter
        username_layout = QVBoxLayout()
        username_layout.addWidget(QLabel("Username(s):"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g. user1, user2")
        self.username_input.setToolTip("Separate multiple usernames with commas")
        username_layout.addWidget(self.username_input)
        filter_layout.addLayout(username_layout)

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
        right_side.addWidget(self.run_button)

        # ---------- Query Preview ----------
        self.query_preview = QTextEdit()
        self.query_preview.setReadOnly(True)
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
