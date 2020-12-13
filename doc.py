import datetime as dt

from PyQt5.QtWidgets import QDialog, QDesktopWidget, QTableWidget

from database import DataBase


class DocWidget(QDialog):
    def __init__(self, doc_id):
        super().__init__()
        self.docId = doc_id
        size = (QDesktopWidget().availableGeometry().width(), QDesktopWidget().availableGeometry().height())
        self.resize(*size)
        self.table = QTableWidget(self)
        self.table.resize(1100, size[1] - 30)
        self.table.setColumnCount(14)
        self.database = DataBase()
        self.setTableTime()
        self.table_trans = {'Sunday': 'Вс', 'Monday': 'Пн', 'Tuesday': 'Вт', 'Wednesday': 'Ср', 'Thursday': 'Чт',
                            'Friday': 'Пт', 'Saturday': 'Сб'}
        self.setTableDates()

    def setTableTime(self):
        time_list = self.database.get_data("doctors", "Monday, Tuesday, Wednesday,"
                                                      " Thursday, Friday, Saturday, Sunday",
                                           "id=?", (self.docId,))[0]
        time_of_rec = self.database.get_data("doctors", "rec_time", "id=?", (self.docId,))[0][0]
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

        self.table.setRowCount((maxx - minn) * 60 // time_of_rec)
        start = dt.datetime.combine(dt.date.today(), dt.time(hour=minn))
        times = []
        for i in range((maxx - minn) * 60 // time_of_rec):
            delta = dt.timedelta(minutes=time_of_rec)
            timee = start.strftime('%H:%M') + '-' + (start + delta).strftime('%H:%M')
            start += delta
            times.append(timee)
        self.table.setVerticalHeaderLabels(times)
        # заполнение времени

    def setTableDates(self):
        now = dt.date.today()
        lst = []
        for i in range(14):
            delta = dt.timedelta(days=i)
            var = now + delta
            wd = var.strftime('%A')
            print(self.database.get_data("doctors", wd, "id=?", (self.docId,))[0])
            wd = self.table_trans[wd]
            lst.append(wd + var.strftime(',  %d %b'))
        self.table.setHorizontalHeaderLabels(lst)

    def color(self, table, i, color):
        for j in range(table.columnCount()):
            table.item(i, j).setBackground(color)

# app = QApplication(sys.argv)
# ex = DocWidget(2)
# ex.show()
# sys.exit(app.exec())
