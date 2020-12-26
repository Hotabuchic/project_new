import datetime as dt

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QTableWidget, QTableWidgetItem

from appointment import NewAppointment
from database import DataBase


class PatientsFinalWidget(QDialog):
    def __init__(self, doc_id, patients_id):
        super().__init__()
        self.setWindowTitle("Запись на прием")
        self.docId = doc_id
        self.patients_id = patients_id
        size = (QDesktopWidget().availableGeometry().width(),
                QDesktopWidget().availableGeometry().height())
        self.resize(*size)
        self.table = QTableWidget(self)
        self.table.resize(*size)
        self.table.setColumnCount(15)
        self.database = DataBase()
        self.setTableTime()
        self.table_trans = {'Sunday': 'Вс', 'Monday': 'Пн', 'Tuesday': 'Вт', 'Wednesday': 'Ср',
                            'Thursday': 'Чт', 'Friday': 'Пт', 'Saturday': 'Сб'}
        self.setTableDates()
        self.table.setStyleSheet('gridline-color: #6B6B6B')
        self.table.cellDoubleClicked.connect(self.new_appoint)
        # ЗАМЕНИТЬ ПОТОМ НА cellClicked

    def new_appoint(self, r, c):
        item = self.table.item(r, c)
        date, time = self.dates[c + 1], self.times[r]
        if item.text() == ' ' and item.background().color() == QColor(225, 225, 225):
            addApp = NewAppointment(time, date, self.docId, self.patients_id)
            addApp.show()
            addApp.exec_()
            self.setTableDates()

    def setTableTime(self):
        time_list = self.database.get_data("doctors", "Monday, Tuesday, Wednesday,"
                                                      " Thursday, Friday, Saturday, Sunday",
                                           "id=?", (self.docId,))[0]
        time_of_rec = self.database.get_data("doctors", "rec_time", "id=?", (self.docId,))[0][0]
        self.time_of_rec = time_of_rec
        minn = 25
        maxx = -1
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
        self.times = []
        self.count = (maxx - minn) * 60 // time_of_rec
        for i in range(self.count):
            delta = dt.timedelta(minutes=time_of_rec)
            timee = start.strftime('%H:%M') + '-' + (start + delta).strftime('%H:%M')
            start += delta
            self.times.append(timee)
        self.table.setVerticalHeaderLabels(self.times)
        for i in range(len(self.times)):
            self.table.verticalHeaderItem(i).setBackground(QColor(245, 245, 245))
        # заполнение времени

    def setTableDates(self):
        now = dt.date.today()
        lst = []
        con = DataBase()
        self.dates = [now]
        for i in range(15):
            delta = dt.timedelta(days=i)
            var = now + delta
            self.dates.append(var)
            wd = var.strftime('%A')
            wd = self.table_trans[wd]
            lst.append(wd + var.strftime(',  %d %b'))
            rasp = con.get_data('doctors', var.strftime('%A'), f'id={self.docId}')[0][0]
            minn, maxx = [int(i) for i in rasp.split('-')]
            for j in range(self.count):
                recording = con.get_data("appointments, patients",
                                         "patients.surname, patients.name",
                                         "appointments.time = ? AND appointments.day = ?"
                                         " AND appointments.id_patients"
                                         " = (SELECT id FROM patients)",
                                         (self.times[j], lst[i].split()[1]
                                          + " " + lst[i].split()[2]))
                # СЮДА ПОДХОДЯТ ВСЕ ЗАПИСИ!!! ДАЖЕ СВОИ!!
                if len(recording) != 0:
                    self.table.setItem(j, i, QTableWidgetItem("---"))
                else:
                    self.table.setItem(j, i, QTableWidgetItem(" "))

                if not (j in range((minn - self.min_time) * 60 // self.time_of_rec)) and not (
                        j > (- self.min_time + maxx) * 60 // self.time_of_rec - 1):
                    self.table.item(j, i).setBackground(QColor(225, 225, 225))
                if self.table.item(j, i).text() != ' ':
                    self.table.item(j, i).setBackground(QColor('#7F8080'))
        self.table.setHorizontalHeaderLabels(lst)
        for i in range(15):
            self.table.horizontalHeaderItem(i).setBackground(QColor(245, 245, 245))
        self.table.resizeColumnsToContents()
