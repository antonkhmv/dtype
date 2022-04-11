from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLayout, QLabel, QPushButton, QGridLayout

from utils.stylesheet_storage import StylesheetStorage


class WindowTemplate(QWidget):
    def __init__(self, parent):
        super(WindowTemplate, self).__init__()
        self.parent = parent

        def update_background(value):
            p = self.palette()
            p.setColor(self.backgroundRole(), QColor(value))
            self.setPalette(p)
            self.setAutoFillBackground(True)

        StylesheetStorage.add_listener(["secondary_color"], update_background)

        self.box = QVBoxLayout()
        self.box.setSizeConstraint(QLayout.SetFixedSize)
        self.grid = QGridLayout()
        self.grid.addLayout(self.box, 0, 0, Qt.AlignCenter)
        self.setLayout(self.grid)
        self.key_map = None
        self.buttons = None

    def keyPressEvent(self, a0) -> None:
        if a0.key() in self.key_map:
            self.key_map[a0.key()].click()

    def showEvent(self, a0):
        if self.buttons is None:
            self.buttons = self.key_map.values()

        for button in self.buttons:
            StylesheetStorage.add_stylesheet_listener(button,
                                                      ["secondary_color", "button_background-color", "button_font-size"])
            self.box.addWidget(button)

        self.move(self.parent.rect().center() - self.rect().center())
