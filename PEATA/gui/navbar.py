import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, pyqtSignal

# ───── HoverIconButton class ─────
class HoverIconButton(QToolButton):
    def __init__(self, label, icon_default_path, icon_hover_path, icon_size, style, height):
        super().__init__()
        self.icon_default = QIcon(icon_default_path)
        self.icon_hover = QIcon(icon_hover_path)

        self.setText(label)
        self.setIcon(self.icon_default)
        self.setIconSize(icon_size)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setMinimumHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet(style)

    def enterEvent(self, event):
        self.setIcon(self.icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.icon_default)
        super().leaveEvent(event)

# ───── Navbar Widget ─────
class Navbar(QWidget):
    user_query_clicked = pyqtSignal()
    video_query_clicked = pyqtSignal()
    comment_query_clicked = pyqtSignal()
    about_clicked = pyqtSignal()
    exit_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(15)

        # ───── Style and Paths ─────
        button_height = 80
        icon_size = QSize(64, 64)
        base_path = os.path.join(os.path.dirname(__file__), "assets")
        icon_path = lambda name, theme: os.path.join(base_path, f"{name}_{theme}.svg")

        style = """
        QToolButton {
            background-color: #0078d7;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
        }
        QToolButton:hover {
            background-color: #005a9e;
        }
        QToolButton:pressed {
            background-color: #003f7d;
        }
        """

        def create_hover_button(label, icon_name, on_click=None):
            btn = HoverIconButton(
                label=label,
                icon_default_path=icon_path(icon_name, "dark"),
                icon_hover_path=icon_path(icon_name, "light"),
                icon_size=icon_size,
                style=style,
                height=button_height
            )
            if on_click:
                btn.clicked.connect(on_click)
            return btn

        # ───── Buttons ─────
        layout.addWidget(create_hover_button("USER QUERY", "icon_user"))
        layout.addWidget(create_hover_button("VIDEO QUERY", "icon_video"))
        layout.addWidget(create_hover_button("COMMENT\nQUERY", "icon_comments"))

        # Extra space before ABOUT US
        layout.addSpacerItem(QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        layout.addWidget(create_hover_button("ABOUT US", "icon_info", self.about_clicked.emit))

        # Extra space before EXIT
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # EXIT button
        layout.addWidget(create_hover_button("EXIT", "icon_exit", self.exit_clicked.emit))

        self.setLayout(layout)
        self.setFixedWidth(150)
