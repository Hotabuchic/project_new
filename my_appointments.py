from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QListWidget, QListWidgetItem
from pymorphy2 import MorphAnalyzer

from database import DataBase


class ViewWidget(QDialog):
    def __init__(self, patients_id):
        super().__init__()
        self.setWindowTitle("Просмотр записей")
        self.resize(500, 520)

        self.label_view = QLabel(self)
        self.label_view.setText("Ваши записи:")
        self.label_view.setFont(QFont("Times", 16))
        self.label_view.move(150, 8)

        self.view = QListWidget(self)
        self.view.resize(480, 480)
        self.view.move(10, 32)

        self.con = DataBase()
        self.appointments = self.con.get_data("appointments",
                                              "id_doctors, time, day",
                                              "id_patients = ?",
                                              (patients_id,))

        if len(self.appointments) != 0:
            self.morph = MorphAnalyzer()
            for appointment in self.appointments:
                doc_id, time, day = appointment
                surname, name, position = self.con.get_data("doctors",
                                                            "surname,"
                                                            " name, "
                                                            "position")[0]
                item = QListWidgetItem(f"""
                Запись к
                {self.morph.parse(position)[0].inflect({'datv'}).word.capitalize()} 
                {self.morph.parse(surname)[0].inflect({'datv'}).word.capitalize()} 
                {self.morph.parse(name)[0].inflect({'datv'}).word.capitalize()}
                на {day} в {time}
                """)
                item.setFont(QFont("Times", 20))
                self.view.addItem(item)
