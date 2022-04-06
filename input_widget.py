import copy
import itertools

from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTimer, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen, QPaintEvent, QShowEvent, QBrush, QColor
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout

from dtype.text_highlighting import HighlightedQLabel
from dtype.global_storage import GlobalStorage, raw


class InputWidget(QWidget):
    def __init__(self, parent, width, line_count, scroll_margin):
        super().__init__(parent=parent)
        self.parent = parent
        self.line_height = 0

        def update_line_height(value):
            self.line_height = 1.2 * float(raw(value, suffix="px"))

        GlobalStorage.add_listener("input_font_size", update_line_height)

        self.resize(width + 10, line_count * self.line_height + 18)
        # self.setGeometry(0, 0, width, height)

        self.true_words = "over the sunset at the edge of the atlas i'm driving" \
                          " alone when i see in the distance a light in the dark" \
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
        self.label = HighlightedQLabel(max_width=width, exp_words=self.words_expected,
                                       line_count=line_count, scroll_margin=scroll_margin)
        self.label.setStyleSheet(GlobalStorage.get("input_font_size"))
        # self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignLeft)

        # Overlay
        self.placeholder = QLabel(text=" ".join(self.words_expected))
        self.placeholder.lineWidth()

        def update_placeholder(value):
            self.placeholder.setStyleSheet(GlobalStorage.get("placeholder_color")
                                           + GlobalStorage.get("input_font_size"))

        GlobalStorage.add_listener("placeholder_color", update_placeholder)
        GlobalStorage.add_listener("input_font_size", update_placeholder)
        # self.placeholder.setWordWrap(True)
        self.placeholder.setAlignment(QtCore.Qt.AlignLeft)

        self.timer = QTimer(self)
        self.is_cursor_active = True

        def update_cursor():
            self.is_cursor_active = not self.is_cursor_active

        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(update_cursor)
        self.timer.start(500)

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.placeholder, 0, 0)
        self.layout.addWidget(self.label, 0, 0)
        self.setLayout(self.layout)

    def paintEvent(self, a0: QPaintEvent) -> None:
        pt = QPainter(self)
        cl = raw(GlobalStorage.get("primary_color"))
        fs = raw(GlobalStorage.get("input_font_size"), suffix="px")
        pt.setBrush(QColor(cl))
        tm, lm = 12, 8
        pt.drawRect(QRect(QPoint(self.label.cursor_pos + lm, self.label.current_line * self.line_height + tm),
                          QPoint(self.label.cursor_pos + lm + 1, self.label.current_line * self.line_height + int(fs) + tm)))
        self.update()

    def showEvent(self, a0: QShowEvent) -> None:
        self.updatePlaceholder()

    @staticmethod
    def common_prefix(word, word_expected):
        return sum(itertools.takewhile(lambda y: y, [x[0] == x[1] for x in zip(word, word_expected)]))

    def updatePlaceholder(self):
        last_ind = len(self.label.words) - 1
        if last_ind >= 0:
            real = self.label.words[last_ind]
            true = self.true_words[last_ind]
            self.words_expected[last_ind] = real + true[len(real):]
        breaks = self.label.get_word_breaks()
        placeholder = ""
        for i, word in enumerate(self.words_expected):
            placeholder += (" " * (i > 0)) + ("<br>" * breaks[i]) + word
        self.placeholder.setText(placeholder)

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
                self.label.remove_last_char()

            self.updatePlaceholder()

        elif event.key() == Qt.Key_Space:
            if self.label.words and self.words_expected:
                last_ind = len(self.label.words) - 1
                real = self.label.words[last_ind]
                if last_ind == len(self.words_expected):
                    self.parent.onWin(self)
                expected = self.words_expected[last_ind]
                if real == expected:
                    self.label.add_char(" ")
                else:
                    pref = InputWidget.common_prefix(real, expected)
                    self.label.add_char(expected[pref:])
                    self.label.add_highlighting(HighlightedQLabel.HighlightColors.blank_color, pref)
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
                    self.label.add_or_extend_highlighting(HighlightedQLabel.HighlightColors.error_color)
                self.updatePlaceholder()

        self.label.update_text()
        self.label.move(QPoint(0, self.label.scroll_pos * self.line_height))
