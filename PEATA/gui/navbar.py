import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, pyqtSignal


class HoverIconButton(QToolButton):
    def __init__(self, label, icon_default_path, icon_hover_path, icon_size, height):
        super().__init__()
        self.icon_default = QIcon(icon_default_path)
        self.icon_hover = QIcon(icon_hover_path)

        self.setText(label)
        self.setIcon(self.icon_default)
        self.setIconSize(icon_size)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setMinimumHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.style_active = """
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

        self.style_disabled = """
            QToolButton {
                background-color: #888;
                color: #ccc;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
        """

        self.setStyleSheet(self.style_active)

    def enterEvent(self, event):
        if self.isEnabled():
            self.setIcon(self.icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.icon_default)
        super().leaveEvent(event)

    def set_active_style(self, active=True):
        self.setStyleSheet(self.style_active if active else self.style_disabled)


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

        # ───── Setup ─────
        button_height = 80
        icon_size = QSize(64, 64)
        base_path = os.path.join(os.path.dirname(__file__), "assets")
        icon_path = lambda name, theme: os.path.join(base_path, f"{name}_{theme}.svg")

        def make_btn(label, icon, slot):
            btn = HoverIconButton(
                label,
                icon_default_path=icon_path(icon, "dark"),
                icon_hover_path=icon_path(icon, "light"),
                icon_size=icon_size,
                height=button_height
            )
            if slot:
                btn.clicked.connect(slot)
            return btn

        # ───── Buttons ─────
        self.user_btn = make_btn("USER QUERY", "icon_user", self.user_query_clicked.emit)
        self.video_btn = make_btn("VIDEO QUERY", "icon_video", self.video_query_clicked.emit)
        self.comment_btn = make_btn("COMMENT\nQUERY", "icon_comments", self.comment_query_clicked.emit)
        self.about_btn = make_btn("ABOUT US", "icon_info", self.about_clicked.emit)
        self.exit_btn = make_btn("EXIT", "icon_exit", self.exit_clicked.emit)

        # Add buttons
        layout.addWidget(self.user_btn)
        layout.addWidget(self.video_btn)
        layout.addWidget(self.comment_btn)
        layout.addSpacerItem(QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addWidget(self.about_btn)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)
        self.setFixedWidth(150)

        self.buttons = [self.user_btn, self.video_btn, self.comment_btn, self.about_btn]

    def set_logged_in(self, is_logged_in: bool):
        for btn in self.buttons:
            btn.setEnabled(is_logged_in)
            btn.set_active_style(is_logged_in)
