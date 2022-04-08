import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget

from input_widget import InputWidget
from windows import MainMenu, Results


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
        self.removeWidget(test_page)
        results = Results(self, *test_page.get_metrics())
        self.addWidget(results)
        self.setCurrentWidget(results)

    def on_finished_results(self, results):
        self.removeWidget(results)
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
