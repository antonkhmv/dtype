import sqlite3
from pathlib import Path
import time

from PyQt5.QtWidgets import QMessageBox

from windows.input_widget import InputWidget
from windows.mode import QuoteMode, TimeMode


class DBManager:
    def __init__(self):
        try:
            path = Path.cwd() / "data" / "tests.sqlite"
            if not path.exists():
                path.touch()
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tests (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TIMESTAMP TIMESTAMP NOT NULL,
                    ELAPSED NUMERIC(8, 2) NOT NULL,
                    NUM_CHARS INT NOT NULL,
                    NUM_CHAR_ERRORS INT NOT NULL,
                    NUM_WORDS INT NOT NULL,
                    NUM_WORD_ERRORS INT NOT NULL,
                    LANG TEXT CHECK( LANG IN ('RUS', 'ENG') ) NOT NULL,
                    MODE TEXT CHECK( MODE IN ('W','T','Q') ) NOT NULL
                )
            """)
            self.connection.commit()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('База данных недосупна')
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        # query = "SELECT * FROM test_table WHERE  LIMIT 50"

    def write_data(self, test_page: InputWidget):
        elapsed, num_words, num_word_errors, num_chars, num_char_errors = test_page.get_metrics()
        mode = 'W'
        if isinstance(test_page, TimeMode):
            mode = 'T'
        elif isinstance(test_page, QuoteMode):
            mode = 'Q'
        lang = dict(russian='RUS', english='ENG')[test_page.lang]
        query = f"INSERT INTO " \
                f"tests(TIMESTAMP, ELAPSED, NUM_CHARS, NUM_CHAR_ERRORS, NUM_WORDS, NUM_WORD_ERRORS, LANG, MODE)" \
                f" VALUES (datetime('now', 'localtime'), {elapsed:.2f}, {num_chars}, {num_char_errors}, {num_words}," \
                f" {num_word_errors}, '{lang}', '{mode}')"
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('База данных недосупна')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def get_query(self, mode, lang, params):
        mode = dict(words='W', time='T', quote='Q')[mode]
        lang = dict(russian='RUS', english='ENG')[lang]
        suffix = ""
        if mode == 'W':
            suffix = f" AND NUM_WORDS = {params}"
        elif mode == 'T':
            suffix = f" AND ROUND(ELAPSED) = {params}"
        result = []
        try:
            result = list(self.cursor.execute(f"SELECT * from tests where MODE = '{mode}' AND LANG = '{lang}'" + suffix))
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('База данных недосупна')
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        return result
