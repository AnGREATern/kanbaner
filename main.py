import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic


class New(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('create.ui', self)
        self.title = []
        self.pb_complete.clicked.connect(self.vvod)

    def vvod(self):
        self.title.extend([self.le2.text(), self.le3.text(), self.le4.text(), self.le5.text(),
                          self.le6.text(), self.le7.text(), self.le8.text(), self.le9.text()])
        a = ''
        for i in range(8):
            if self.title[i] == '':
                a += str(i)
        a = a[::-1]
        for i in range(len(a)):
            del self.title[int(a[i])]


class Kanbaner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pb_create.clicked.connect(self.create)
        self.pb_open.clicked.connect(self.open)
        self.pb_delete.clicked.connect(self.delete)

    def create(self):
        self.new = New()
        self.new.show()

    def open(self):
        pass

    def delete(self):
        pass


app = QApplication(sys.argv)
window = Kanbaner()
window.show()
app.exec_()
