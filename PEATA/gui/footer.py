import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QFrame
)
from PyQt5.QtCore import Qt


class Footer(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Horizontal line
        line = QFrame()
        line.setObjectName("footerLine")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Vertical layout for labels
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        # GitHub link label
        gitHub_label = QLabel(
            '<a href="https://github.com/amalie246/PEATA.git">GitHub</a>'
        )
        gitHub_label.setObjectName("gitHubLabel")
        gitHub_label.setAlignment(Qt.AlignCenter)
        gitHub_label.setOpenExternalLinks(True)
        gitHub_label.setTextInteractionFlags(Qt.TextBrowserInteraction)

        # Copyright label
        copyright_label = QLabel("v1.0.0 © 2025 PEATA Team")
        copyright_label.setObjectName("copyrightLabel")
        copyright_label.setAlignment(Qt.AlignCenter)

        # Add labels to text layout
        text_layout.addWidget(gitHub_label)
        text_layout.addWidget(copyright_label)

        # Add to main layout
        layout.addLayout(text_layout)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        self.setLayout(layout)


# For quick test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    footer = Footer()
    footer.show()
    sys.exit(app.exec())
