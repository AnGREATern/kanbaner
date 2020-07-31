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
con = sqlite3.connect('personal.db')
cur = con.cursor()
table_row = len(cur.execute('''SELECT id FROM finance''').fetchall()) + 1


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


class More(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('more.ui', self)
        self.role = cur.execute(f'''SELECT admin FROM main WHERE SN="{user}"''').fetchall()[0][0]
        self.role = cur.execute(f'''SELECT admin FROM main WHERE SN="{user}"''').fetchall()[0][0]
        # Здесь надо выгружать текст из бд в self.teTask и в self.teChat
        if self.role in ['Editor', 'Admin']:
            self.pb_save.clicked.connect(self.save)
        else:
            self.pb_save.setParent(None)
            self.teTask.setReadOnly(True)
        self.pb_send.clicked.connect(self.send)
        self.lastText = ''  # Сюда нужно выгрузить текст из бд для задания
        self.lastChat = ''  # Сюда нужно выгрузить текст из бд для чата
        self.teTask.setText(self.lastText)
        self.teChat.setText(self.lastChat)

    def save(self):  # Здесь надо сохранять текст из self.teTask в бд
        self.saveText = str(self.teTask.toPlainText())  # Текст из задания, его нужно загрузить в бд

    def send(self):
        if str(self.teSend.toPlainText()):
            self.teChat.append(user + ': ' + str(self.teSend.toPlainText()))
        else:
            self.teSend.setPlaceholderText('Чтобы отправить сообщение, напишите что-нибудь!!!')
        self.teSend.clear()
        self.saveChat = str(self.teChat.toPlainText())


class Task(QWidget):
    def __init__(self, rowTitles):
        super().__init__()
        uic.loadUi('tasks.ui', self)
        self.pb_addT.clicked.connect(self.addTask)
        self.c_num = 0
        self.tabs = []
        # В двумерных списках помещены параметры задач, например self.cbs[Номер вкладки][Номер задачи](с нуля)
        self.cbs = [[] for _ in range(len(rowTitles))]  # combobox с исполнителями
        self.dts = [[] for _ in range(len(rowTitles))]  # Время начала
        self.dtss = [[] for _ in range(len(rowTitles))]  # Время конца
        self.pbs = [[] for _ in range(len(rowTitles))]  # Кнопка подробнее
        self.cbss = [[] for _ in range(len(rowTitles))]  # combobox со статусом

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
        self.rowNum = self.tabs[self.c_num].rowCount()
        if self.rowNum != 0:
            self.tabs[self.c_num].insertRow(0)
        else:
            self.tabs[self.c_num].setRowCount(1)
        self.cbs[self.c_num].append(QComboBox())
        self.dts[self.c_num].append(QDateTimeEdit())
        self.dtss[self.c_num].append(QDateTimeEdit())
        self.pbs[self.c_num].append(QPushButton('Подробнее'))
        self.cbss[self.c_num].append(QComboBox())
        self.tabs[self.c_num].setCellWidget(0, 0, self.cbs[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 1, self.dts[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 2, self.dtss[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 3, self.pbs[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 4, self.cbss[self.c_num][self.rowNum])

    def more(self):
        pass
        # print(str(self.i) + str(self.y))


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
        uic.loadUi('main.ui', self)
        self.label.setText(user)
        self.pb_create.clicked.connect(self.creater)
        self.pb_open.clicked.connect(self.open)
        self.pb_delete.clicked.connect(self.delete)
        self.pb_login.clicked.connect(self.exit)
        self.pb_finance.clicked.connect(self.cash)
        self.pb_graph.clicked.connect(self.graphics)
        self.title = ''
        self.rowTitlesBad = []
        self.rowTitles = []
        self.id = len(cur.execute('''SELECT id FROM kanban''').fetchall())
        for i in range(self.id, 0, -1):
            a, b, c, d = str(cur.execute('''SELECT * FROM kanban WHERE id = ?''',
                                         [str(i)]).fetchall())[6:-2].replace("'", '').split(', ')
            self.rowTitles.append(d.split())
            self.tw.addTopLevelItem(QTreeWidgetItem([a, b, c]))
        self.dz = '-'
        self.crew = None
        self.new = None
        self.task = None
        self.enter = None
        self.finance = None

    def creater(self):
        self.new = New()
        self.new.show()
        self.new.pb_complete.clicked.connect(self.vvod)

    def graphics(self):
        pass

    def vvod(self):
        self.rowTitlesBad.clear()
        self.rowTitlesBad.extend([self.new.le2.text(), self.new.le3.text(), self.new.le4.text(), self.new.le5.text(),
                                  self.new.le6.text(), self.new.le7.text(), self.new.le8.text(), self.new.le9.text()])
        self.title = self.new.leName.text()
        self.rowTitles.append([])
        for i in self.rowTitlesBad:
            if i:
                self.rowTitles[-1].append(i)
        if len(self.rowTitles[-1]) > 1:
            self.id += 1
            cur.executemany("""INSERT INTO kanban VALUES (?,?,?,?,?)""",
                            [(self.id, self.title,
                             str(datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d %H:%M:%S")),
                              self.dz, ' '.join(self.rowTitles[-1]))])
            con.commit()
            self.tw.clear()
            for i in range(self.id, 0, -1):
                a, b, c, _ = str(cur.execute('''SELECT * FROM kanban WHERE id = ?''',
                                             [str(i)]).fetchall())[6:-2].replace("'", '').split(', ')
                self.tw.addTopLevelItem(QTreeWidgetItem([a, b, c]))
        else:
            del self.rowTitles[-1]
        self.title = ''
        self.new.close()

    def open(self):
        if [x.row() for x in self.tw.selectedIndexes()]:
            self.task = Task(self.rowTitles[int(str([x.row() for x in self.tw.selectedIndexes()])[1])])
            self.task.show()

    def cash(self):
        self.finance = Finance()
        self.finance.show()

    def delete(self):
        if [x.row() for x in self.tw.selectedIndexes()]:
            pos = int(str([x.row() for x in self.tw.selectedIndexes()])[1])
            cur.execute("DELETE FROM kanban WHERE id = ?", [(str(self.id - pos))])
            con.commit()
            for i in range(self.id - pos, self.id):
                cur.execute("""UPDATE kanban SET id = ? WHERE id = ?""", [str(i), str(i + 1)])
                con.commit()
            self.id -= 1
            self.tw.takeTopLevelItem(pos)

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
        self.enter = Enter()
        self.enter.show()
        self.close()


app = QApplication(sys.argv)
window = Enter()
window.show()
app.exec_()
