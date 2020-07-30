import datetime
import sys
import sqlite3
import time

from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QTreeWidgetItem, QTreeWidget, \
    QHeaderView, QLineEdit, QPushButton, QComboBox, QTableWidget, QDateTimeEdit
from PyQt5 import uic, QtCore, QtGui, QtWidgets

user = None
con = sqlite3.connect('C://Users//Максим//PycharmProjects//kanbaner1//personal.db')
cur = con.cursor()
table_row = int(str(cur.execute('''SELECT id FROM finance''').fetchall()[-1])[1:-2]) + 1


class Enter(QWidget):
    global user, con, cur

    def __init__(self):
        super().__init__()
        uic.loadUi('C://Users//Максим//PycharmProjects//kanbaner1//login.ui', self)
        self.pb_login.clicked.connect(self.switch)
        memory = open('C://Users//Максим//PycharmProjects//kanbaner1//memory.txt', 'r')
        self.le_login.setText(memory.read())
        memory.close()
        self.new = None
        self.crew = None

    def switch(self):
        global user, con, cur
        user = self.le_login.text()
        self.crew = str(cur.execute('''SELECT SN FROM main''').fetchall())[3:-4].split("',), ('")
        if user in self.crew:
            memory = open('C://Users//Максим//PycharmProjects//kanbaner1//memory.txt', 'w')
            memory.write(user)
            memory.close()
            self.new = Kanbaner()
            self.new.show()
            self.close()

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.switch()


class New(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('C://Users//Максим//PycharmProjects//kanbaner1//create.ui', self)


class Task(QWidget):
    def __init__(self, rowTitles):
        super().__init__()
        uic.loadUi('C://Users//Максим//PycharmProjects//kanbaner1//tasks.ui', self)
        self.pb_addT.clicked.connect(self.addTask)
        self.c_num = 0
        self.tabs = []
        self.cbs = [[] for _ in range(len(rowTitles))]
        self.dts = [[] for _ in range(len(rowTitles))]
        self.dtss = [[] for _ in range(len(rowTitles))]
        self.pbs = [[] for _ in range(len(rowTitles))]
        self.cbss = [[] for _ in range(len(rowTitles))]
        for i in range(len(rowTitles)):
            self.tabs.append(QTableWidget(self))
            self.tabs[i].setFont(QFont('Segoe UI', 12))
            self.tabs[i].setColumnCount(5)
            header = self.tabs[i].horizontalHeader()
            for y in range(5):
                header.setSectionResizeMode(y, QtWidgets.QHeaderView.Stretch)
            self.tabs[i].setHorizontalHeaderLabels(['Исполнитель', 'Время выдачи', 'Срок сдачи',
                                                    'Задача/чат', 'Статус'])
            self.tabWidget.addTab(self.tabs[i], rowTitles[i])

    def addTask(self):
        self.c_num = self.tabWidget.currentIndex()
        rowNum = self.tabs[self.c_num].rowCount()
        if rowNum != 0:
            self.tabs[self.c_num].insertRow(0)
        else:
            self.tabs[self.c_num].setRowCount(1)
        self.cbs[self.c_num].append(QComboBox())
        self.dts[self.c_num].append(QDateTimeEdit())
        self.dtss[self.c_num].append(QDateTimeEdit())
        self.pbs[self.c_num].append(QPushButton('Подробнее'))
        self.cbss[self.c_num].append(QComboBox())
        self.tabs[self.c_num].setCellWidget(0, 0, self.cbs[self.c_num][rowNum])
        self.tabs[self.c_num].setCellWidget(0, 1, self.dts[self.c_num][rowNum])
        self.tabs[self.c_num].setCellWidget(0, 2, self.dtss[self.c_num][rowNum])
        self.tabs[self.c_num].setCellWidget(0, 3, self.pbs[self.c_num][rowNum])
        self.tabs[self.c_num].setCellWidget(0, 4, self.cbss[self.c_num][rowNum])


class Finance(QWidget):
    global table_row, con, cur

    def __init__(self):
        super().__init__()
        uic.loadUi('C://Users//Максим//PycharmProjects//kanbaner1//finance.ui', self)
        self.table.setRowCount(table_row)
        for i in range(table_row - 1):
            a, b, c = str(cur.execute('''SELECT * FROM finance WHERE id = ?''',
                                      str(i + 1)).fetchall())[6:-2].replace("'", '').split(', ')
            self.table.setItem(i, 0, QTableWidgetItem(a))
            self.table.setItem(i, 1, QTableWidgetItem(b))
            self.table.setItem(i, 2, QTableWidgetItem(c))

    def keyPressEvent(self, event):
        global table_row, con, cur
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == 16777220:
            try:
                bablo = [(str(table_row), self.table.item(table_row - 1, 0).text(),
                          self.table.item(table_row - 1, 1).text(), self.table.item(table_row - 1, 2).text())]
                cur.executemany("""INSERT INTO finance VALUES (?,?,?,?)""", bablo)
                con.commit()
                table_row += 1
                self.table.setRowCount(table_row)
            except:
                pass


class Kanbaner(QMainWindow):
    global user, con, cur

    def __init__(self):
        super().__init__()
        uic.loadUi('C://Users//Максим//PycharmProjects//kanbaner1//main.ui', self)
        self.label.setText(user)
        self.pb_create.clicked.connect(self.creater)
        self.pb_open.clicked.connect(self.open)
        self.pb_delete.clicked.connect(self.delete)
        self.pb_login.clicked.connect(self.exit)
        self.pb_finance.clicked.connect(self.cash)
        self.pb_graph.clicked.connect(self.graphics)
        self.title = ''
        self.rowTitlesBad = []
        self.dz = '-'
        self.rowTitles = []
        self.crew = None
        self.new = None
        self.task = None
        self.finance = None

    def creater(self):
        self.new = New()
        self.new.show()
        self.new.pb_complete.clicked.connect(self.vvod)

    def graphics(self):
        pass

    def vvod(self):
        self.rowTitlesBad.extend([self.new.le2.text(), self.new.le3.text(), self.new.le4.text(), self.new.le5.text(),
                                  self.new.le6.text(), self.new.le7.text(), self.new.le8.text(), self.new.le9.text()])
        self.title = self.new.leName.text()
        for i in self.rowTitlesBad:
            if i:
                self.rowTitles.append(i)
        if len(self.rowTitles) > 1:
            self.tw.addTopLevelItem(QTreeWidgetItem([self.title, str(datetime.datetime.strftime(datetime.datetime.now(),
                                                                                                "%Y.%m.%d %H:%M:%S")),
                                                     self.dz]))
        self.title = ''
        self.new.close()

    def open(self):
        if [x.row() for x in self.tw.selectedIndexes()]:
            self.task = Task(self.rowTitles)
            self.task.show()

    def cash(self):
        self.finance = Finance()
        self.finance.show()

    def delete(self):
        if [x.row() for x in self.tw.selectedIndexes()]:
            self.tw.takeTopLevelItem(int(str([x.row() for x in self.tw.selectedIndexes()])[1]))

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.open()
        elif event.key() == Qt.Key_Backspace:
            self.delete()
        elif event.key() == Qt.Key_Delete:
            self.delete()
        elif event.key() == Qt.Key_Q:
            self.creater()
        elif event.key() == Qt.Key_W:
            self.graphics()
        elif event.key() == Qt.Key_E:
            self.cash()

    def exit(self):
        self.close()


app = QApplication(sys.argv)
window = Enter()
window.show()
app.exec_()
