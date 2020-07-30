import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QScrollArea, QTableWidgetItem
from PyQt5 import uic
user = None
con = sqlite3.connect('personal.db')
cur = con.cursor()
table_row = int(str(cur.execute('''SELECT id FROM finance''').fetchall()[-1])[1:-2]) + 1
print(table_row)


class Enter(QWidget):
    global user, con, cur

    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.pb_login.clicked.connect(self.switch)
        memory = open('memory.txt', 'r')
        self.le_login.setText(memory.read())
        memory.close()
        self.new = None
        self.crew = None

    def switch(self):
        global user, con, cur
        user = self.le_login.text()
        self.crew = str(cur.execute('''SELECT SN FROM main''').fetchall())[3:-4].split("',), ('")
        if user in self.crew:
            memory = open('memory.txt', 'w')
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
        uic.loadUi('create.ui', self)


class Task(QWidget):
    def __init__(self, rowTitles):
        super().__init__()
        uic.loadUi('tasks.ui', self)
        self.layoutsStats = []
        self.layoutsRow = QGridLayout()
        self.layouts = []
        self.scrolls = []
        self.widgets = []
        for i in range(len(rowTitles)):
            self.scrolls.append(QScrollArea())
            self.widgets.append(QWidget())
            self.scrolls[i].setWidget(self.widgets[i])
            self.scrolls[i].resize(1121, 711)
            # self.scrolls[i].show()
            self.layouts.append(QGridLayout)
            self.layoutsStats.append(QGridLayout())
            # self.widgets[i].setLayout(self.layouts[i])
            self.tabWidget.addTab(self.scrolls[i], rowTitles[i])


class Finance(QWidget):
    global table_row, con, cur

    def __init__(self):
        super().__init__()
        uic.loadUi('finance.ui', self)
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
            bablo = [(str(table_row), self.table.item(table_row - 1, 0).text(),
                      self.table.item(table_row - 1, 1).text(), self.table.item(table_row - 1, 2).text())]
            cur.executemany("""INSERT INTO finance VALUES (?,?,?,?)""", bablo)
            con.commit()
            table_row += 1
            self.table.setRowCount(table_row)
        self.table.resizeColumnsToContents()


class Kanbaner(QMainWindow):
    global user, con, cur

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.label.setText(user)
        self.pb_create.clicked.connect(self.creater)
        self.pb_open.clicked.connect(self.open)
        self.pb_delete.clicked.connect(self.delete)
        self.pb_login.clicked.connect(self.exit)
        self.pb_finance.clicked.connect(self.cash)
        self.title = ''
        self.rowTitlesBad = []
        self.rowTitles = []
        self.crew = None
        self.new = None
        self.task = None
        self.finance = None

    def creater(self):
        self.new = New()
        self.new.show()
        self.new.pb_complete.clicked.connect(self.vvod)

    def vvod(self):
        self.rowTitlesBad.extend([self.new.le2.text(), self.new.le3.text(), self.new.le4.text(), self.new.le5.text(),
                                  self.new.le6.text(), self.new.le7.text(), self.new.le8.text(), self.new.le9.text()])
        self.title = self.new.leName.text()
        for i in self.rowTitlesBad:
            if i:
                self.rowTitles.append(i)
        if len(self.rowTitles) > 1:
            self.lw.addItem(self.title)
        self.title = ''
        self.new.close()

    def open(self):
        if [x.row() for x in self.lw.selectedIndexes()]:
            self.task = Task(self.rowTitles)
            self.task.show()

    def cash(self):
        self.finance = Finance()
        self.finance.show()

    def delete(self):
        if [x.row() for x in self.lw.selectedIndexes()]:
            self.lw.takeItem(int(str([x.row() for x in self.lw.selectedIndexes()])[1]))

    def exit(self):
        self.close()


app = QApplication(sys.argv)
window = Enter()
window.show()
app.exec_()
