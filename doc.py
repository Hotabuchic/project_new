import datetime as dt
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor

from database import DataBase
from info_for_doc import Information
from random import randint

COLORS = [QColor(0, 213, 124), QColor(255, 252, 121), QColor(0, 150, 255), QColor(148, 55, 255)]


class DocWidget(QDialog):
    def __init__(self, doc_id):
        super().__init__()
        self.docId = doc_id
        size = (QDesktopWidget().availableGeometry().width(),
                QDesktopWidget().availableGeometry().height())
        self.resize(*size)
        self.table = QTableWidget(self)
        self.table.resize(1100, size[1] - 30)
        self.table.setColumnCount(14)
        self.database = DataBase()
        self.setTableTime()
        self.table_trans = {'Sunday': 'Вс', 'Monday': 'Пн', 'Tuesday': 'Вт', 'Wednesday': 'Ср',
                            'Thursday': 'Чт', 'Friday': 'Пт', 'Saturday': 'Сб'}
        self.setTableDates()
        self.table.cellClicked.connect(self.info)
        self.table.resizeColumnsToContents()
        # ЗАМЕНИТЬ ПОТОМ НА cellClicked

    def info(self):
        if self.table.currentItem().text() != ' ':
            data = self.table.currentItem().text().split(", ")
            info = Information(data[0], data[1], data[2], self.docId)
            info.show()
            info.exec()
            # В ячейке где кто-то записан должно быть написано его ФИ, время и день
            # Формат записи должен быть такой: Иванов Иван, 08:30-08:45, 20 Dec
            # ОЧЕНЬ ЖЕЛАТЕЛЬНО ЧТОБЫ ВРЕМЯ И ДЕНЬ НЕ БЫЛО ВИДНО В ТАБЛИЦЕ
            # Ячейка где кто то записан должна быть закрашена красным, свободная - зеленым,
            # А ячейка в которое время врач не работает - серым цветом

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
        # заполнение времени

    def setTableDates(self):
        now = dt.date.today()
        lst = []
        con = DataBase()
        recordings = con.get_data("appointments", criterion="id_doctors = ?",
                                  data_criterion=(self.docId,))
        for i in range(14):
            delta = dt.timedelta(days=i)
            var = now + delta
            wd = var.strftime('%A')
            wd = self.table_trans[wd]
            lst.append(wd + var.strftime(',  %d %b'))
            rasp = con.get_data('doctors', var.strftime('%A'), f'id={self.docId}')[0][0]
            minn, maxx = [int(i) for i in rasp.split('-')]
            if len(recordings) != 0:
                for j in range(self.count):
                    recording = con.get_data("appointments, patients",
                                             "patients.surname, patients.name",
                                             "appointments.time = ? AND appointments.day = ?"
                                             " AND appointments.id_patients"
                                             " = (SELECT id FROM patients)",
                                             (self.times[j], lst[i].split()[1]
                                              + " " + lst[i].split()[2]))
                    if len(recording) != 0:
                        recording = recording[0]
                        item = recording[0] + " " + recording[1] + ", " + self.times[j] + \
                               ", " + lst[i].split()[1] + " " + lst[i].split()[2]
                        self.table.setItem(j, i, QTableWidgetItem(item))
                    else:
                        self.table.setItem(j, i, QTableWidgetItem(" "))

                    if not (j in range((minn - self.min_time) * 60 // self.time_of_rec)) and not (
                            j > (- self.min_time + maxx) * 60 // self.time_of_rec - 1):
                        self.table.item(j, i).setBackground(QColor(192, 192, 192))
                    if self.table.item(j, i).text() != ' ':
                        self.table.item(j, i).setBackground(COLORS[randint(0, len(COLORS) - 1)])

        self.table.setHorizontalHeaderLabels(lst)

    def color(self, table, i, color):
        for j in range(table.columnCount()):
            table.item(i, j).setBackground(color)
