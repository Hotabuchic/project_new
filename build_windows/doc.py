import datetime as dt

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QDialog, QDesktopWidget,
                             QTableWidget, QTableWidgetItem)

from appointment import NewAppointment
from database import DataBase
from info_for_doc import Information

WEEKDAYS = {'Sunday': 'Вс', 'Monday': 'Пн', 'Tuesday': 'Вт', 'Wednesday': 'Ср',
            'Thursday': 'Чт', 'Friday': 'Пт', 'Saturday': 'Сб'}


class DocWidget(QDialog):
    def __init__(self, doc_id):
        super().__init__()
        self.docId = doc_id
        size = (QDesktopWidget().availableGeometry().width(),
                QDesktopWidget().availableGeometry().height())
        self.resize(*size)
        self.setWindowTitle('Личный кабинет')
        self.database = DataBase()

        self.table = QTableWidget(self)
        self.table.resize(*size)
        self.table.setColumnCount(15)
        self.setTableTime()
        self.setTableDates()
        self.fill_table()
        self.table.setStyleSheet('gridline-color: #6B6B6B')
        self.table.cellClicked.connect(self.info)
        self.table.cellDoubleClicked.connect(self.new_appoint)

    def new_appoint(self, r, c):
        item = self.table.item(r, c)
        self.last_r, self.last_c = r, c
        date, time = self.dates[c + 1], self.times[r]
        if item.text() == ' ' and \
                item.background().color().name() == '#e1e1e1':
            self.mini_app = NewAppointment(time, date, self.docId)
            self.mini_app.show()
            self.mini_app.add_appointment_btn.clicked. \
                connect(self.add_appointment)
            # Добавление записи

    def add_appointment(self):
        day = self.mini_app.date.strftime('%d %b')
        sql = [self.mini_app.patients_combo.currentIndex() + 1,
               self.mini_app.docid,
               self.mini_app.appointments_input.toPlainText(),
               self.mini_app.time, day]
        self.mini_app.con.add_data('appointments', sql)
        self.mini_app.close()
        self.new_cell(self.last_r, self.last_c)

    def new_cell(self, r, c):
        note = self.database.get_data('appointments', '*')[-1]
        full_name = self.database.get_data('patients', 'surname, name',
                                           f'id={note[0]}')[0]
        full_name = ' '.join(full_name)
        item = f'{full_name}, {note[3]}, {note[-1]}'
        self.table.setItem(r, c, QTableWidgetItem(item))
        self.table.item(r, c).setBackground(QColor(255, 252, 121))
        self.table.resizeColumnsToContents()

    def info(self):
        if self.table.currentItem().text() != ' ':
            data = self.table.currentItem().text().split(", ")
            info = Information(data[0], data[1], data[2], self.docId)
            info.show()
            info.exec()

    def setTableTime(self):
        time_list = self.database.get_data("doctors", "Monday,"
                                                      " Tuesday, Wednesday,"
                                                      " Thursday, Friday,"
                                                      " Saturday, Sunday",
                                           "id=?", (self.docId,))[0]
        time_of_rec = self.database.get_data("doctors", "rec_time",
                                             "id=?", (self.docId,))[0][0]
        self.time_of_rec = time_of_rec

        # Нахождение самого раннего и самого позднего начала смены
        maxx = -1
        minn = 25
        time_list = list(time_list)
        for i in time_list:
            if i is None:
                continue
            if int(i.split('-')[0]) < minn:
                minn = int(i.split('-')[0])
            if int(i.split('-')[1]) > maxx:
                maxx = int(i.split('-')[1])
        self.min_time, self.max_time = minn, maxx

        self.table.setRowCount((maxx - minn) * 60 // time_of_rec)

        start = dt.datetime.combine(dt.date.today(), dt.time(hour=minn))
        self.times = []  # список с временами в строквом виде

        self.count = (maxx - minn) * 60 // time_of_rec
        # максимальное кол-во строк в таблице

        for i in range(self.count):
            delta = dt.timedelta(minutes=time_of_rec)
            timee = start.strftime('%H:%M') + '-' + (start + delta).\
                strftime('%H:%M')
            start += delta
            self.times.append(timee)
        self.table.setVerticalHeaderLabels(self.times)
        for i in range(len(self.times)):
            self.table.verticalHeaderItem(i).setBackground(QColor('#F5F5F5'))
        # заполнение времени

    def setTableDates(self):
        now = dt.date.today()
        self.datesInStr = []
        self.dates = [now]
        for i in range(15):
            delta = dt.timedelta(days=i)
            var = now + delta
            self.dates.append(var)
            wd = var.strftime('%A')
            wd = WEEKDAYS[wd]
            self.datesInStr.append(wd + var.strftime(',  %d %b'))
        self.table.setHorizontalHeaderLabels(self.datesInStr)
        for i in range(15):
            self.table.horizontalHeaderItem(i).setBackground(QColor('#F5F5F5'))
        self.table.resizeColumnsToContents()

    def fill_table(self):
        for i in range(15):
            wd = self.dates[i].strftime('%A')
            a = self.database.get_data('doctors', wd, f'id={self.docId}')[0][0]
            minn, maxx = list(map(int, a.split('-')))
            for j in range(len(self.times)):
                self.table.setItem(j, i, QTableWidgetItem(' '))
                if not (j in range((minn - self.min_time) * 60 //
                                   self.time_of_rec)) and not (
                        j > (- self.min_time + maxx) * 60 //
                        self.time_of_rec - 1):
                    self.table.item(j, i).setBackground(QColor('#e1e1e1'))
                else:
                    continue
                date, time = self.datesInStr[i][5:], self.times[j]
                a = self.database.get_data('appointments', 'id_patients',
                                           f'time="{time}" and day='
                                           f'"{date}" and '
                                           f'id_doctors={self.docId}')
                if not a:
                    continue
                a = self.database.get_data('patients', 'surname, name',
                                           f'id={a[0][0]}')[0]
                self.table.setItem(j, i, QTableWidgetItem(f'{a[0]} {a[1]},'
                                                          f' {time}, {date}'))
                self.table.item(j, i).setBackground(QColor('#FFFC79'))
                self.table.resizeColumnsToContents()
