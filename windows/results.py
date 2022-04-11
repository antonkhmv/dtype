from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QLayout

from utils.stylesheet_storage import StylesheetStorage
from utils.window_template import WindowTemplate
from windows.main_menu import calc_speed


class Results(WindowTemplate):
    def __init__(self, parent, elapsed, num_words, num_word_errors, num_chars, num_errors):
        super(Results, self).__init__(parent)

        self.info = QLabel(f"Всего слов: {num_words} <br>"
                           f"Скорость печати: {round(calc_speed(elapsed, num_chars, num_errors)*60)} символов/минуту <br>"
                           f"Точность: {round((1 - num_word_errors / num_words) * 100)}% <br>"
                           f"Ошибок в символах: {num_errors} / {num_chars} символов <br>"
                           f"Ошибок в словах: {num_word_errors} / {num_words} слов <br>"
                           f"Времени затрачено: {elapsed:.1f} сек")

        StylesheetStorage.add_stylesheet_listener(self.info, ["primary_color", "results_font-size"])
        self.box.addWidget(self.info)
        self.info.setFixedSize(400, 200)

        self.again = QPushButton("Начать сначала")
        # noinspection PyUnresolvedReferences
        self.again.clicked.connect(self.parent.on_enter_test_page)

        self.back = QPushButton("Назад в главное меню")
        # noinspection PyUnresolvedReferences
        self.back.clicked.connect(self.parent.on_finished_results)

        self.box.setSpacing(12)

        self.key_map = {
            Qt.Key_1: self.again,
            Qt.Key_2: self.back,
        }
