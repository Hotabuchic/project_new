from PyQt5.QtWidgets import QDialog, QLabel

from database import DataBase


class Information(QDialog):
    def __init__(self, name, time, day):
        super().__init__()
        self.setGeometry(300, 300, 300, 300)

        self.name = QLabel(self)
        self.name.setText(name)
        self.name.move(120, 30)

        self.time = QLabel(time)
        self.time.setText(time)
        self.time.move(130, 70)

        self.day = QLabel(day)
        self.day.setText(day)
        self.day.move(135, 110)
