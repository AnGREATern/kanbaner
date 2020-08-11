import datetime
import sys
import sqlite3
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt, QDate, QTimer, QSize, QTime
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QTreeWidgetItem, QPushButton, \
    QComboBox, QTableWidget, QSizePolicy, QDateEdit, QLabel, QDesktopWidget, QCheckBox
from PyQt5 import uic, QtWidgets
from dateutil.relativedelta import relativedelta

user = None
con = sqlite3.connect('personal.db')
cur = con.cursor()
task_index = 0
table_row = len(cur.execute('''SELECT id FROM finance''').fetchall()) + 1
task_row = len(cur.execute('''SELECT id FROM tasks''').fetchall())
pushs = []


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
            self.yyyy()

    def yyyy(self):
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
        isp1, isp2, isp3 = {}, {}, {}
        self.rowTitlesR, self.titles, self.rowNum, self.kanbanid, self.ispolns, self.datesK = [], [], [], [], [], []

        for i in cur.execute('''SELECT * FROM tasks''').fetchall():
            self.rowNum.append(i[2])
            self.kanbanid.append(i[1])
            self.ispolns.append(i[4])
            self.datesK.append(i[6])
        for j in self.kanbanid:
            a = cur.execute(f'''SELECT * FROM kanban WHERE id={str(j)}''').fetchall()
            for i in range(len(a)):
                self.titles.append(a[i][1])
                self.rowTitlesR.append(a[i][4].split())

        for i in range(len(self.ispolns)):
            col = 0
            if self.rowNum[i] == len(self.rowTitlesR[i]) - 1:
                if datetime.datetime(int(pushs[3][i].split('.')[0]), int(pushs[3][i].split('.')[1]),
                                     int(pushs[3][i].split('.')[2])) + relativedelta(
                    months=+12) >= datetime.datetime.now():
                    col = 3
                if datetime.datetime(int(pushs[3][i].split('.')[0]), int(pushs[3][i].split('.')[1]),
                                     int(pushs[3][i].split('.')[2])) + relativedelta(
                    months=+3) >= datetime.datetime.now():
                    col = 2
                if datetime.datetime(int(pushs[3][i].split('.')[0]), int(pushs[3][i].split('.')[1]),
                                     int(pushs[3][i].split('.')[2])) + relativedelta(
                    months=+1) >= datetime.datetime.now():
                    col = 1
                if col == 1:
                    if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in isp1.keys():
                        isp1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = 1
                    else:
                        isp1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += 1
                    if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in isp2.keys():
                        isp2[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = 1
                    else:
                        isp2[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += 1
                    if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in isp3.keys():
                        isp3[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = 1
                    else:
                        isp3[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += 1
                if col == 2:
                    if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in isp1.keys():
                        isp1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = 1
                    else:
                        isp1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += 1
                    if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in isp2.keys():
                        isp2[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = 1
                    else:
                        isp2[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += 1
                if col == 3:
                    if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in isp1.keys():
                        isp1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = 1
                    else:
                        isp1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += 1
        ispF1, ispF2, ispF3 = {}, {}, {}
        self.dengi, self.ispolns, self.datesK = [], [], []

        for i in cur.execute('''SELECT * FROM finance''').fetchall():
            self.ispolns.append(i[1])
            self.datesK.append(i[3])
            self.dengi.append(i[4])
        for i in range(len(self.ispolns)):
            col = 0
            if datetime.datetime(int(self.datesK[i].split('.')[0]), int(self.datesK[i].split('.')[1]),
                                 int(self.datesK[i].split('.')[2])) + relativedelta(months=+12) >= datetime.datetime.now():
                col = 3
            if datetime.datetime(int(self.datesK[i].split('.')[0]), int(self.datesK[i].split('.')[1]),
                                 int(self.datesK[i].split('.')[2])) + relativedelta(months=+3) >= datetime.datetime.now():
                col = 2
            if datetime.datetime(int(self.datesK[i].split('.')[0]), int(self.datesK[i].split('.')[1]),
                                 int(self.datesK[i].split('.')[2])) + relativedelta(months=+1) >= datetime.datetime.now():
                col = 1
            if col == 1:
                if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in ispF1.keys():
                    ispF1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = self.dengi[i]
                else:
                    ispF1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += self.dengi[i]
                if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in ispF2.keys():
                    ispF2[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = self.dengi[i]
                else:
                    ispF2[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += self.dengi[i]
                if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in ispF3.keys():
                    ispF3[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = self.dengi[i]
                else:
                    ispF3[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += self.dengi[i]
            if col == 2:
                if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in ispF1.keys():
                    ispF1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = self.dengi[i]
                else:
                    ispF1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += self.dengi[i]
                if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in ispF2.keys():
                    ispF2[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = self.dengi[i]
                else:
                    ispF2[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += self.dengi[i]
            if col == 3:
                if not self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.' in ispF1.keys():
                    ispF1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] = self.dengi[i]
                else:
                    ispF1[self.ispolns[i].split()[0] + ' ' + self.ispolns[i].split()[1][0] + '.'] += self.dengi[i]
        m = PlotCanvas(self, width=50, height=4, isp=isp3, ispF=ispF3)
        m1 = PlotCanvas(self, width=50, height=4, isp=isp2, ispF=ispF2)
        m2 = PlotCanvas(self, width=50, height=4, isp=isp1, ispF=ispF1)
        self.tabWidget.addTab(m, 'За месяц')
        self.tabWidget.addTab(m1, 'За квартал')
        self.tabWidget.addTab(m2, 'За год')


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, isp=None, ispF=None, dpi=80):
        if isp is None:
            isp = []
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(212)
        self.axes1 = fig.add_subplot(211)
        self.isp = isp
        self.ispF = ispF
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.bar()

    def bar(self):
        ax = self.figure.add_subplot(212)
        ax1 = self.figure.add_subplot(211)

        ax.bar(self.isp.keys(), [self.isp.get(i) for i in self.isp.keys()])
        ax.set_title('График с нагрузкой персонала')
        ax1.bar(self.ispF.keys(), [self.ispF.get(i) for i in self.ispF.keys()])
        ax1.set_title('График финансов')

        self.draw()


class More(QWidget):
    global cur, con

    def __init__(self, a):
        super().__init__()
        uic.loadUi('more.ui', self)
        self.role = cur.execute(f'''SELECT adm FROM main WHERE SN="{user}"''').fetchall()[0][0]
        if user in a[4]:
            del a[4][a[4].index(user)]
        cur.execute(f"""UPDATE tasks SET comment = '{'-'.join(a[4])}' WHERE bind = {str(a[0])}
AND row = {str(a[1])} AND positioning = {str(a[2])}""")
        con.commit()
        self.saveText = None
        self.saveChat = None
        self.a = a
        _, _, _, _, _, _, _, _, _, task, chat, _ = cur.execute(f'''SELECT * FROM tasks WHERE bind = {str(a[0])}
AND row = {str(a[1])} AND positioning = {str(a[2])}''').fetchall()[0]
        if self.role in ['Editor', 'Admin']:
            self.pb_save.clicked.connect(self.save)
        else:
            self.pb_save.setParent(None)
            self.teTask.setReadOnly(True)
        self.pb_send.clicked.connect(self.send)
        self.lastText = task  # Сюда нужно выгрузить текст из бд для задания
        self.lastChat = chat  # Сюда нужно выгрузить текст из бд для чата
        self.teTask.setText(self.lastText)
        self.teChat.setText(self.lastChat)

    def save(self):  # Здесь надо сохранять текст из self.teTask в бд
        self.saveText = str(self.teTask.toPlainText())  # Текст из задания, его нужно загрузить в бд
        cur.execute(f"""UPDATE tasks SET task = '{self.saveText}' WHERE bind = {str(self.a[0])}
AND row = {str(self.a[1])} AND positioning = {str(self.a[2])}""")
        con.commit()

    def send(self):
        if str(self.teSend.toPlainText()):
            com = [self.a[3], cur.execute(f'''SELECT SN FROM main WHERE adm = "Admin"''').fetchall()[0][0],
                   cur.execute(f'''SELECT SN FROM main WHERE adm = "Editor"''').fetchall()[0][0]]
            com = list(set(com))
            del com[com.index(user)]
            self.teChat.append(user + ': ' + str(self.teSend.toPlainText()).rstrip())
            cur.execute(f"""UPDATE tasks SET comment = '{'-'.join(com)}'
WHERE bind = {str(self.a[0])} AND row = {str(self.a[1])} AND positioning = {str(self.a[2])}""")
        else:
            self.teSend.setPlaceholderText('Чтобы отправить сообщение, напишите что-нибудь!!!')
        self.teSend.clear()
        self.saveChat = str(self.teChat.toPlainText())
        cur.execute(
            f"""UPDATE tasks SET chat = '{self.saveChat}' WHERE bind = {str(self.a[0])} AND row = {str(self.a[1])}
AND positioning = {str(self.a[2])}""")
        con.commit()

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.send()


class Task_6(QWidget):
    global con, cur, task_row, task_index

    def __init__(self, rowTitles, name, id):
        super().__init__()
        uic.loadUi('tasks.ui', self)
        self.setWindowTitle(name)
        self.setMouseTracking(True)
        self.role = cur.execute(f'''SELECT adm FROM main WHERE SN="{user}"''').fetchall()[0][0]
        if self.role == 'Admin':
            self.pb_addT.clicked.connect(self.addTask)
        else:
            self.pb_addT.setParent(None)
        self.pb_reboot.clicked.connect(self.reboot)
        self.name = name
        self.poz = [-1 for _ in range(len(rowTitles))]
        self.id = id
        self.mor = None
        self.c_num = 0
        self.tabs = []
        self.rowNum = None
        self.pb_more = None
        self.ispolniteli = []  # Переменная хранящая всех сотрудников
        self.statusbezadmina = rowTitles.copy()
        self.rT = rowTitles[:]
        if self.role == 'Admin':
            self.rT.extend(['%Удалить%', '%Обновить%'])
        else:
            self.rT.extend(['%Обновить%'])
        self.status = self.rT
        # В двумерных списках помещены параметры задач, например self.cbs[Номер вкладки][Номер задачи](с нуля)
        self.cbs = [[] for _ in range(len(rowTitles))]  # combobox с исполнителями
        for i in range(len(cur.execute('''SELECT id FROM main''').fetchall())):
            self.ispolniteli.append(cur.execute('''SELECT SN FROM main''').fetchall()[i][0])
        self.dts = [[] for _ in range(len(rowTitles))]  # Время начала
        self.dtss = [[] for _ in range(len(rowTitles))]  # Время конца
        self.pbs = [[] for _ in range(len(rowTitles))]  # Кнопка подробнее
        self.cbss = [[] for _ in range(len(rowTitles))]  # combobox со статусом
        self.chx = [[] for _ in range(len(rowTitles))]
        self.dlina_kalumny = [-1 for _ in range(len(rowTitles))]
        for i in range(len(rowTitles)):
            self.tabs.append(QTableWidget(self))
            self.tabs[i].setFont(QFont('Segoe UI', 12))
            self.tabs[i].setColumnCount(6)
            header = self.tabs[i].horizontalHeader()
            for y in range(6):
                header.setSectionResizeMode(y, QtWidgets.QHeaderView.Stretch)
            self.tabs[i].setHorizontalHeaderLabels(['Исполнитель', 'Время выдачи', 'Срок сдачи',
                                                    'Задача/чат', 'Уведомления', 'Статус'])
            self.tabWidget.addTab(self.tabs[i], rowTitles[i])
        for i in range(task_row):
            _, bind, row, self.position, self.sn, self.startdate, self.enddate, check_admin, check_editor, _, _, com = \
                cur.execute('''SELECT * FROM tasks WHERE id = ?''', [(str(i))]).fetchall()[0]
            if bind == self.id:
                if len(self.startdate) != 10:
                    if self.startdate[6] == '.':
                        self.startdate = self.startdate[:5] + '0' + self.startdate[5:]
                    if len(self.startdate) != 10:
                        self.startdate = self.startdate[:-1] + '0' + self.startdate[-1]
                if len(self.enddate) != 10:
                    if self.enddate[6] == '.':
                        self.enddate = self.enddate[:5] + '0' + self.enddate[5:]
                    if len(self.enddate) != 10:
                        self.enddate = self.enddate[:-1] + '0' + self.enddate[-1]
                self.startdate1 = QDate.fromString(self.startdate, "yyyy.MM.dd")
                self.enddate1 = QDate.fromString(self.enddate, "yyyy.MM.dd")
                self.c_num = row
                self.rowNum = self.tabs[self.c_num].rowCount()
                if self.rowNum != 0:
                    self.tabs[self.c_num].insertRow(0)
                else:
                    self.tabs[self.c_num].setRowCount(1)
                self.cbs[self.c_num].append(QComboBox())
                self.cbs[self.c_num][-1].addItems(self.ispolniteli)
                self.cbs[self.c_num][-1].setCurrentIndex(self.ispolniteli.index(self.sn))
                self.cbs[self.c_num][-1].setStyleSheet('font: 75 12pt')
                self.dts[self.c_num].append(QDateEdit())
                self.dts[self.c_num][self.rowNum].setStyleSheet(
                    'font: 75 12pt "MS Shell Dlg 2";')
                self.dtss[self.c_num].append(QDateEdit())
                self.dtss[self.c_num][self.rowNum].setStyleSheet(
                    'font: 75 12pt "MS Shell Dlg 2";')
                self.dts[self.c_num][self.rowNum].setDate(self.startdate1)
                self.dtss[self.c_num][self.rowNum].setDate(self.enddate1)
                if self.dtss[self.c_num][self.rowNum].date() < datetime.datetime.now():
                    self.dtss[self.c_num][self.rowNum].setStyleSheet('background-color: red;'
                                                                     ' font: 75 12pt "MS Shell Dlg 2";')
                self.chx[self.c_num].append(QCheckBox())
                if (self.role == 'Admin' and check_admin == 'True')\
                        or (self.role == 'Editor' and check_editor == 'True'):
                    self.chx[self.c_num][-1].setChecked(True)
                self.pb_more = QPushButton('Подробнее')
                self.pbs[self.c_num].append(self.pb_more)
                self.pbs[self.c_num][-1].setStyleSheet('font: 75 12pt')
                com = com.split('-')
                if user in com:
                    self.pbs[self.c_num][-1].setStyleSheet('QPushButton {background-color: rgb(116, 208, 196);'
                                                           ' font: 75 12pt}')
                self.pbs[self.c_num][-1].clicked.connect(lambda checked,
                                                         a=[bind, row, self.position, self.sn, com]:
                                                         self.more(a))
                self.cbss[self.c_num].append(QComboBox())
                self.cbss[self.c_num][-1].setStyleSheet('font: 75 12pt')
                self.cbss[self.c_num][-1].addItems(self.status)
                self.cbss[self.c_num][-1].setCurrentIndex(self.c_num)
                self.tabs[self.c_num].setCellWidget(0, 0, self.cbs[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 1, self.dts[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 2, self.dtss[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 3, self.pbs[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 5, self.cbss[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 4, self.chx[self.c_num][self.rowNum])
                self.dlina_kalumny[self.c_num] += 1
        self.tabWidget.setCurrentIndex(task_index)

    def more(self, a):
        self.pbs[a[1]][a[2]].setStyleSheet('font: 75 12pt')
        self.mor = More(a)
        self.mor.show()

    def addTask(self):
        self.c_num = self.tabWidget.currentIndex()
        self.rowNum = self.tabs[self.c_num].rowCount()
        self.poz[self.c_num] += 1
        if self.rowNum != 0:
            self.tabs[self.c_num].insertRow(0)
        else:
            self.tabs[self.c_num].setRowCount(1)
        self.cbs[self.c_num].append(QComboBox())
        self.cbs[self.c_num][-1].addItems(self.ispolniteli)
        self.cbs[self.c_num][-1].setStyleSheet('font: 75 12pt')
        self.dts[self.c_num].append(QDateEdit(datetime.datetime.now()))
        self.dtss[self.c_num].append(QDateEdit(datetime.datetime.now()))
        self.pb_more = QPushButton('Подробнее')
        self.pbs[self.c_num].append(self.pb_more)
        self.cbss[self.c_num].append(QComboBox())
        self.cbss[self.c_num][-1].addItems(self.status)
        self.cbss[self.c_num][-1].setStyleSheet('font: 75 12pt')
        self.cbss[self.c_num][-1].setCurrentIndex(self.c_num)
        self.chx[self.c_num].append(QCheckBox())
        self.tabs[self.c_num].setCellWidget(0, 0, self.cbs[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 1, self.dts[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 2, self.dtss[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 3, self.pbs[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 5, self.cbss[self.c_num][self.rowNum])
        self.tabs[self.c_num].setCellWidget(0, 4, self.chx[self.c_num][self.rowNum])

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.addTask()
        elif event.key() == Qt.Key_F5:
            self.reboot()

    def reboot(self):
        global con, cur, task_row, task_index
        for j in range(len(self.tabs)):
            try:
                for i in range(self.tabs[self.tabWidget.currentIndex()].rowCount() - 1, self.dlina_kalumny[j], -1):
                    a = str(self.dts[j][i].date().year()) + '.' + str(self.dts[j][i].date().month()) + '.' + \
                        str(self.dts[j][i].date().day())
                    b = str(self.dtss[j][i].date().year()) + '.' + str(self.dtss[j][i].date().month()) + '.' + \
                        str(self.dtss[j][i].date().day())
                    if self.role == 'Admin':
                        c = str(self.chx[j][i].isChecked())
                        d = "False"
                    else:
                        d = str(self.chx[j][i].isChecked())
                        c = "False"
                    bablo = [(task_row, str(self.id), str(j),
                              self.tabs[self.tabWidget.currentIndex()].rowCount() - 1 - self.poz[j],
                              self.cbs[j][i].currentText(), a, b, c, d, '', '', '')]
                    cur.executemany("""INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", bablo)
                    con.commit()
                    self.dlina_kalumny[j] += 1
                    self.poz[j] -= 1
                    task_row += 1
            except:
                pass
        try:
            i = self.tabWidget.currentIndex()
            for j in range(self.tabs[i].rowCount() - 1, -1, -1):
                if [self.dtss[i][j].date().day(), self.dtss[i][j].date().month(), self.dtss[i][j].date().year()] ==\
                        [datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year]:
                    self.dtss[i][j].setStyleSheet('background-color: red')
                if self.cbss[i][j].currentText() == '%Удалить%':
                    kapcha = 0
                    y, bind, row, positioning, _, _, _, _, _, _, _, _ = \
                        cur.execute('''SELECT * FROM tasks WHERE row = ? AND positioning = ? AND bind = ?''',
                                    (str(i), str(j), str(self.id))).fetchall()[0]
                    cur.execute("DELETE FROM tasks WHERE id = ?", [(str(y))])
                    con.commit()
                    for h in range(y, task_row):
                        cur.execute("""UPDATE tasks SET positioning = ? WHERE row = ? AND bind = ? AND id = ?""",
                                    (str(positioning + kapcha), str(row), str(bind), str(h + 1)))
                        cur.execute("""UPDATE tasks SET id = ? WHERE id = ?""",
                                    [str(h), str(h + 1)])
                        kapcha += 1
                    con.commit()
                    self.tabs[i].removeRow(self.dlina_kalumny[i] - j)
                    task_row -= 1
                    self.dlina_kalumny[i] -= 1
                elif self.cbss[i][j].currentText() == '%Обновить%':
                    a = str(self.dts[i][j].date().year()) + '.' + str(self.dts[i][j].date().month()) + '.' + \
                        str(self.dts[i][j].date().day())
                    b = str(self.dtss[i][j].date().year()) + '.' + str(self.dtss[i][j].date().month()) + '.' + \
                        str(self.dtss[i][j].date().day())
                    cur.execute("""UPDATE tasks SET startdate = ? WHERE row = ? AND positioning = ? AND bind = ?""",
                                [a, str(i), str(j), str(self.id)])
                    cur.execute("""UPDATE tasks SET enddate = ? WHERE row = ? AND positioning = ? AND bind = ?""",
                                [b, str(i), str(j), str(self.id)])
                    cur.execute("""UPDATE tasks SET ispoln = ? WHERE row = ? AND positioning = ? AND bind = ?""",
                                [self.cbs[i][j].currentText(), str(i), str(j), str(self.id)])
                    if self.role == 'Admin':
                        cur.execute("""UPDATE tasks SET check_admin = ? WHERE row = ? AND positioning = ?
                         AND bind = ?""", [str(self.chx[i][j].isChecked()), str(i), str(j), str(self.id)])
                    else:
                        cur.execute("""UPDATE tasks SET check_editor = ? WHERE row = ? AND positioning = ?
                         AND bind = ?""", [str(self.chx[i][j].isChecked()), str(i), str(j), str(self.id)])
                    con.commit()
                elif not self.cbss[i][j].currentText() == self.tabWidget.tabText(i):
                    tab = self.statusbezadmina.index(self.cbss[i][j].currentText())
                    kapcha = 0
                    y, bind, row, positioning, c, a, b, d, e, f, g, z = \
                        cur.execute('''SELECT * FROM tasks WHERE row = ? AND positioning = ? AND bind = ?''',
                                    (str(i), str(j), str(self.id))).fetchall()[0]
                    cur.execute("DELETE FROM tasks WHERE id = ?", [(str(y))])
                    con.commit()
                    for h in range(y, task_row):
                        cur.execute("""UPDATE tasks SET positioning = ? WHERE row = ? AND bind = ? AND id = ?""",
                                    (str(positioning + kapcha), str(row), str(bind), str(h + 1)))
                        cur.execute("""UPDATE tasks SET id = ? WHERE id = ?""",
                                    [str(h), str(h + 1)])
                        kapcha += 1
                    con.commit()
                    self.tabs[i].removeRow(self.dlina_kalumny[i] - j)
                    task_row -= 1
                    self.dlina_kalumny[i] -= 1

                    bablo = [(str(task_row), str(bind), str(tab), str(self.tabs[tab].rowCount() - 1 - self.poz[tab]), c,
                              a, b, d, e, f, g, z)]
                    cur.executemany("""INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", bablo)
                    con.commit()
                    self.dlina_kalumny[tab] += 1
                    self.poz[tab] -= 1
                    task_row += 1
        except:
            print('sasatb')
        for i in range(len(self.tabs)):
            if i == (len(self.tabs) - 1):
                cur.execute("""UPDATE kanban SET stage = ? WHERE id = ?""",
                            [self.tabWidget.tabText(len(self.tabs) - 1), str(self.id)])
                cur.execute("""UPDATE kanban SET end_date = ? WHERE id = ?""",
                            [str(datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d %H:%M:%S")),
                             str(self.id)])
                con.commit()
                break
            elif self.dlina_kalumny[i] > -1:
                cur.execute("""UPDATE kanban SET stage = ? WHERE id = ?""",
                            [self.tabWidget.tabText(i), str(self.id)])
                cur.execute("""UPDATE kanban SET end_date = ? WHERE id = ?""", [str('-'), str(self.id)])
                con.commit()
                break
        task_index = self.tabWidget.currentIndex()
        self.close()
        window.new.reboot(self.id)


class Task(QWidget):
    global con, cur, task_row, task_index

    def __init__(self, rowTitles, name, id):
        super().__init__()
        uic.loadUi('tasks.ui', self)
        self.setMouseTracking(True)
        self.setWindowTitle(name)
        self.role = cur.execute(f'''SELECT adm FROM main WHERE SN="{user}"''').fetchall()[0][0]
        self.pb_addT.setParent(None)
        self.pb_reboot.clicked.connect(self.reboot)
        self.name = name
        self.poz = [-1 for _ in range(len(rowTitles))]
        self.id = id
        self.mor = None
        self.c_num = 0
        self.tabs = []
        self.rowNum = None
        self.pb_more = None
        self.ispolniteli = []  # Переменная хранящая всех сотрудников
        self.statusbezadmina = rowTitles.copy()
        self.rT = rowTitles[:]
        self.status = self.rT
        # В двумерных списках помещены параметры задач, например self.cbs[Номер вкладки][Номер задачи](с нуля)
        self.cbs = [[] for _ in range(len(rowTitles))]  # combobox с исполнителями
        for i in range(len(cur.execute('''SELECT id FROM main''').fetchall())):
            self.ispolniteli.append(cur.execute('''SELECT SN FROM main''').fetchall()[i][0])
        self.dts = [[] for _ in range(len(rowTitles))]  # Время начала
        self.dtss = [[] for _ in range(len(rowTitles))]  # Время конца
        self.pbs = [[] for _ in range(len(rowTitles))]  # Кнопка подробнее
        self.cbss = [[] for _ in range(len(rowTitles))]  # combobox со статусом
        self.dlina_kalumny = [-1 for _ in range(len(rowTitles))]
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
            _, bind, row, self.position, self.sn, self.startdate, self.enddate, _, _, _, _, com = \
                cur.execute('''SELECT * FROM tasks WHERE id = ?''', [(str(i))]).fetchall()[0]
            if bind == self.id and self.sn == user:
                if len(self.startdate) != 10:
                    if self.startdate[6] == '.':
                        self.startdate = self.startdate[:5] + '0' + self.startdate[5:]
                    if len(self.startdate) != 10:
                        self.startdate = self.startdate[:-1] + '0' + self.startdate[-1]
                if len(self.enddate) != 10:
                    if self.enddate[6] == '.':
                        self.enddate = self.enddate[:5] + '0' + self.enddate[5:]
                    if len(self.enddate) != 10:
                        self.enddate = self.enddate[:-1] + '0' + self.enddate[-1]
                self.startdate1 = QDate.fromString(self.startdate, "yyyy.MM.dd")
                self.enddate1 = QDate.fromString(self.enddate, "yyyy.MM.dd")
                self.c_num = row
                self.rowNum = self.tabs[self.c_num].rowCount()
                if self.rowNum != 0:
                    self.tabs[self.c_num].insertRow(0)
                else:
                    self.tabs[self.c_num].setRowCount(1)
                self.cbs[self.c_num].append(QLabel(self.sn))
                self.cbs[self.c_num][-1].setStyleSheet('font: 75 12pt')
                self.dts[self.c_num].append(QDateEdit())
                self.dts[self.c_num][self.rowNum].setStyleSheet(
                    'font: 75 12pt "MS Shell Dlg 2";')
                self.dtss[self.c_num].append(QDateEdit())
                self.dtss[self.c_num][self.rowNum].setStyleSheet(
                    'font: 75 12pt "MS Shell Dlg 2";')
                self.dts[self.c_num][self.rowNum].setDate(self.startdate1)
                self.dtss[self.c_num][self.rowNum].setDate(self.enddate1)
                if self.dtss[self.c_num][self.rowNum].date() < datetime.datetime.now():
                    self.dtss[self.c_num][self.rowNum].setStyleSheet('background-color: red;'
                                                                     ' font: 75 12pt "MS Shell Dlg 2";')
                self.dts[self.c_num][self.rowNum].setReadOnly(True)
                self.dtss[self.c_num][self.rowNum].setReadOnly(True)
                self.pb_more = QPushButton('Подробнее')
                self.pbs[self.c_num].append(self.pb_more)
                self.pbs[self.c_num][-1].setStyleSheet('font: 75 12pt')
                com = com.split('-')
                if user in com:
                    self.pbs[self.c_num][-1].setStyleSheet('QPushButton {background-color: rgb(116, 208, 196);'
                                                           ' font: 75 12pt}')
                self.pbs[self.c_num][-1].clicked.connect(lambda checked,
                                                         a=[bind, row, self.position, self.sn, com]:
                                                         self.more(a))
                self.cbss[self.c_num].append(QComboBox())
                self.cbss[self.c_num][-1].setStyleSheet('font: 75 12pt')
                self.cbss[self.c_num][-1].addItems(self.status)
                self.cbss[self.c_num][-1].setCurrentIndex(self.c_num)
                self.tabs[self.c_num].setCellWidget(0, 0, self.cbs[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 1, self.dts[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 2, self.dtss[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 3, self.pbs[self.c_num][self.rowNum])
                self.tabs[self.c_num].setCellWidget(0, 4, self.cbss[self.c_num][self.rowNum])
                self.dlina_kalumny[self.c_num] += 1
        self.tabWidget.setCurrentIndex(task_index)

    def more(self, a):
        self.pbs[a[1]][a[2]].setStyleSheet('font: 75 12pt')
        self.mor = More(a)
        self.mor.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.reboot()

    def reboot(self):
        global con, cur, task_row, task_index
        try:
            i = self.tabWidget.currentIndex()
            for j in range(self.tabs[i].rowCount() - 1, -1, -1):
                if [self.dtss[i][j].date().day(), self.dtss[i][j].date().month(), self.dtss[i][j].date().year()] ==\
                        [datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year]:
                    self.dtss[i][j].setStyleSheet('background-color: red')
                if not self.cbss[i][j].currentText() == self.tabWidget.tabText(i):
                    tab = self.statusbezadmina.index(self.cbss[i][j].currentText())
                    kapcha = 0
                    y, bind, row, positioning, c, a, b, d, e, f, g, z = \
                        cur.execute('''SELECT * FROM tasks WHERE row = ? AND positioning = ? AND bind = ?''',
                                    (str(i), str(j), str(self.id))).fetchall()[0]
                    cur.execute("DELETE FROM tasks WHERE id = ?", [(str(y))])
                    con.commit()
                    for h in range(y, task_row):
                        cur.execute("""UPDATE tasks SET positioning = ? WHERE row = ? AND bind = ? AND id = ?""",
                                    (str(positioning + kapcha), str(row), str(bind), str(h + 1)))
                        cur.execute("""UPDATE tasks SET id = ? WHERE id = ?""",
                                    [str(h), str(h + 1)])
                        kapcha += 1
                    con.commit()
                    self.tabs[i].removeRow(self.dlina_kalumny[i] - j)
                    task_row -= 1
                    self.dlina_kalumny[i] -= 1

                    bablo = [(str(task_row), str(bind), str(tab), str(self.tabs[tab].rowCount() - 1 - self.poz[tab]), c,
                              a, b, d, e, f, g, z)]
                    cur.executemany("""INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?)""", bablo)
                    con.commit()
                    self.dlina_kalumny[tab] += 1
                    self.poz[tab] -= 1
                    task_row += 1
        except:
            print('sasatb')
        for i in range(len(self.tabs)):
            if self.dlina_kalumny[i] > -1:
                cur.execute("""UPDATE kanban SET stage = ? WHERE id = ?""",
                            [self.tabWidget.tabText(i), str(self.id)])
                con.commit()
                break
            elif i == len(self.tabs) - 1:
                cur.execute("""UPDATE kanban SET stage = ? WHERE id = ?""",
                            [self.tabWidget.tabText(len(self.tabs) - 1), str(self.id)])
                cur.execute("""UPDATE kanban SET end_date = ? WHERE id = ?""",
                            [str(datetime.datetime.strftime(datetime.datetime.now(),
                                                            "%Y.%m.%d %H:%M:%S")), str(self.id)])
                con.commit()
                break
        task_index = self.tabWidget.currentIndex()
        self.close()
        window.new.reboot(self.id)


class Finance(QWidget):
    global table_row, con, cur

    def __init__(self):
        super().__init__()
        uic.loadUi('finance.ui', self)
        for y in range(4):
            self.table.horizontalHeader().setSectionResizeMode(y, QtWidgets.QHeaderView.Stretch)
        self.table.setRowCount(table_row)
        self.ispolniteli = []
        for i in range(len(cur.execute('''SELECT id FROM main''').fetchall())):
            self.ispolniteli.append(cur.execute('''SELECT SN FROM main''').fetchall()[i][0])
        self.cbss = []
        self.dtss = []
        for i in range(table_row - 1):
            self.dtss.append(QDateEdit())
            self.cbss.append(QComboBox())
            self.cbss[-1].addItems(self.ispolniteli)
            _, b, c, d, e = cur.execute('''SELECT * FROM finance WHERE id = ?''', [str(i + 1)]).fetchall()[0]
            if len(d) != 10:
                if d[6] == '.':
                    d = d[:5] + '0' + d[5:]
                if len(d) != 10:
                    d = d[:-1] + '0' + d[-1]
            d = QDate.fromString(d, "yyyy.MM.dd")
            self.dtss[i].setDate(d)
            self.cbss[-1].setCurrentIndex(self.ispolniteli.index(b))
            self.table.setCellWidget(i, 0, self.cbss[i])
            self.table.setItem(i, 1, QTableWidgetItem(c))
            self.table.setCellWidget(i, 2, self.dtss[i])
            self.table.setItem(i, 3, QTableWidgetItem(str(e)))
        self.dtss.append(QDateEdit(datetime.datetime.now()))
        self.cbss.append(QComboBox())
        self.cbss[-1].addItems(self.ispolniteli)
        self.table.setCellWidget(table_row - 1, 2, self.dtss[-1])
        self.table.setCellWidget(table_row - 1, 0, self.cbss[-1])

    def keyPressEvent(self, event):
        global table_row, con, cur
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == 16777220:
            try:
                b = str(self.dtss[-1].date().year()) + '.' + str(self.dtss[-1].date().month()) + '.' + \
                    str(self.dtss[-1].date().day())
                bablo = [(str(table_row), self.cbss[-1].currentText(),
                          self.table.item(table_row - 1, 1).text(), b, self.table.item(table_row - 1, 3).text())]
                cur.executemany("""INSERT INTO finance VALUES (?,?,?,?,?)""", bablo)
                con.commit()
                table_row += 1
                self.table.setRowCount(table_row)
                self.dtss.append(QDateEdit(datetime.datetime.now()))
                self.table.setCellWidget(table_row, 2, self.dtss[-1])
                self.cbss.append(QComboBox())
                self.cbss[-1].addItems(self.ispolniteli)
                self.table.setCellWidget(table_row, 2, self.dtss[-1])
            except:
                pass


class Push(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('push.ui', self)
        q = QDesktopWidget().availableGeometry()
        self.move(q.width() - 680, q.height() - 260)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.f = True
        self.pb_10.pressed.connect(self.sleep10p)
        self.pb_30.pressed.connect(self.sleep30p)
        self.pb_120.pressed.connect(self.sleep120p)
        self.pb_10.clicked.connect(self.sleep10)
        self.pb_30.clicked.connect(self.sleep30)
        self.pb_120.clicked.connect(self.sleep120)
        f = "False"
        for i in range(len(pushs[0])):
            self.role = cur.execute(f'''SELECT adm FROM main WHERE SN="{user}"''').fetchall()[0][0]
            if user in pushs[6][i].split('-'):
                lgbt = f'У вас новое сообщение в столбце "{pushs[1][i]}" канбана "{pushs[0][i]}" '
                self.listWidget.addItem(lgbt)
            if self.role == 'Admin':
                f = pushs[4][i]
            if self.role == 'Editor':
                f = pushs[5][i]
            if f == "True":
                dtl = datetime.datetime(int(pushs[3][i].split('.')[0]),
                                        int(pushs[3][i].split('.')[1]), int(pushs[3][i].split('.')[2]))
                now = datetime.datetime.now()
                if dtl > now:
                    lwt = f'У {pushs[2][i].split(".")[0]} осталось {str((dtl - now).days)} д. до завершения задания в '\
                          f'столбце "{pushs[1][i].split(".")[0]}" канбана "{pushs[0][i].split(".")[0]}" '
                elif dtl < now:
                    lwt = f'У {pushs[2][i].split(".")[0]} просрочилось на {str((now - dtl).days)} д. задание в столбце'\
                          f' "{pushs[1][i].split(".")[0]}" канбана "{pushs[0][i].split(".")[0]}" '
                else:
                    lwt = f'У {pushs[2][i].split(".")[0]} сегодня завершается задание в столбце' \
                          f' "{pushs[1][i].split(".")[0]}" канбана "{pushs[0][i].split(".")[0]}"'
                self.listWidget.addItem(lwt)
        self.timerS = QTimer(self)
        self.timerS.timeout.connect(self.rePush)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.closeTime)
        self.timer.start(15000)

    def closeTime(self):
        if self.f:
            self.close()
            self.timer.stop()

    def sleep10(self):
        self.f = False
        self.timerS.start(600000)
        self.close()

    def sleep10p(self):
        self.pb_10.setStyleSheet('border-radius: 5px;\nborder-bottom: 4px solid  rgb(154, 91, 40);\nbackground-color: '
                                 'rgb(195, 113, 51);\ncolor: rgb(233, 233, 233);\nmargin-top: 3px;\nfont: 81 10pt '
                                 '"Rockwell Extra Bold";')

    def sleep30p(self):
        self.pb_30.setStyleSheet('border-radius: 5px;\nborder-bottom: 4px solid  rgb(154, 91, 40);\nbackground-color: '
                                 'rgb(195, 113, 51);\ncolor: rgb(233, 233, 233);\nmargin-top: 3px;\nfont: 81 10pt '
                                 '"Rockwell Extra Bold";')

    def sleep120p(self):
        self.pb_120.setStyleSheet('border-radius: 5px;\nborder-bottom: 4px solid  rgb(154, 91, 40);\nbackground-color: '
                                  'rgb(195, 113, 51);\ncolor: rgb(233, 233, 233);\nmargin-top: 3px;\nfont: 81 10pt '
                                  '"Rockwell Extra Bold";')

    def sleep30(self):
        self.f = False
        self.timerS.start(1800000)
        self.close()

    def sleep120(self):
        self.f = False
        self.timerS.start(7200000)
        self.close()

    def rePush(self):
        self.show()


class AllPush(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('allPush.ui', self)
        print(pushs)
        f = None
        for i in range(len(pushs[0])):
            self.role = cur.execute(f'''SELECT adm FROM main WHERE SN="{user}"''').fetchall()[0][0]
            p = str(pushs[6][i]).split('-')
            print(p)
            if user in p:
                lgbt = f'У вас новое сообщение в столбце "{pushs[1][i]}" канбана "{pushs[0][i]}" '
                self.listWidget.addItem(lgbt)
            if self.role == 'Admin':
                f = pushs[4][i]
            if self.role == 'Editor':
                f = pushs[5][i]
            if f == "True":
                dtl = datetime.datetime(int(pushs[3][i].split('.')[0]), int(pushs[3][i].split('.')[1]),
                                        int(pushs[3][i].split('.')[2]))
                now = datetime.datetime.now()
                if dtl > now:
                    lwt = f'У {pushs[2][i].split(".")[0]} осталось {str((dtl - now).days)} д. до завершения задания в' \
                          f' столбце "{str(pushs[1][i].split(".")[0])}" канбана "{pushs[0][i].split(".")[0]}"'
                elif dtl < now:
                    lwt = f'У {pushs[2][i].split(".")[0]} просрочилось на {str((now - dtl).days)} д. задание в' \
                          f' столбце {str(pushs[1][i].split(".")[0])}" канбана "{pushs[0][i].split(".")[0]}" '
                else:
                    lwt = f'У {pushs[2][i].split(".")[0]} сегодня завершается задание в столбце' \
                          f' "{str(pushs[1][i].split(".")[0])}" канбана "{pushs[0][i].split(".")[0]}"'
                self.listWidget.addItem(lwt)
        memory = open('timeE.txt', 'r')
        m = memory.read()
        self.timeEdit.setTime(QTime(int(m.split(':')[0]), int(m.split(':')[1])))
        memory.close()
        self.pb_save.clicked.connect(self.save)

    def save(self):
        memory = open('timeE.txt', 'w')
        memory.write(':'.join([str(self.timeEdit.time().hour()), str(self.timeEdit.time().minute())]))
        memory.close()


class Kanbaner(QMainWindow):
    global user, con, cur, pushs

    def __init__(self):
        super().__init__()
        self.rowTitlesR, self.titles, self.check_admin, self.rowNum, self.check_editor = [], [], [], [], []
        self.kanbanid, self.ispolns, self.datesK = [], [], []
        uic.loadUi('main.ui', self)
        self.pb_allPush.setIcon(QIcon('bell.ico'))
        self.pb_allPush.setIconSize(QSize(40, 40))
        self.role = cur.execute(f'''SELECT adm FROM main WHERE SN="{user}"''').fetchall()[0][0]
        self.label.setText(user)
        if self.role == 'Admin':
            self.pb_create.clicked.connect(self.creater)
            self.pb_delete.clicked.connect(self.delete)
            self.pb_finance.clicked.connect(self.cash)
            self.pb_graph.clicked.connect(self.graphics)
        else:
            self.pb_create.setParent(None)
            self.pb_finance.setParent(None)
            self.pb_delete.setParent(None)
            self.pb_graph.setParent(None)
        self.pb_open.clicked.connect(self.open)
        self.pb_login.clicked.connect(self.exit)
        self.pb_allPush.clicked.connect(self.showAllPush)
        self.title = ''
        self.rowTitlesBad = []
        self.rowTitles = []
        self.id = len(cur.execute('''SELECT id FROM kanban''').fetchall())
        for i in range(self.id, 0, -1):
            a, b, c, d, e = str(cur.execute('''SELECT * FROM kanban WHERE id = ?''',
                                            [str(i)]).fetchall())[6:-2].replace("'", '').split(', ')
            self.rowTitles.append(d.split())
            self.tw.addTopLevelItem(QTreeWidgetItem([a, e, b, c]))
        self.gr = None
        self.crew = None
        self.new = None
        self.task = None
        self.enter = None
        self.allPush = None
        self.finance = None
        self.push = None
        self.com, self.rowTitlesR, self.titles, self.rowNum, self.kanbanid, self.ispolns, self.datesK = [], [], [], [], [], [], []
        self.reloadPush = QTimer(self)
        self.reloadPush.timeout.connect(self.reloadPushing)
        self.reloadPushing()
        self.timeForPush = QTimer(self)
        self.timeForPush.timeout.connect(self.showAllPush1)
        self.timeForPush.setInterval(1000)
        self.timeForPush.start()
        self.showPush()

    def showAllPush(self):
        self.allPush = AllPush()
        self.allPush.show()

    def showAllPush1(self):
        memory = open('timeE.txt', 'r')
        m = memory.read()
        if datetime.datetime.now().hour == int(m.split(':')[0]) and datetime.datetime.now().minute == int(
                m.split(':')[1]):
            self.showPush()
            self.timeForPush.stop()
        memory.close()

    def reloadPushing(self):
        global pushs
        pushs = []
        self.reloadPush.stop()
        self.reloadPush.start(120000)
        self.rowTitlesR, self.titles, self.rowNum, self.kanbanid, self.com, self.ispolns, self.datesK = [], [], [], [], [], [], []
        for i in cur.execute('''SELECT * FROM tasks''').fetchall():
            self.rowNum.append(i[2])
            self.kanbanid.append(i[1])
            self.ispolns.append(i[4])
            self.datesK.append(i[6])
            self.check_admin.append(i[7])
            self.check_editor.append(i[8])
            self.com.append(i[11])
        for j in self.kanbanid:
            a = cur.execute(f'''SELECT * FROM kanban WHERE id={str(j)}''').fetchall()
            for i in range(len(a)):
                self.titles.append(a[i][1])
                self.rowTitlesR.append(a[i][4].split()[self.rowNum[i]])
        pushs.append(self.rowTitlesR)
        pushs.append(self.titles)
        pushs.append(self.ispolns)
        pushs.append(self.datesK)
        pushs.append(self.check_admin)
        pushs.append(self.check_editor)
        pushs.append(self.com)

    def showPush(self):
        self.push = Push()
        self.push.show()

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
        self.rowTitles.insert(0, [])
        for i in self.rowTitlesBad:
            if i:
                self.rowTitles[0].append(i)
        self.rowTitles[0].append('Готово')
        if len(self.rowTitles[0]) > 1:
            self.id += 1
            cur.executemany("""INSERT INTO kanban VALUES (?,?,?,?,?,?)""",
                            [(self.id, str(self.title),
                              str(datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d %H:%M:%S")),
                              '-', ' '.join(self.rowTitles[0]), self.rowTitles[0][0])])
            con.commit()
            self.tw.clear()
            for i in range(self.id, 0, -1):
                a, b, c, _, d = str(cur.execute('''SELECT * FROM kanban WHERE id = ?''',
                                                [str(i)]).fetchall())[5:-2].replace("'", '').split(', ')
                self.tw.addTopLevelItem(QTreeWidgetItem([a, d, b, c]))
        else:
            del self.rowTitles[0]
        self.title = ''
        self.new.close()

    def open(self, *ide):
        try:
            if self.role == 'Admin' or self.role == 'Editor':
                if [x.row() for x in self.tw.selectedIndexes()]:
                    pos = int(str([x.row() for x in self.tw.selectedIndexes()])[1])
                    self.task = Task_6(self.rowTitles[pos], cur.execute('''SELECT title FROM kanban WHERE id = ?''',
                                                                        [(str(self.id - pos))]).fetchall()[0][0],
                                       self.id - pos)
                    self.task.show()
                elif ide:
                    pos = ide[0]
                    self.task = Task_6(self.rowTitles[self.id - pos],
                                       cur.execute('''SELECT title FROM kanban WHERE id = ?''',
                                                   [(str(pos))]).fetchall()[0][0], pos)
                    self.task.show()
            else:
                if [x.row() for x in self.tw.selectedIndexes()]:
                    pos = int(str([x.row() for x in self.tw.selectedIndexes()])[1])
                    self.task = Task(self.rowTitles[pos], cur.execute('''SELECT title FROM kanban WHERE id = ?''',
                                                                      [(str(self.id - pos))]).fetchall()[0][0],
                                     self.id - pos)
                    self.task.show()
                elif ide:
                    pos = ide[0]
                    self.task = Task(self.rowTitles[self.id - pos],
                                     cur.execute('''SELECT title FROM kanban WHERE id = ?''',
                                                 [(str(pos))]).fetchall()[0][0], pos)
                    self.task.show()
        except:
            pass

    def cash(self):
        self.finance = Finance()
        self.finance.show()

    def delete(self):
        global task_row
        if [x.row() for x in self.tw.selectedIndexes()]:
            pos = int(str([x.row() for x in self.tw.selectedIndexes()])[1])
            i = self.id - pos
            row = len(self.rowTitles[pos])
            for p in range(row):
                for j in range(
                        len(cur.execute(f'''SELECT id FROM tasks WHERE row = "{p}" AND bind = "{i}"''').fetchall()) - 1,
                        -1, -1):
                    y = cur.execute('''SELECT id FROM tasks WHERE row = ? AND positioning = ? AND bind = ?''',
                                    (str(p), str(j), str(i))).fetchall()[0][0]
                    cur.execute("DELETE FROM tasks WHERE id = ?", [(str(y))])
                    con.commit()
                    for h in range(y, task_row):
                        cur.execute("""UPDATE tasks SET id = ? WHERE id = ?""", [str(h), str(h + 1)])
                    con.commit()
                    task_row -= 1
            for j in range(i, len(cur.execute('''SELECT id FROM kanban''').fetchall())):
                cur.execute("""UPDATE tasks SET bind = ? WHERE bind = ?""", [str(j), str(j + 1)])
            con.commit()
            cur.execute("DELETE FROM kanban WHERE id = ?", [(str(i))])
            con.commit()
            for p in range(i, self.id):
                cur.execute("""UPDATE kanban SET id = ? WHERE id = ?""", [str(p), str(p + 1)])
            con.commit()
            self.id -= 1
            self.tw.takeTopLevelItem(pos)
            del self.rowTitles[pos]

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.open()
        elif event.key() == Qt.Key_Backspace and self.role == 'Admin':
            self.delete()
        elif event.key() == Qt.Key_Delete and self.role == 'Admin':
            self.delete()
        elif event.key() == Qt.Key_Q and self.role == 'Admin':
            self.creater()
        elif event.key() == Qt.Key_W and self.role == 'Admin':
            self.graphics()
        elif event.key() == Qt.Key_E and self.role == 'Admin':
            self.cash()

    def reboot(self, id):
        self.tw.clear()
        for i in range(self.id, 0, -1):
            a, b, c, d, e = str(cur.execute('''SELECT * FROM kanban WHERE id = ?''',
                                            [str(i)]).fetchall())[6:-2].replace("'", '').split(', ')
            self.rowTitles.append(d.split())
            self.tw.addTopLevelItem(QTreeWidgetItem([a, e, b, c]))
        self.open(id)

    def exit(self):
        self.enter = Enter()
        self.enter.show()
        self.close()


app = QApplication(sys.argv)
window = Enter()
window.show()
app.exec_()
cur.close()
con.close()
