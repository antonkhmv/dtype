import sys
from time import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QLabel, QWidget, QStackedWidget, QPushButton, \
    QVBoxLayout, QLayout

from input_widget import InputWidget


class MainMenu(QWidget):
    def __init__(self, parent):
        super(MainMenu, self).__init__()
        self.parent = parent
        self.setStyleSheet("""
        QPushButton {
            font-size: 30px;
        }
        """)
        self.box = QVBoxLayout()
        self.box.setSizeConstraint(QLayout.SetFixedSize)
        self.logo = QLabel("dtype")

        self.box.addWidget(self.logo, Qt.AlignCenter)
        self.logo.setFixedSize(400, 70)
        self.logo.setStyleSheet("font-size: 50px;")

        self.start = QPushButton("Start test")
        self.start.clicked.connect(self.parent.on_enter_test_page)
        self.box.addWidget(self.start)

        self.stat = QPushButton("Statistics")
        self.box.addWidget(self.stat)

        self.settings = QPushButton("Settings")
        self.box.addWidget(self.settings)

        self.grid = QGridLayout()
        self.grid.addLayout(self.box, 0, 0, Qt.AlignCenter)
        self.setLayout(self.grid)
        self.show()

    def showEvent(self, a0):
        self.move(self.parent.rect().center() - self.rect().center())


class ContentView(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.title = "dtype"
        self.init_window()
        self.main_menu = MainMenu(self)

        self.addWidget(self.main_menu)
        self.time = None
        self.input = None

    def on_enter_test_page(self):
        self.input = InputWidget(self, 600, true_words=None, line_count=6, scroll_margin=2)
        self.addWidget(self.input)
        self.setCurrentWidget(self.input)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        cw = self.currentWidget()
        cw.layout().setAlignment(Qt.AlignCenter)
        if isinstance(cw, InputWidget):
            cw.label_pos = cw.label.pos()

    def on_finished_test(self, test_page):
        elapsed, _, _, num_chars, num_errors = test_page.get_metrics()
        # self.removeWidget(self.main_menu)
        self.removeWidget(test_page)
        # self.main_menu = MainMenu(self)
        # self.addWidget(self.main_menu)
        self.setCurrentWidget(self.main_menu)

    def init_window(self):
        # self.resize(1000, 500)
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 1000, 600)

    # def paintEvent(self, a0: QPaintEvent) -> None:
    #     self.input.paintEvent(a0)

    def setCurrentWidget(self, w: QWidget) -> None:
        super().setCurrentWidget(w)

    def keyPressEvent(self, event):
        curr_widget = self.currentWidget()
        if curr_widget is not None:
            curr_widget.keyPressEvent(event)
        # print('pressed from MainWindow: ', event.key())
        # self.keyPressed.emit(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ContentView()
    demo.show()
    sys.exit(app.exec_())
