import datetime
import random
import sys
import sqlite3

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QTreeWidgetItem, QTreeWidget, \
    QHeaderView, QLineEdit, QPushButton, QComboBox, QTableWidget, QDateTimeEdit, QSizePolicy
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QTreeWidgetItem, QPushButton,\
    QComboBox, QTableWidget, QDateTimeEdit
from PyQt5 import uic, QtWidgets

user = None
con = sqlite3.connect('personal.db')
cur = con.cursor()
table_row = len(cur.execute('''SELECT id FROM finance''').fetchall()) + 1
task_row = len(cur.execute('''SELECT id FROM tasks''').fetchall())


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


class Graphics(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('graphics.ui', self)
        isp1 = str(cur.execute('''SELECT SN FROM main''').fetchall())[3:-4].split("',), ('")
        ispT = [1 for i in range(len(isp1))]
        print(isp1[0], ispT)
        m = PlotCanvas(self, width=50, height=4, isp=isp1)
        m1 = PlotCanvas(self, width=50, height=4, isp=isp1)
        m2 = PlotCanvas(self, width=50, height=4, isp=isp1)
        self.tabWidget.addTab(m, 'За месяц')
        self.tabWidget.addTab(m1, 'За квартал')
        self.tabWidget.addTab(m2, 'За год')


class PlotCanvas(FigureCanvas):
    def __init__(self, ispT=0, parent=None, width=5, height=4, isp=None, dpi=50):
        if isp is None:
            isp = []
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.isp = isp
        self.ispT = ispT
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.bar()

    def bar(self):
        data = [random.random() for i in range(len(self.isp))]
        ax = self.figure.add_subplot(111)
        ax.bar(self.isp, data)
        ax.set_title('График с нагрузкой персонала')
        self.draw()


class More(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('more.ui', self)
        self.role = cur.execute(f'''SELECT admin FROM main WHERE SN="{user}"''').fetchall()[0][0]
        self.saveText = None
        self.saveChat = None
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
    global con, cur, task_row

    def __init__(self, rowTitles, name):
        super().__init__()
        uic.loadUi('tasks.ui', self)
        self.setMouseTracking(True)
        self.pb_addT.clicked.connect(self.addTask)
        self.pb_reboot.clicked.connect(self.reboot)
        self.name = name
        self.mor = None
        self.c_num = 0
        self.tabs = []
        self.rowNum = None
        self.pb_more = None
        self.ispolniteli = []  # Переменная хранящая всех сотрудников
        self.status = ['', 'Удалить']
        self.status.extend(rowTitles)
        # В двумерных списках помещены параметры задач, например self.cbs[Номер вкладки][Номер задачи](с нуля)
        self.cbs = [[] for _ in range(len(rowTitles))]  # combobox с исполнителями
        for i in range(len(cur.execute('''SELECT id FROM main''').fetchall())):
            self.ispolniteli.append(cur.execute('''SELECT SN FROM main''').fetchall()[i][0])
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
        for i in range(task_row):
            _, _, self.sn, self.startdate, self.enddate, _, _ =\
                cur.execute('''SELECT * FROM tasks WHERE id = ?''', str(i)).fetchall()[0]
            self.addTask()

    def addTask(self):
        self.c_num = self.tabWidget.currentIndex()
        self.rowNum = self.tabs[self.c_num].rowCount()
        if self.rowNum != 0:
            self.tabs[self.c_num].insertRow(0)
        else:
            self.tabs[self.c_num].setRowCount(1)
        self.cbs[self.c_num].append(QComboBox())
        self.cbs[self.c_num][-1].addItems(self.ispolniteli)
        try:
            self.cbs[self.c_num][-1].setCurrentIndex(self.ispolniteli.index(self.sn))
            self.sn = None
        except:
            pass
        self.dts[self.c_num].append(QDateTimeEdit())
        self.dtss[self.c_num].append(QDateTimeEdit())
        self.pb_more = QPushButton('Подробнее')
        self.pbs[self.c_num].append(self.pb_more)
        self.cbss[self.c_num].append(QComboBox())
        self.cbss[self.c_num][-1].addItems(self.status)
        self.tabs[self.c_num].setCellWidget(0, 0, self.cbs[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 1, self.dts[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 2, self.dtss[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 3, self.pbs[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 4, self.cbss[self.c_num][self.rowNum])
        self.pb_more.clicked.connect(self.more)

    def more(self):
        self.mor = More()
        self.mor.show()

    def reboot(self):
        for j in range(len(self.tabs)):
            try:
                for i in range(self.rowNum, -1, -1):
                    bablo = [(str(i), self.name + ' ' + str(j), self.cbs[j][i].currentText(),
                              self.dts[j][i].date().toString(), self.dtss[j][i].date().toString(), '', '')]
                    cur.executemany("""INSERT INTO tasks VALUES (?,?,?,?,?,?,?)""", bablo)
                    con.commit()
            except:
                pass


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
        self.gr = Graphics()
        self.gr.show()

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
            self.task = Task(self.rowTitles[int(str([x.row() for x in self.tw.selectedIndexes()])[1])],
                             cur.execute('''SELECT title FROM kanban WHERE id = ?''',
                                         [(str(self.id))]).fetchall()[0][0])
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
