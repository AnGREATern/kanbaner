import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5 import uic


class New(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('create.ui', self)






class Kanbaner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('personal.db')
        self.cur = self.con.cursor()
        self.pb_create.clicked.connect(self.create)
        self.pb_open.clicked.connect(self.open)
        self.pb_delete.clicked.connect(self.delete)
        self.pb_login.clicked.connect(self.login)
        self.title = []
        self.badTitle = []
        self.user = None
        self.crew = None

    def create(self):
        self.new = New()
        self.new.show()
        self.new.pb_complete.clicked.connect(self.vvod)

    def vvod(self):

        self.badTitle.extend([self.new.le2.text(), self.new.le3.text(), self.new.le4.text(), self.new.le5.text(),
                              self.new.le6.text(), self.new.le7.text(), self.new.le8.text(), self.new.le9.text()])

        for i in self.badTitle:
            if i:
                print(i)
                self.title.append(i)

        self.lw.addItems(self.title)
        self.title = []
        self.new.close()

    def open(self):
        pass

    def delete(self):
        pass

    def login(self):
        if self.pb_login.text() == 'Вход':
            self.user = self.le_login.text()
            self.crew = str(self.cur.execute('''SELECT SN FROM main''').fetchall())[3:-4].split("',), ('")
            if self.user in self.crew:
                self.pb_login.setText('Выход')
                self.le_login.hide()
                self.label.setText(self.user)
                self.label.resize(271, 21)
        else:
            self.label.setText('')
            self.label.resize(20, 21)
            self.le_login.show()
            self.pb_login.setText('Вход')


app = QApplication(sys.argv)
window = Kanbaner()
window.show()
app.exec_()
