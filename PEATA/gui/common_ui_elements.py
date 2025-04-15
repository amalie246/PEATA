from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QGroupBox, QDateEdit, 
    QTableView, QProgressBar, QPushButton, QScrollArea, QWidget, QSizePolicy, 
    QFrame, QSpinBox, QComboBox
)
from PyQt5.QtCore import QDate, QTimer
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat, QColor
from region_codes import get_flag_emoji
import os

# For general structure styling. Created this for reusable components in UI

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

def create_date_range_widget():
    start_label = QLabel("Start Date:")
    start_date = QDateEdit()
    start_date.setCalendarPopup(True)
    start_date.setDate(QDate.currentDate().addDays(-7))

    end_label = QLabel("End Date:")
    end_date = QDateEdit()
    end_date.setCalendarPopup(True)
    end_date.setDate(QDate.currentDate())

    layout = QHBoxLayout()
    layout.addWidget(start_label)
    layout.addWidget(start_date)
    layout.addWidget(end_label)
    layout.addWidget(end_date)

    container = QWidget()
    container.setLayout(layout)
    return container, start_date, end_date


def create_field_checkbox_group(fields):
    group_box = QGroupBox("Select Fields")
    layout = QVBoxLayout()
    checkboxes = {}

    for field in fields:
        cb = QCheckBox(f"{field}")
        checkboxes[field] = cb
        layout.addWidget(cb)

    group_box.setLayout(layout)
    return group_box, checkboxes


def create_result_table():
    table = QTableView()
    table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return table


def create_progress_bar():
    bar = QProgressBar()
    bar.setRange(0, 0)  # Indeterminate mode
    bar.setVisible(False) # Set True later!
    return bar

# For Advanced filters (less used options)
def create_collapsible_section(title: str, widget: QWidget, checked =True, on_toggle_callback=None):
    container = QGroupBox(title)
    container.setCheckable(True)
    container.setChecked(checked)
    
    layout = QVBoxLayout()
    layout.addWidget(widget)
    container.setLayout(layout)
    
    # Connect to Signal : If main advanced filter are unchecked, all children checkboxes are unchecked and update live query preview
    def handle_groupbox_toggled(state):
        for cb in widget.findChildren(QCheckBox):
            cb.setChecked(state)
        if on_toggle_callback:
            on_toggle_callback()
            
    container.toggled.connect(handle_groupbox_toggled)        
        
    return container

# For various fields (text box, dropdown etc)
def create_labeled_input(label_text: str, input_widget: QWidget, placeholder: str = ""):
    label = QLabel(label_text)
    if hasattr(input_widget, 'setPlaceholderText'):
        input_widget.setPlaceholderText(placeholder)
    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(input_widget)
    container = QWidget()
    container.setLayout(layout)
    return container

