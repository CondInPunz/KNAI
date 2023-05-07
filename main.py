import sys
import threading

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QSize, pyqtSignal

import requester
import scanner


class Client(QMainWindow):
    show_request = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi("main_window.ui", self)
        self.show_request.connect(self.show_string)
        self.submit.clicked.connect(self.bebra)

    def bebra(self):
        def mini_bebra():
            try:
                self.sentence_quantity = self.output_size_sent.text()
                print(self.sentence_quantity)
                self.file_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
                if self.file_name == "":
                    return
                output = scanner.scan(self.file_name)
                output = requester.request(output, self.sentence_quantity)
                self.show_request.emit(output)
            except Exception as e:
                print(e)

        threading.Thread(target=mini_bebra).start()

    def show_string(self, s):
        print(s)
        self.output_window.setText(s)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec())
