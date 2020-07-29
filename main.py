import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5 import uic
user = None


class Enter(QWidget):
    global user

    def __init__(self):
        super().__init__()
        uic.loadUi('C://Users//Максим//PycharmProjects//kanbaner1//login.ui', self)
        self.con = sqlite3.connect('C://Users//Максим//PycharmProjects//kanbaner1//personal.db')
        self.cur = self.con.cursor()
        self.pb_login.clicked.connect(self.switch)
        memory = open('C://Users//Максим//PycharmProjects//kanbaner1//memory.txt', 'r')
        self.le_login.setText(memory.read())
        memory.close()
        self.new = None
        self.crew = None

    def switch(self):
        global user
        user = self.le_login.text()
        self.crew = str(self.cur.execute('''SELECT SN FROM main''').fetchall())[3:-4].split("',), ('")
        if user in self.crew:
            memory = open('memory.txt', 'w')
            memory.write(user)
            memory.close()
            self.new = Kanbaner()
            self.new.show()
            self.close()


class New(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('C://Users//Максим//PycharmProjects//kanbaner1//create.ui', self)



class Kanbaner(QMainWindow):
    global user

    def __init__(self):
        super().__init__()
        uic.loadUi('C://Users//Максим//PycharmProjects//kanbaner1//main.ui', self)
        self.con = sqlite3.connect('C://Users//Максим//PycharmProjects//kanbaner1//personal.db')
        self.cur = self.con.cursor()
        self.label.setText(user)
        self.pb_create.clicked.connect(self.create)
        self.pb_open.clicked.connect(self.open)
        self.pb_delete.clicked.connect(self.delete)
        self.pb_login.clicked.connect(self.exit)
        self.title = ''
        self.rowTitles = []
        self.crew = None

    def create(self):
        self.new = New()
        self.new.show()
        self.new.pb_complete.clicked.connect(self.vvod)

    def vvod(self):

        self.rowTitles.extend([self.new.le2.text(), self.new.le3.text(), self.new.le4.text(), self.new.le5.text(),
                              self.new.le6.text(), self.new.le7.text(), self.new.le8.text(), self.new.le9.text()])
        self.title = self.new.leName.text()

        self.lw.addItem(self.title)
        self.title = ''
        self.new.close()

    def open(self):
        pass

    def delete(self):
        if [x.row() for x in self.lw.selectedIndexes()]:
            self.lw.takeItem(int(str([x.row() for x in self.lw.selectedIndexes()])[1]))

    def exit(self):
        exit()


app = QApplication(sys.argv)
window = Enter()
window.show()
app.exec_()
