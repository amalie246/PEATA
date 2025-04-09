from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QGroupBox, QDateEdit, QTableView,
    QProgressBar, QPushButton, QScrollArea, QWidget, QSizePolicy, QFrame
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
import os

# For general structure styling. Created this for reusable components in UI

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
def create_collapsible_section(title: str, widget: QWidget):
    container = QGroupBox(title)
    container.setCheckable(True)
    container.setChecked(False)
    layout = QVBoxLayout()
    layout.addWidget(widget)
    container.setLayout(layout)
    return container

# For various fields (text box, dropdown etc)
def create_labeled_input(label_text: str, input_widget: QWidget):
    label = QLabel(label_text)
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

def create_button(text: str, object_name: str = "", tooltip: str = "", icon_path: str = "", click_callback=None):
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