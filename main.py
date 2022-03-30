import sys

from PyQt5.QtWidgets import QApplication, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QGridLayout, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.uic.properties import QtGui
from PyQt5.Qt import Qt
from string import punctuation


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Widgets
        self.label = QLabel(text="Hi")
        self.label.setStyleSheet("font-size: 20px;")
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # Overlay
        self.label2 = QLabel(text="Hi")
        self.label2.setStyleSheet("font-size: 20px;")
        self.label2.setWordWrap(True)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.label2, 0, 0)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        self.setLayout(self.layout)

        self.setLayout(self.layout)

    def keyPressEvent(self, event):
        # modifiers = QtWidgets.QApplication.keyboardModifiers()
        # if modifiers == QtCore.Qt.ShiftModifier:
        #     print('Shift+Click')
        if event.key() == Qt.Key_Backspace:
            if event.modifiers() & Qt.ControlModifier:
                self.label.setText(" ".join(self.label.text().split(" ")[:-1]))
            else:
                self.label.setText(self.label.text()[:-1])
        else:
            print(punctuation)
            text = event.text()
            if text.isalpha() or text in set(r" !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"):
                self.label.setText(self.label.text() + event.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())
