from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QRadioButton

from utils.stylesheet_storage import StylesheetStorage
from utils.window_template import WindowTemplate


class Settings(WindowTemplate):
    styles = [
        {
            "button_background-color": "#a9a9a9",
            "primary_color": "white",
            "secondary_color": "#323232",
            "placeholder_color": "#808080",

            "cursor_color": "#a9a9a9",
            "error_color": "#ff3333",
            "blank_color": "#bf9494",

            "header_color": "#242424",
            "cell_color": "#2a2a2a",
            "stats_color": "#b0b0b0",
        },
        {
            "button_background-color": "#808080",
            "primary_color": "black",
            "secondary_color": "#cdcdcd",
            "placeholder_color": "#808080",

            "cursor_color": "#565656",
            "error_color": "#ff3333",
            "blank_color": "#bf9494",

            "header_color": "#dbdbdb",
            "cell_color": "#d5d5d5",
            "stats_color": "#4f4f4f",
        },
        {
            "button_background-color": "#808080",
            "primary_color": "#d17504",
            "secondary_color": "#610e10",
            "placeholder_color": "#e2a528",

            "cursor_color": "#565656",
            "error_color": "#ff3333",
            "blank_color": "#bf9494",

            "header_color": "#630608",
            "cell_color": "#8c0f12",
            "stats_color": "#a67512",
        },
    ]

    def __init__(self, parent):
        super().__init__(parent)

        self.style1 = QRadioButton("Стиль 1")
        self.style1.setFixedWidth(400)
        # noinspection PyUnresolvedReferences
        self.style1.clicked.connect(lambda: self.on_style(1))

        self.style2 = QRadioButton("Стиль 2")
        self.style2.setFixedWidth(400)
        # noinspection PyUnresolvedReferences
        self.style2.clicked.connect(lambda: self.on_style(2))

        self.style3 = QRadioButton("Стиль 3")
        self.style3.setFixedWidth(400)
        # noinspection PyUnresolvedReferences
        self.style3.clicked.connect(lambda: self.on_style(3))

        self.back = QPushButton("Назад")
        # noinspection PyUnresolvedReferences
        self.back.clicked.connect(parent.on_leave_settings)
        self.style1.click()
        self.key_map = {
            Qt.Key_1: self.style1,
            Qt.Key_2: self.style2,
            Qt.Key_3: self.style3,
            Qt.Key_Backspace: self.back
        }

    @staticmethod
    def on_style(idx):
        for key, value in Settings.styles[idx-1].items():
            StylesheetStorage.change(key, value)
