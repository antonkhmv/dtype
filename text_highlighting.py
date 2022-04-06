from collections import defaultdict
from enum import IntEnum
from html import escape
from itertools import takewhile

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QLabel

from .global_storage import GlobalStorage, raw


class HighlightedQLabel(QLabel):
    class HighlightColors(IntEnum):
        error_color = 0,
        blank_color = 1

    def __init__(self, exp_words, max_width, line_count, scroll_margin):
        super().__init__()
        self.word_highlights = defaultdict(lambda: [])
        self.words = []
        self.exp_words = exp_words
        self.max_width = max_width
        self.real_text = ""
        self.line_count = line_count
        self.scroll_margin = scroll_margin
        self.scroll_pos = 0
        self.cursor_pos = 0
        self.current_line = 0
        self.formats = []
        for i, name in enumerate(HighlightedQLabel.HighlightColors):
            def update(value):
                self.formats[i] = value
            self.formats.append("")
            GlobalStorage.add_listener(name.name, update)

    def add_new_word(self, word):
        self.words.append(word)

    def remove_word(self):
        if not self.words:
            return
        self.remove_highlighting()
        self.words.pop()

    def empty_last_word(self):
        if not self.words:
            return
        self.remove_highlighting()
        self.words[-1] = ""

    def remove_last_char(self):
        if not self.words:
            return
        if len(self.words[-1]) == 0:
            self.remove_word()
        else:
            self.words[-1] = self.words[-1][:-1]

    def add_char(self, text):
        if text == " ":
            self.add_new_word("")
        else:
            if not self.words:
                self.add_new_word(text)
            else:
                self.words[-1] += text

    def add_highlighting(self, color: HighlightColors, start_index=None, end_index=None, index=None):
        if index is None:
            index = len(self.words) - 1
        if end_index is None:
            end_index = len(self.words[-1])
        if start_index is None:
            start_index = len(self.words[-1]) - 1
        self.word_highlights[index].append((start_index, end_index, color))

    def add_or_extend_highlighting(self, color: HighlightColors):
        word_index = len(self.words) - 1
        char_index = len(self.words[-1]) - 1
        for i, (st, end, cl) in enumerate(self.word_highlights[word_index]):
            if end == char_index:
                self.word_highlights[word_index][i] = (st, char_index + 1, color)
                return
        self.add_highlighting(color)

    def remove_highlighting(self, index=None):
        if index is None:
            index = len(self.words) - 1
        if index in self.word_highlights:
            del self.word_highlights[index]

    def get_size_of_blank(self):
        last_index = len(self.words) - 1
        if last_index in self.word_highlights:
            for (start, end, color) in self.word_highlights[last_index]:
                if end == len(self.words[last_index]) and color == HighlightedQLabel.HighlightColors.blank_color:
                    return end - start
        return None

    def get_word_breaks(self):
        result = [False] * len(self.exp_words)
        string = ""
        for i, word in enumerate(self.exp_words):
            string += (" " if i > 0 else "") + word
            if self.fontMetrics().boundingRect(string).width() > self.max_width:
                string = word
                result[i] = True
            else:
                result[i] = False
        return result

    def update_text(self):
        result = ""
        breaks = self.get_word_breaks()
        for i, word in enumerate(self.words):
            result += " " * (i > 0)
            result += "<br>" * breaks[i]
            if i in self.word_highlights:
                last_end = 0
                for j, highlight in enumerate(list(self.word_highlights[i])):
                    start, end, color = highlight
                    if end > len(word):
                        if start >= len(word):
                            del self.word_highlights[i][j]
                            continue
                        else:
                            self.word_highlights[i][j] = (start, min(end, len(word)), color)
                    css = self.formats[color.value]
                    result += word[last_end:start]
                    result += f"<font style=\"{escape(css)}\">{escape(word[start:end])}</font>"
                    last_end = end
                result += word[last_end:]
            else:
                result += word
        last_str = ""
        for i in range(len(self.words)):
            last_str += " " * (i > 0) + self.words[-1-i]
            if breaks[len(self.words)-1-i]:
                break
        if last_str and last_str[-1] == " ":
            last_str = last_str[:-1] + "t"
        self.cursor_pos = self.fontMetrics().boundingRect(last_str).width()
        self.current_line = sum(breaks[:len(self.words)])
        if self.scroll_pos + self.current_line >= self.line_count - self.scroll_margin:
            self.scroll_pos -= 1
        if self.scroll_pos + self.current_line <= self.scroll_margin:
            self.scroll_pos += 1
        super().setText(result)
