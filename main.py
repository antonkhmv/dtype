from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QBrush, QPainter, QColor, QPaintEvent, QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout

from dtype.global_storage import raw, GlobalStorage
from dtype.input_widget import InputWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "dtype"
        self.InitWindow()
        self.layout = QGridLayout()
        self.input = InputWidget(self, 800, line_count=7, scroll_margin=2)
        self.layout.addWidget(self.input, 1000, 1000)
        self.setLayout(self.layout)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.input.move(self.rect().center() - self.input.rect().center())

    def onFinishedText(self):
        pass

    def InitWindow(self):
        self.resize(1440, 1000)
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 1440, 1000)

    # def paintEvent(self, a0: QPaintEvent) -> None:
    #     self.input.paintEvent(a0)

    def keyPressEvent(self, event):
        self.input.keyPressEvent(event)
        # print('pressed from MainWindow: ', event.key())
        # self.keyPressed.emit(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())
