import copy
import itertools
from time import time

from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTimer, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen, QPaintEvent, QShowEvent, QBrush, QColor
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QVBoxLayout, QLayout

from text_highlighting import HighlightedQLabel
from global_storage import GlobalStorage


class InputWidgetWrapper(QWidget):
    def __init__(self, parent, width, line_count, scroll_margin):
        super().__init__(parent)
        self.input = InputWidget(self, width, line_count, scroll_margin)
        self.input.stackUnder(self)
        layout = QGridLayout()
        layout.addWidget(self.input)
        self.setLayout(self.input.box)


class InputWidget(QWidget):
    def __init__(self, parent, width, true_words=None, line_count=6, scroll_margin=2):
        super().__init__(parent=parent)
        self.parent = parent
        self.line_height = 0
        self.font_size = None
        self.cursor_color = None

        def update_params(font_size, cursor_color):
            font_size = int(font_size.rstrip("px"))
            self.line_height = 1.2 * font_size
            self.font_size = font_size
            self.cursor_color = cursor_color

        GlobalStorage.add_listener(["input_font-size", "cursor_color"], update_params)

        self.true_words = true_words
        self.true_words = "over the sunset at the edge of the atlas i'm driving alone when" \
                          " i see in the distance a light in the dark" \
                          " and when i approach it a note on the glass we're serving" \
                          " inside it's quiet but the tables are shining with blue chrome" \
                          " and white with a fan on above but no service in sight" \
                          " i pick out a booth sliding in from the side" \
                          " and then i start feeling quite tired so i know that i'll be here a little" \
                          " while when i go i'll get right back on the road" \
                          " let everybody come together the world at peace as one we could live a dream forever" \
                          " its really up to us and if you're not sure how to start then open up " \
                          " you heart let the feeling grow and soon you're sure to know light up light up" \
                          " the whole night sky with all your love just say the prayer we'll make it there if we" \
                          " work hard enough keep on keep on and give it everything you've got 'cos only then we'll" \
                          " reach the end the land where we belong so when we walk among the clouds hold your neighbor" \
                          " close as the trumpets echo round you don't wanna be a-".split()

        self.words_expected = copy.copy(self.true_words)


        # Widgets
        self.label = HighlightedQLabel(self, exp_words=self.words_expected, max_width=width, line_count=line_count,
                                       scroll_margin=scroll_margin)

        GlobalStorage.add_stylesheet_listener(self.label, ["input_font-size"])
        self.label.setAlignment(Qt.AlignLeft)

        # Overlay
        self.placeholder = QLabel(text=" ".join(self.words_expected))
        self.placeholder.lineWidth()

        GlobalStorage.add_stylesheet_listener(self.placeholder, ["placeholder_color", "input_font-size"])

        # self.placeholder.setWordWrap(True)
        self.placeholder.setAlignment(Qt.AlignLeft)
        self.resize(width, line_count * self.line_height + 18)
        # Layout
        self.label_pos = self.label.pos()
        self.grid = QGridLayout()
        self.box = QGridLayout()
        self.box.setSizeConstraint(QLayout.SetFixedSize)
        self.label.setFixedSize(width, line_count * self.line_height)
        self.placeholder.setFixedSize(width, line_count * self.line_height)
        self.box.addWidget(self.placeholder, 0, 0)
        self.box.addWidget(self.label, 0, 0)
        self.grid.addLayout(self.box, 0, 0, Qt.AlignCenter)
        self.setLayout(self.grid)
        self.show()

        def update_cursor():
            self.is_cursor_active = (self.is_cursor_active + 1) % 5
            self.update()

        self.cursor_timer = QTimer(self)
        self.is_cursor_active = 0
        # noinspection PyUnresolvedReferences
        self.cursor_timer.timeout.connect(update_cursor)
        self.cursor_timer.start(300)

        def update_stats():
            pass

        self.stats_update = QTimer(self)
        self.stats_update.timeout.connect(update_stats)
        self.stats_update.start(100)
        self.time = time()

    def paintEvent(self, a0: QPaintEvent) -> None:
        pt = QPainter(self)
        cl = QColor(self.cursor_color)
        pen = QPen()
        brush = QBrush(cl)
        pen.setBrush(brush)
        pt.setBrush(brush)
        pt.setPen(pen)
        # pt.setBackgroundMode(Qt.BGMode.OpaqueMode)
        pt.setBackground(QColor(self.cursor_color))
        tm, lm = self.label_pos.y() + self.line_height/10, self.label_pos.x()-2
        label = self.label
        if self.is_cursor_active < 3:
            pt.drawRect(QRect(QPoint(label.cursor_pos + lm, (label.current_line-label.scroll_pos) * self.line_height + tm),
                              QPoint(label.cursor_pos + lm + 1,
                                     (label.current_line-label.scroll_pos) * self.line_height + self.font_size + tm)))

    def showEvent(self, a0: QShowEvent) -> None:
        self.update_placeholder()
        self.label_pos = self.label.pos()
        # self.parent.resizeEvent(None)

    @staticmethod
    def common_prefix(word, word_expected):
        return sum(itertools.takewhile(lambda y: y, [x[0] == x[1] for x in zip(word, word_expected)]))

    def update_placeholder(self):
        last_ind = len(self.label.words) - 1
        if last_ind >= 0:
            real = self.label.words[last_ind]
            true = self.true_words[last_ind]
            self.words_expected[last_ind] = real + true[len(real):]
        breaks = self.label.get_word_breaks()
        breaks = " ".join(breaks)
        self.placeholder.setText("<br>".join(breaks.split("<br>")[self.label.scroll_pos:]))

    def calc_speed(self, elapsed, num_entries, num_errors):
        return (num_entries - num_errors) / (elapsed + 1e-5)

    def get_metrics(self):
        num_words = len(self.label.words)
        num_words_with_errors = len(self.label.word_highlights)
        num_errors = sum(sum(end-start for (start, end, _) in highlight)
                         for highlight in self.label.word_highlights.values())
        num_chars = len("".join(self.label.words))
        elapsed = time() - self.time
        return elapsed, num_words, num_words_with_errors, num_chars, num_errors

    def keyPressEvent(self, event):
        # modifiers = QtWidgets.QApplication.keyboardModifiers()
        # if modifiers == QtCore.Qt.ShiftModifier:
        #     print('Shift+Click')
        if event.key() == Qt.Key_Backspace:
            if event.modifiers() & Qt.ControlModifier:
                if len(self.label.words) > 1 and not self.label.words[-1]:
                    self.label.words.pop()
                self.label.empty_last_word()
            else:
                if self.label.words and len(self.label.words[-1]) == 0:
                    self.label.remove_highlighting()
                    self.label.remove_word()
                    size = self.label.get_size_of_blank()
                    if size is not None:
                        for _ in range(size - 1):
                            self.label.remove_last_char()
                    else:
                        self.label.add_char(" ")
                self.label.remove_last_char()

            self.update_placeholder()

        elif event.key() == Qt.Key_Space:
            if self.label.words and self.words_expected:
                last_ind = len(self.label.words) - 1
                real = self.label.words[last_ind]
                if last_ind >= len(self.words_expected) - 1:
                    self.parent.on_finished_test(self)
                    return
                expected = self.words_expected[last_ind]
                if real != expected:
                    pref = InputWidget.common_prefix(real, expected)
                    self.label.add_char(expected[pref:])
                    self.label.add_highlighting("blank_color", pref)
                self.label.add_char(" ")
        else:
            text = event.text()
            if text.isalnum() or text in set(r" !\"#$%&'()*+,-./:;=?@[\]^_`{|}~"):
                self.label.add_char(text)
                # self.label.remove_highlighting()
                last_ind = len(self.label.words) - 1
                real = self.label.words[last_ind]
                true = self.true_words[last_ind]
                real_index = len(real) - 1
                if len(real) > len(true) or real[real_index] != true[real_index]:
                    self.label.add_or_extend_highlighting("error_color")
                self.update_placeholder()

        self.label.update_text()
        self.label.update()
        self.is_cursor_active = True
        self.update()
        #self.label.move(QPoint(0, self.label.scroll_pos * self.line_height))