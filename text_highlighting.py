from collections import defaultdict
from html import escape

from PyQt5.QtWidgets import QLabel
import sys
from global_storage import GlobalStorage


class HighlightedQLabel(QLabel):

    def __init__(self, parent, exp_words, max_width, line_count, scroll_margin):
        super().__init__()
        self.parent = parent
        self.colors = dict(
            error_color=0,
            blank_color=1
        )
        GlobalStorage.add_dict_listener(self.colors)
        # self.colors = list(self.color_values.keys())
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

    def get_space_length(self):
        if sys.platform == 'win32':
            return int(int(GlobalStorage.get("input_font-size").rstrip("px")) * 0.27)
        elif sys.platform == 'darwin':
            return int(int(GlobalStorage.get("input_font-size").rstrip("px")) * 0.25)

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

    def add_highlighting(self, color, start_index=None, end_index=None, index=None):
        if index is None:
            index = len(self.words) - 1
        if end_index is None:
            end_index = len(self.words[-1])
        if start_index is None:
            start_index = len(self.words[-1]) - 1
        self.word_highlights[index].append((start_index, end_index, color))

    def add_or_extend_highlighting(self, color):
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
                if end == len(self.words[last_index]) and color == "blank_color":
                    return end - start
        return None

    def get_word_breaks(self):
        result = []
        space_size = self.get_space_length()
        string = ""
        i = 0
        for word in self.exp_words:
            string += word
            if self.fontMetrics().boundingRect(string).width() + i * space_size > self.max_width:
                string = word
                i = 0
                word = "<br>" + word
            i += 1
            result.append(word)
        return result

    def update_text(self):
        space_size = self.get_space_length() #int(int(GlobalStorage.get("input_font-size").rstrip("px")) * 0.25)
        result = []
        last_str = []
        breaks = self.get_word_breaks()
        for i, (exp, word) in enumerate(zip(breaks, self.words)):
            r = word
            if i in self.word_highlights:
                last_end = 0
                r = ""
                for j, highlight in enumerate(self.word_highlights[i]):
                    start, end, color = highlight
                    if end > len(word):
                        if start >= len(word):
                            del self.word_highlights[i][j]
                            continue
                        else:
                            self.word_highlights[i][j] = (start, min(end, len(word)), color)
                    r += escape(word[last_end:start])
                    r += f"<font color=\"{self.colors[color]}\">{escape(word[start:end])}</font>"
                    last_end = end
                r += escape(word[last_end:])
            if exp.startswith("<br>"):
                r = "<br>" + r
                last_str = [word]
            else:
                last_str.append(word)
            result.append(r)
        result = " ".join(result)
        self.cursor_pos = max(0, len(last_str)-1) * space_size
        last_str = "".join(last_str)
        self.cursor_pos += self.fontMetrics().boundingRect(last_str).width()
        line_pos = result.count("<br>")
        if self.current_line != line_pos:
            self.current_line = line_pos
            if self.current_line - self.scroll_pos >= self.line_count - self.scroll_margin:
                self.scroll_pos += 1
            elif self.scroll_pos > 0 and self.current_line - self.scroll_pos <= self.scroll_margin:
                self.scroll_pos -= 1
            self.parent.update_placeholder()
        super().setText("<br>".join(result.split("<br>")[self.scroll_pos:]))
