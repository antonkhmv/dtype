import random
from time import time

from PyQt5.QtCore import QTimer, Qt

from global_storage import GlobalStorage
from input_widget import InputWidget
from windows import calc_speed


class TimeMode(InputWidget):
    def __init__(self, parent, max_time, width, line_count=6, scroll_margin=2):
        self.max_time = max_time
        true_words = None
        with open("./vocab.txt", "r") as f:
            true_words = random.sample(f.read().split("\n"), k=500)
        super().__init__(parent, width, true_words, line_count, scroll_margin)
        GlobalStorage.add_stylesheet_listener(self.stats, ["results_font-size"])
        self.stats_update = QTimer(self)
        self.stats_update.start(100)
        self.time = time()

    def update_stats(self):
        elapsed, num_word, num_word_errors, num_chars, num_errors = self.get_metrics()
        self.stats.setText(f"Времени осталось: {round(self.max_time - elapsed)}c. <br>"
                           f"Скорость: {round(calc_speed(elapsed, num_chars, num_errors) * 60)} сим/с")
        if self.max_time < elapsed:
            self.stats_update.timeout.disconnect(self.update_stats)
            self.parent.on_finished_test(self)

    def start_timer(self):
        self.stats_update.timeout.connect(self.update_stats)
        self.update_stats()
        self.label_pos = self.label.pos()
        self.repaint()
        # super(TimeMode, self).start_timer()


class WordsMode(InputWidget):
    def __init__(self, parent, word_len, width, line_count=6, scroll_margin=25):
        true_words = None
        with open("./vocab.txt", "r") as f:
            true_words = random.sample(f.read().split("\n"), k=word_len)
        super().__init__(parent, width, true_words, line_count, scroll_margin)
        GlobalStorage.add_stylesheet_listener(self.stats, ["results_font-size"])
        self.stats_update = QTimer(self)
        self.stats_update.start(100)
        self.time = time()

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        self.label_pos = self.label.pos()

    def update_stats(self):
        elapsed, num_word, num_word_errors, num_chars, num_errors = self.get_metrics()
        # self.label_pos = self.label.pos()
        self.stats.setText(f"Времени с начала: {round(elapsed)}c <br>"
                           f"Скорость: {round(calc_speed(elapsed, num_chars, num_errors) * 60)} сим/с")

    def start_timer(self):
        self.stats_update.timeout.connect(self.update_stats)
        self.update_stats()
        # super(TimeMode, self).start_timer()
