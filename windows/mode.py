import random
from pathlib import Path
from time import time

from PyQt5.QtCore import QTimer

from utils.stylesheet_storage import StylesheetStorage
from windows.input_widget import InputWidget
from windows.main_menu import calc_speed


class WordsMode(InputWidget):
    def __init__(self, parent, lang, word_len, width, line_count, scroll_margin):
        self.init_mode(lang, word_len)
        self.lang = lang
        super().__init__(parent, width, self.true_words, line_count, scroll_margin)
        StylesheetStorage.add_stylesheet_listener(self.stats, ["primary_color", "results_font-size"])
        self.stats_update = QTimer(self)
        self.stats_update.start(100)
        self.time = time()

    def init_mode(self, lang, word_len):
        self.true_words = None
        path = Path.cwd() / "data" / f"vocab_{'rus' if lang == 'russian' else 'eng'}.txt"
        with open(path, "r", encoding="utf-8-sig") as f:
            self.true_words = random.sample(f.read().split("\n"), k=word_len)

    def start_timer(self):
        # noinspection PyUnresolvedReferences
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
        super().__init__(parent, lang, 400, width, line_count, scroll_margin)

    def update_stats(self):
        elapsed, num_word, num_word_errors, num_chars, num_errors = self.get_metrics()
        self.stats.setText(f"{round(self.max_time - elapsed)}"
                           f" cек\t{round(calc_speed(elapsed, num_chars, num_errors) * 60)} сим/с")
        if self.max_time < elapsed:
            # noinspection PyUnresolvedReferences
            self.stats_update.timeout.disconnect(self.update_stats)
            self.parent.on_finished_test(self)


class QuoteMode(WordsMode):
    def __init__(self, parent, lang, width, line_count, scroll_margin):
        super().__init__(parent, lang, 0, width, line_count, scroll_margin)

    def init_mode(self, lang, word_len):
        self.true_words = None
        path = Path.cwd() / "data" / f"texts_{'rus' if lang == 'russian' else 'eng'}"
        filepath = random.choice(list(filter(Path.is_file, path.iterdir())))
        with open(filepath, "r", encoding="utf-8-sig") as f:
            self.true_words = " ".join(f.read().split("\n")).replace("  ", " ").split()
