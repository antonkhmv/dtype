from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton

from utils.stylesheet_storage import StylesheetStorage
from utils.window_template import WindowTemplate


def calc_speed(elapsed, num_entries, num_errors):
    return (num_entries - num_errors) / (elapsed + 1e-5)


class MainMenu(WindowTemplate):
    def __init__(self, parent):
        super(MainMenu, self).__init__(parent)
        self.logo = QLabel("dtype")

        self.box.addWidget(self.logo, Qt.AlignCenter)
        self.logo.setFixedSize(400, 70)
        StylesheetStorage.add_stylesheet_listener(self.logo, ["primary_color", "logo_font-size"])

        self.start = QPushButton("Начать тест")
        # noinspection PyUnresolvedReferences
        self.start.clicked.connect(self.parent.on_enter_select_mode)

        self.stat = QPushButton("Статистика")
        # noinspection PyUnresolvedReferences
        self.stat.clicked.connect(self.parent.on_enter_stats)

        self.settings = QPushButton("Настройки")

        self.key_map = {
            Qt.Key_1: self.start,
            Qt.Key_2: self.stat,
            Qt.Key_3: self.settings
        }


