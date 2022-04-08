from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLayout, QPushButton, QGridLayout

from global_storage import GlobalStorage


class MainMenu(QWidget):
    def __init__(self, parent):
        super(MainMenu, self).__init__()
        self.parent = parent
        self.setStyleSheet("""
        QPushButton {
            font-size: 30px;
        }
        """)

        def update_background(value):
            p = self.palette()
            p.setColor(self.backgroundRole(), QColor(value))
            self.setPalette(p)
            self.setAutoFillBackground(True)

        GlobalStorage.add_listener(["secondary_color"], update_background)

        self.box = QVBoxLayout()
        self.box.setSizeConstraint(QLayout.SetFixedSize)
        self.logo = QLabel("dtype")

        self.box.addWidget(self.logo, Qt.AlignCenter)
        self.logo.setFixedSize(400, 70)
        GlobalStorage.add_stylesheet_listener(self.logo, ["primary_color", "logo_font-size"])

        self.start = QPushButton("Начать тест")
        # noinspection PyUnresolvedReferences
        self.start.clicked.connect(self.parent.on_enter_test_page)
        self.box.addWidget(self.start)

        self.stat = QPushButton("Статистика")
        self.box.addWidget(self.stat)

        self.settings = QPushButton("Настройки")
        self.box.addWidget(self.settings)

        for button in [self.start, self.settings, self.stat]:
            GlobalStorage.add_stylesheet_listener(button, ["primary_color", "buttons_background-color"])

        self.grid = QGridLayout()
        self.grid.addLayout(self.box, 0, 0, Qt.AlignCenter)
        self.setLayout(self.grid)
        self.show()

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_1:
            self.start.click()
        elif a0.key() == Qt.Key_2:
            self.stat.click()

    def showEvent(self, a0):
        self.move(self.parent.rect().center() - self.rect().center())


def calc_speed(elapsed, num_entries, num_errors):
    return (num_entries - num_errors) / (elapsed + 1e-5)


class Results(QWidget):
    def __init__(self, parent, elapsed, num_words, num_word_errors, num_chars, num_errors):
        super(Results, self).__init__()
        self.parent = parent
        self.setStyleSheet("""
        QPushButton {
            font-size: 30px;
        }
        """)

        def update_background(value):
            p = self.palette()
            p.setColor(self.backgroundRole(), QColor(value))
            self.setPalette(p)
            self.setAutoFillBackground(True)

        GlobalStorage.add_listener(["secondary_color"], update_background)

        self.box = QVBoxLayout()
        self.box.setSizeConstraint(QLayout.SetFixedSize)
        self.info = QLabel(f"Всего слов: {num_words-num_word_errors} <br>"
                           f"Ошибок в символах: {num_errors} / {num_chars} символов <br>"
                           f"Ошибок в словах: {num_word_errors} / {num_words} слов <br>"
                           f"Скорость печати: {round(calc_speed(elapsed, num_chars, num_errors)*60)} символов/минуту <br>"
                           f"Точность: {round((1 - num_word_errors / num_words) * 100)}%")

        self.box.addWidget(self.info)
        self.info.setFixedSize(400, 250)

        self.again = QPushButton("Начать сначала")
        self.box.addWidget(self.again)
        self.again.clicked.connect(self.parent.on_enter_test_page)

        GlobalStorage.add_stylesheet_listener(self.info, ["primary_color", "results_font-size"])

        self.back = QPushButton("Назад в главное меню")
        # noinspection PyUnresolvedReferences
        self.back.clicked.connect(self.parent.on_finished_results)
        self.box.addWidget(self.back)

        for button in [self.back, self.again]:
            GlobalStorage.add_stylesheet_listener(button, ["primary_color", "buttons_background-color"])

        self.grid = QGridLayout()
        self.grid.addLayout(self.box, 0, 0, Qt.AlignCenter)
        self.setLayout(self.grid)
        self.show()

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_1:
            self.again.click()
        elif a0.key() == Qt.Key_2:
            self.back.click()

    def showEvent(self, a0):
        self.move(self.parent.rect().center() - self.rect().center())
