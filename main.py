import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5 import uic
user = None


class Enter(QWidget):
    global user

    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.con = sqlite3.connect('personal.db')
        self.cur = self.con.cursor()
        self.pb_login.clicked.connect(self.switch)
        self.new = None
        self.crew = None

    def switch(self):
        global user
        user = self.le_login.text()
        self.crew = str(self.cur.execute('''SELECT SN FROM main''').fetchall())[3:-4].split("',), ('")
        if user in self.crew:
            self.new = Kanbaner()
            self.new.show()
            self.close()


class New(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('create.ui', self)






class Kanbaner(QMainWindow):
    global user

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('personal.db')
        self.cur = self.con.cursor()
        self.label.setText(user)
        self.pb_create.clicked.connect(self.create)
        self.pb_open.clicked.connect(self.open)
        self.pb_delete.clicked.connect(self.delete)
        self.pb_login.clicked.connect(self.exit)
        self.title = []
        self.badTitle = []
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

    def exit(self):
        exit()


app = QApplication(sys.argv)
window = Enter()
window.show()
app.exec_()
