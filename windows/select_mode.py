from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, QHBoxLayout

from utils.stylesheet_storage import StylesheetStorage
from utils.window_template import WindowTemplate


class SelectMode(WindowTemplate):
    def __init__(self, parent):
        super(SelectMode, self).__init__(parent)

        self.back = QPushButton("Назад")
        self.back.clicked.connect(lambda: self.parent.setCurrentWidget(self.parent.main_menu))
        self.mode = QLabel("Выбор режима")
        self.box.addWidget(self.mode, Qt.AlignCenter)
        self.mode.setFixedSize(400, 50)
        StylesheetStorage.add_stylesheet_listener(self.mode, ["primary_color", "button_font-size"])

        mode_box = QHBoxLayout()
        self.mode_group = QButtonGroup(mode_box)
        self.words = QRadioButton("Ограниченное количество слов")
        self.time = QRadioButton("Ограниченное время")
        self.quote = QRadioButton("Текст")
        mode_box.addWidget(self.words)
        self.mode_group.addButton(self.words)
        mode_box.addWidget(self.time)
        self.mode_group.addButton(self.time)
        self.mode_group.addButton(self.quote)
        self.words.click()
        self.box.addLayout(mode_box)
        self.box.addWidget(self.quote)
        self.mode_group.buttonToggled.connect(self.update_buttons)

        self.language = QLabel("Выберите язык")
        self.language.setFixedSize(400, 50)
        self.box.addWidget(self.language, Qt.AlignCenter)
        StylesheetStorage.add_stylesheet_listener(self.language, ["primary_color", "button_font-size"])

        lang_box = QHBoxLayout()
        self.lang_group = QButtonGroup(lang_box)
        self.english = QRadioButton("English")
        self.russian = QRadioButton("Русский")
        lang_box.addWidget(self.english)
        self.lang_group.addButton(self.english)
        lang_box.addWidget(self.russian)
        self.lang_group.addButton(self.russian)
        self.english.click()
        self.box.addLayout(lang_box)

        self.params = QLabel("Параметры")
        self.params.setFixedSize(400, 50)
        self.box.addWidget(self.params, Qt.AlignCenter)
        StylesheetStorage.add_stylesheet_listener(self.params, ["primary_color", "button_font-size"])
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
        self.box.addLayout(self.param_box)

        for radio_button in [self.english, self.russian, self.words, self.time, self.quote] + self.param_buttons:
            StylesheetStorage.add_stylesheet_listener(radio_button, ["stats_color", "radio_button_font-size"])

        self.setStyleSheet("QPushButton {margin-top: 10px !important;}")
        self.start = QPushButton("Начать тест")
        # noinspection PyUnresolvedReferences
        self.start.clicked.connect(self.parent.on_enter_test_page)

        self.key_map = {
            Qt.Key_Backspace: self.back,
            Qt.Key_1: self.words,
            Qt.Key_2: self.time,
            Qt.Key_3: self.english,
            Qt.Key_4: self.russian,
            Qt.Key_Return: self.start,
        }

        self.buttons = [self.start, self.back]

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

    def get_params(self):
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
        selected.append(int(self.param_group.checkedButton().text()))
        return tuple(selected)