# For checkboxes in Advanced Options
def create_scrollable_area(content: QWidget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(content)
    return scroll


def create_horizontal_line():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    return line

def create_button(
        text: str, 
        object_name: str = "", 
        tooltip: str = "", 
        icon_path: str = "", 
        click_callback=None
        ):
    
    button = QPushButton(text)
    if object_name:
        button.setObjectName(object_name)
    if tooltip:
        button.setToolTip(tooltip)
    if icon_path and os.path.exists(icon_path):
        button.setIcon(QIcon(icon_path))
    if click_callback:
        button.clicked.connect(click_callback)
    return button

def create_field_group_with_emojis(
        title: str, fields: dict, store_dict: dict, default_checked=True
        ):
    
    group = QGroupBox(title)
    vbox = QVBoxLayout()
    for field, (emoji, tooltip) in fields.items():
        checkbox = QCheckBox(f"{emoji} {field.replace('_', ' ').title()}")
        checkbox.setToolTip(tooltip)
        checkbox.setChecked(default_checked)
        store_dict[field] = checkbox
        vbox.addWidget(checkbox)
    group.setLayout(vbox)
    return group

def create_enum_checkbox_group(title: str, enum_values: list, default_checked=True):
    group_box = QGroupBox(title)
    layout = QVBoxLayout()
    checkboxes = {}
    for val in enum_values:
        cb = QCheckBox(val)
        cb.setChecked(default_checked)
        layout.addWidget(cb)
        checkboxes[val] = cb
    group_box.setLayout(layout)
    return group_box, checkboxes

def create_numeric_filter_group(fields: list, operators: list, default_op="GT"):
    numeric_inputs = {}
    layout = QVBoxLayout()
    
    for field in fields:
        hbox = QHBoxLayout()
        label = QLabel(field.replace("_", " ").title())
        spinbox = QSpinBox()
        spinbox.setMaximum(1_000_000)
        spinbox.setMinimum(0)
        
        op_selector = QComboBox()
        op_selector.addItems(operators)
        op_selector.setCurrentText(default_op)
        
        hbox.addWidget(label)
        hbox.addWidget(spinbox)
        hbox.addWidget(op_selector)
        container = QWidget()
        container.setLayout(hbox)
        layout.addWidget(container)
        numeric_inputs[field] = (spinbox, op_selector)
    container_widget = QWidget()
    container_widget.setLayout(layout)
    return container_widget, numeric_inputs

def focus_on_query_value(text_edit, value_str):
    """
    Scroll to new added value inside the Live Query View, add on hightlight effect with red color
    - text_edit: QTextEdit instance
    - value_str: new added value"
    """
    
    if not value_str or not value_str.strip():
        return # Ignore empty space or empty string
    
    text = text_edit.toPlainText()
    target = f'"{value_str.strip()}"'
    index = text.find(target)
    
    if index == -1:
        return # No change if there is no relevant value

    # Select exact range
    cursor = text_edit.textCursor()
    cursor.setPosition(index)
    cursor.setPosition(index + len(target), QTextCursor.KeepAnchor)
    
    # Highlight format (Red)
    highlight_format = QTextCharFormat()
    highlight_format.setBackground(QColor("red"))
    cursor.mergeCharFormat(highlight_format)
    
    # Move Scroll 
    text_edit.setTextCursor(cursor)
    text_edit.ensureCursorVisible()   

    # Remove highlight effect after 1 sec
    def clear_highlight():
        cursor.setPosition(index)
        cursor.setPosition(index + len(target), QTextCursor.KeepAnchor)
        clear_format = QTextCharFormat()
        clear_format.setBackground(QColor("transparent"))
        cursor.mergeCharFormat(clear_format)

    QTimer.singleShot(1000, clear_highlight)

# Multi-select using QComboBox + Add button + Selected Display Label
def create_multi_select_input_with_labels(label_text: str, name_code_map: dict, on_add_callback=None):
    
    combo = QComboBox()
    combo.setEditable(True) # Available to search
    
    display_to_code = {}
    for name, code in name_code_map.items():
        display_text = f"{get_flag_emoji(code)} {name}"
        combo.addItem(display_text)
        display_to_code[display_text] = code  # internal map
        
    add_btn = QPushButton("Add")
    remove_btn = QPushButton("Remove")
    clear_all_btn = QPushButton("Clear All")
    selected_label = QLabel("Selected: ALL") # Default
    selected_label.setObjectName("SelectedRegionLabel")
    
    
    selected_codes = []
    
    def update_label():
        if selected_codes:
            selected_label.setText("Selected: " + ", ".join(selected_codes))
        else:
            selected_label.setText("Selected: All")
    
    def add_value():
        display_text = combo.currentText().strip()
        if display_text in display_to_code:
             code = display_to_code[display_text]
             if code not in selected_codes:
                 selected_codes.append(code)
                 selected_label.setText("Selected: " + ", ".join(selected_codes))
                 if on_add_callback:
                    on_add_callback()
     
    def remove_value():
        display_text = combo.currentText().strip()
        if display_text in display_to_code:
            code = display_to_code[display_text]
            if code in selected_codes:
                selected_codes.remove(code)
                update_label()
                if on_add_callback:
                    on_add_callback()
     
    def clear_all():
        selected_codes.clear()
        update_label()
        if on_add_callback:
            on_add_callback()
        
    add_btn.clicked.connect(add_value)
    remove_btn.clicked.connect(remove_value)
    clear_all_btn.clicked.connect(clear_all)
    
    hbox = QHBoxLayout()
    hbox.addWidget(combo)
    hbox.addWidget(add_btn)
    hbox.addWidget(remove_btn)
    hbox.addWidget(clear_all_btn)
    
    container = QWidget()
    container.setLayout(hbox)
    
    outer_layout = QVBoxLayout()
    outer_layout.addWidget(QLabel(label_text))
    outer_layout.addWidget(container)
    outer_layout.addWidget(selected_label)
    
    outer_container = QWidget()
    outer_container.setLayout(outer_layout)
    
    return outer_container, combo, selected_label, selected_codes
    