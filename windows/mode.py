import random
from pathlib import Path
from time import time
from typing import Union

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from utils.stylesheet_storage import StylesheetStorage
from windows.input_widget import InputWidget
from windows.main_menu import calc_speed


class WordsMode(InputWidget):
    stats_update: Union[QTimer, None]

    def __init__(self, parent, lang, word_len, width, line_count, scroll_margin):
        self.lang = lang
        self.word_len = word_len
        self.width = width
        self.line_count = line_count
        self.scroll_margin = scroll_margin
        self.parent = parent
        self.init_mode()
        is_none = False
        if self.true_words is None:
            self.true_words = ['']
            is_none = True
        super().__init__(self.parent, self.width, self.true_words, self.line_count, self.scroll_margin)
        self.stats_update = QTimer(self)
        self.stats_update.start(100)
        self.time = 0
        if is_none:
            self.stats_update.timeout.connect(self.parent.on_leave_test)
        StylesheetStorage.add_stylesheet_listener(self.stats, ["primary_color", "results_font-size"])

    def load_data(self):
        path = Path.cwd() / "data" / f"vocab_{'rus' if self.lang == 'russian' else 'eng'}.txt"
        with open(path, "r", encoding="utf-8-sig") as f:
            self.true_words = random.sample(f.read().split("\n"), k=self.word_len)

    def init_mode(self):
        self.true_words = None
        try:
            self.load_data()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Файл не доступен')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def start_timer(self):
        # noinspection PyUnresolvedReferences
        self.time = time()
        self.stats_update.timeout.connect(self.update_stats)
        self.update_stats()
        self.label_pos = self.label.pos()
        self.repaint()

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        self.label_pos = self.label.pos()

    def update_stats(self):
        elapsed, num_word, num_word_errors, num_chars, num_errors = self.get_metrics()
        self.stats.setText(f"{round(elapsed)} cек\t{round(calc_speed(elapsed, num_chars, num_errors) * 60)} сим/с")


class TimeMode(WordsMode):
    def __init__(self, parent, lang, max_time, width, line_count, scroll_margin):
        self.max_time = max_time
        self.timer_stopped = False
        super().__init__(parent, lang, 400, width, line_count, scroll_margin)

    def update_stats(self):
        elapsed, num_word, num_word_errors, num_chars, num_errors = self.get_metrics()
        self.stats.setText(f"{round(self.max_time - elapsed)}"
                           f" cек\t{round(calc_speed(elapsed, num_chars, num_errors) * 60)} сим/с")
        if elapsed > self.max_time and not self.timer_stopped:
            # noinspection PyUnresolvedReferences
            self.stats_update.timeout.disconnect(self.update_stats)
            self.parent.on_finished_test(self)
            self.timer_stopped = True


class QuoteMode(WordsMode):
    def __init__(self, parent, lang, width, line_count, scroll_margin):
        super().__init__(parent, lang, 0, width, line_count, scroll_margin)

    def load_data(self):
        path = Path.cwd() / "data" / f"texts_{'rus' if self.lang == 'russian' else 'eng'}"
        filepath = random.choice(list(filter(Path.is_file, path.iterdir())))
        with open(filepath, "r", encoding="utf-8-sig") as f:
            self.true_words = " ".join(f.read().split("\n")).replace("  ", " ").split()
