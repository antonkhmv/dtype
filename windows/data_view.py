from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QSplitter, QVBoxLayout, QWidget, QTableWidget, \
    QGridLayout, QTableWidgetItem, QHeaderView, QButtonGroup, QLabel, QRadioButton

from utils.stylesheet_storage import StylesheetStorage
from windows.main_menu import calc_speed


class DataView(QWidget):
    def __init__(self, parent):
        self.parent = parent
        self.table = None
        super().__init__(parent)

        self.box = QGridLayout()
        sidebar = QVBoxLayout()

        self.mode = QLabel("Выбор режима")
        sidebar.addWidget(self.mode, Qt.AlignCenter)
        self.mode.setFixedHeight(50)
        StylesheetStorage.add_stylesheet_listener(self.mode, ["primary_color", "radio_button_font-size"])

        self.mode_group = QButtonGroup(sidebar)
        self.words = QRadioButton("Ограниченное количество слов")
        self.time = QRadioButton("Ограниченное время")
        self.quote = QRadioButton("Текст")
        sidebar.addWidget(self.words)
        self.mode_group.addButton(self.words)
        sidebar.addWidget(self.time)
        self.mode_group.addButton(self.time)
        self.mode_group.addButton(self.quote)
        self.words.click()
        # sidebar.addLayout(mode_box)
        sidebar.addWidget(self.quote)
        self.mode_group.buttonToggled.connect(self.update_buttons)

        self.language = QLabel("Выберите язык")
        self.language.setFixedSize(200, 50)
        sidebar.addWidget(self.language, Qt.AlignCenter)
        StylesheetStorage.add_stylesheet_listener(self.language, ["primary_color", "radio_button_font-size"])

        lang_box = QHBoxLayout()
        self.lang_group = QButtonGroup(lang_box)
        self.english = QRadioButton("English")
        self.russian = QRadioButton("Русский")
        lang_box.addWidget(self.english)
        self.lang_group.addButton(self.english)
        lang_box.addWidget(self.russian)
        self.lang_group.addButton(self.russian)
        self.english.click()
        sidebar.addLayout(lang_box)

        self.params = QLabel("Параметры")
        self.params.setFixedSize(200, 50)
        sidebar.addWidget(self.params, Qt.AlignCenter)
        StylesheetStorage.add_stylesheet_listener(self.params, ["primary_color", "radio_button_font-size"])
        self.param_box = QHBoxLayout()
        self.param_group = QButtonGroup(self.param_box)

        self.param_buttons = []

        for i in range(4):
            button = QRadioButton()
            self.param_buttons.append(button)
            self.param_group.addButton(button)
            self.param_box.addWidget(button)
            pol = button.sizePolicy()
            pol.setRetainSizeWhenHidden(True)
            button.setSizePolicy(pol)

        # self.param_buttons[0].toggled
        self.param_buttons[1].click()
        self.update_buttons()
        sidebar.addLayout(self.param_box)

        for radio_button in [self.english, self.russian, self.words, self.time, self.quote] + self.param_buttons:
            StylesheetStorage.add_stylesheet_listener(radio_button, ["stats_color", "radio_button_font-size"])

        self.setStyleSheet("QPushButton {margin-top: 10px !important;}")
        self.start = QPushButton("Начать тест")
        # noinspection PyUnresolvedReferences
        self.start.clicked.connect(self.parent.on_enter_test_page)

        self.back = QPushButton("Назад")
        self.back.setFixedHeight(40)
        StylesheetStorage.add_stylesheet_listener(self.back,
                                                  ["secondary_color", "button_background-color",
                                                   "radio_button_font-size"])
        self.back.clicked.connect(lambda: self.parent.setCurrentWidget(self.parent.main_menu))

        self.submit = QPushButton("Применить")
        self.submit.setFixedHeight(40)
        StylesheetStorage.add_stylesheet_listener(self.submit,
                                                  ["secondary_color", "button_background-color",
                                                   "radio_button_font-size"])
        self.submit.clicked.connect(self.load_data)

        sidebar.addWidget(self.submit, Qt.AlignCenter)
        sidebar.addWidget(self.back, Qt.AlignCenter)

        self.sidebar_w = QWidget()
        self.sidebar_w.setLayout(sidebar)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.sidebar_w)
        self.table = QTableWidget(50, 8, self)
        self.table.setHorizontalHeaderLabels(
            ["Дата", "Язык", "Режим", "Параметр", "Скорость", "Точность", "Время", "Число символов"])
        self.splitter.addWidget(self.table)

        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem())
                self.table.item(i, j).setFlags(Qt.NoItemFlags)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.horizontalHeader().setFixedHeight(30)

        self.table.verticalHeader().setFixedWidth(30)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.splitter.setSizes([200, 800])
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        def update_background(background_color, table_color, header_color, primary_color):
            p = self.palette()
            p.setColor(self.backgroundRole(), QColor(background_color))
            self.setPalette(p)
            self.setAutoFillBackground(True)

            p = self.table.palette()
            p.setColor(QPalette.Base, QColor(table_color))
            self.table.setPalette(p)
            self.table.setAutoFillBackground(True)

            self.table.setStyleSheet(f"""
                QHeaderView::section {{
                 font-size: 14px;
                 background-color: {header_color};
                 color: {primary_color};
                }}
                QTableView QTableCornerButton::section {{
                 font-size: 14px;
                 background-color: {header_color};
                 color: {primary_color};
                 }}    
                 QTableWidget::item  {{
                 font-size: 14px;
                 color: {primary_color};
                 }}            
            """)

        self.box.addWidget(self.splitter, 0, 0)

        StylesheetStorage.add_listener(["secondary_color", "cell_color", "header_color", "primary_color"],
                                       update_background)

        def update_splitter(cell_color):
            self.splitter.setStyleSheet(f"QSplitter::handle {{ background: {cell_color}; }}")

        StylesheetStorage.add_listener(["secondary_color"], update_splitter)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.box)

    def load_data(self):
        names = {
            self.time: "time",
            self.words: "words",
            self.quote: "quote",
            self.english: "english",
            self.russian: "russian"
        }
        selected = []
        for group in [self.lang_group, self.mode_group]:
            item = ""
            for button in group.buttons():
                if group.id(button) == group.checkedId():
                    item = names[button]
            selected.append(item)
        lang, mode, param = selected + [int(self.param_group.checkedButton().text())]
        rows = self.parent.db.get_query(mode, lang, param)

        self.table.setRowCount(max(self.table.rowCount(), len(rows)))

        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                self.table.item(i, j).setText("")
        for i, row in enumerate(rows):
            _, timestamp, elapsed, num_chars, num_char_errors, num_words, num_word_errors, lang, mode = row
            param = ""
            if mode == 'W':
                param = num_words
            elif mode == 'T':
                param = int(elapsed)
            mode = dict(W="Слова", T="Время", Q="Тексты")[mode]
            lang = dict(ENG="English", RUS="Русский")[lang]
            self.table.item(i, 0).setText(timestamp)
            self.table.item(i, 1).setText(lang)
            self.table.item(i, 2).setText(mode)
            self.table.item(i, 3).setText(str(param))
            self.table.item(i, 4).setText("{:.1f}".format(60 * calc_speed(elapsed, num_chars, num_char_errors)))
            self.table.item(i, 5).setText("{:.1f}".format((1 - num_word_errors / num_words) * 100))
            self.table.item(i, 6).setText("{:.2f}".format(elapsed))
            self.table.item(i, 7).setText(str(num_chars))
        return tuple(selected)

    def update_buttons(self):
        params = [25, 50, 100, 200]
        if self.mode_group.id(self.words) == self.mode_group.checkedId():
            params = [25, 50, 100, 200]
        elif self.mode_group.id(self.time) == self.mode_group.checkedId():
            params = [15, 30, 60, 120]

        for button, param in zip(self.param_buttons, params):
            button.setText(str(param))

        if self.mode_group.id(self.quote) == self.mode_group.checkedId():
            for button in self.param_buttons + [self.params]:
                button.hide()
        else:
            for button in self.param_buttons + [self.params]:
                button.show()
