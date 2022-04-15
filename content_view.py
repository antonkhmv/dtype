import sys
from datetime import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget

from db_manager import DBManager
from windows.data_view import DataView
from windows.input_widget import InputWidget
from windows.main_menu import MainMenu
from windows.results import Results
from windows.mode import WordsMode, TimeMode, QuoteMode
from windows.select_mode import SelectMode
from windows.settings import Settings


class ContentView(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.stats = DataView(self)
        self.results = None
        self.title = "dtype"
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 1200, 720)
        self.main_menu = MainMenu(self)
        self.select_mode = SelectMode(self)
        self.settings = Settings(self)
        self.addWidget(self.main_menu)
        self.db = DBManager()
        self.time = None
        self.input = None
        self.on_enter_select_mode()
        self.on_leave_select_mode()
        # self.on_enter_stats()
        # self.on_leave_stats()

    def setCurrentWidget(self, w: QWidget) -> None:
        super().setCurrentWidget(w)

    def keyPressEvent(self, event):
        curr_widget = self.currentWidget()
        if curr_widget is not None:
            curr_widget.keyPressEvent(event)

    def on_enter_select_mode(self):
        self.addWidget(self.select_mode)
        self.setCurrentWidget(self.select_mode)

    def on_leave_select_mode(self):
        self.removeWidget(self.select_mode)
        self.setCurrentWidget(self.main_menu)

    def on_leave_test(self):
        attrs = [self.input.back.clicked, self.input.stats_update.timeout, self.input.stats_update.timeout]
        funcs = [self.on_leave_test, self.input.update_stats, self.on_leave_test]
        for attr, func in zip(attrs, funcs):
            try:
                attr.disconnect(func)
            except:
                pass
        # try:
        #     self.input.back.clicked.disconnect(self.on_leave_test)
        #     self.input.stats_update.timeout.disconnect(self.input.update_stats)
        #     self.input.stats_update.timeout.connect(self.parent.on_leave_test)
        # except:
        #     pass
        self.removeWidget(self.input)
        # self.input.destroy()
        self.setCurrentWidget(self.select_mode)

    def on_enter_test_page(self):
        lang, mode, param = self.select_mode.get_params()
        if mode == "words":
            self.input = WordsMode(self, lang, param, 800, line_count=6, scroll_margin=2)
        elif mode == "time":
            self.input = TimeMode(self, lang, param, 800, line_count=6, scroll_margin=2)
            # self.input.time = time()
        elif mode == "quote":
            self.input = QuoteMode(self, lang, 800, line_count=6, scroll_margin=2)
        self.addWidget(self.input)
        self.setCurrentWidget(self.input)
        self.input.back.clearFocus()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        cw = self.currentWidget()
        if not isinstance(cw, DataView):
            cw.layout().setAlignment(Qt.AlignCenter)
        if isinstance(cw, InputWidget):
            cw.label_pos = cw.label.pos()

    def on_finished_test(self, test_page):
        self.results = Results(self, *test_page.get_metrics())
        self.db.write_data(test_page)
        self.addWidget(self.results)
        self.setCurrentWidget(self.results)
        self.removeWidget(test_page)

    def on_finished_results(self):
        self.results.back.clicked.disconnect(self.on_finished_results)
        self.removeWidget(self.results)
        self.setCurrentWidget(self.main_menu)

    def on_enter_stats(self):
        self.stats = DataView(self)
        self.addWidget(self.stats)
        self.setCurrentWidget(self.stats)
        self.stats.submit.click()

    def on_leave_stats(self):
        self.setCurrentWidget(self.main_menu)
        self.removeWidget(self.stats)

    def on_enter_settings(self):
        self.addWidget(self.settings)
        self.setCurrentWidget(self.settings)

    def on_leave_settings(self):
        self.setCurrentWidget(self.main_menu)
        self.removeWidget(self.settings)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ContentView()
    demo.show()
    sys.exit(app.exec_())
