from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QPushButton

from certain_doctor import CertainDoctor
from database import DataBase

COLORS = [QColor(0, 213, 124), QColor(255, 252, 121), QColor(0, 150, 255), QColor(148, 55, 255)]


class PatientsWidget(QDialog):
    def __init__(self, patients_id):
        super().__init__()
        self.patients_id = patients_id
        size = (QDesktopWidget().availableGeometry().width(),
                QDesktopWidget().availableGeometry().height())
        print(size)
        self.start_x, self.start_y = size[0] // 4, size[1] // 4
        self.end_x, self.end_y = self.start_x * 3, round(self.start_y * 2.5)
        self.resize(*size)
        self.con = DataBase()
        self.initUI()

    def initUI(self):
        buttons_name = self.con.get_data("doctors", "DISTINCT position")
        print(buttons_name)
        print(self.start_x, self.start_y)
        print(self.end_x, self.end_y)
        for i, elem in enumerate(buttons_name):
            button = QPushButton(self)
            button.setText(elem[0])
            button.setFont(QFont("Times", 32))
            button.clicked.connect(self.doctors)
            button.resize(self.end_x - self.start_x, (self.end_y - self.start_y) // 3)
            button.move(self.start_x, (self.end_y - self.start_y) // 3 * (i + 1) + 25 * i)

    def doctors(self):
        position = self.sender().text()
        print(position)
        self.close()
        doctors = CertainDoctor(self.patients_id, position)
        doctors.show()
        doctors.exec()
