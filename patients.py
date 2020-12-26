from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QPushButton

from certain_doctor import CertainDoctor
from database import DataBase


class PatientsWidget(QDialog):
    def __init__(self, patients_id):
        super().__init__()
        self.setWindowTitle("Запись на прием")
        self.patients_id = patients_id
        size = (QDesktopWidget().availableGeometry().width(),
                QDesktopWidget().availableGeometry().height())
        self.start_x, self.start_y = size[0] // 4, size[1] // 4
        self.end_x, self.end_y = self.start_x * 3, round(self.start_y * 2.5)
        self.resize(*size)
        self.con = DataBase()
        self.initUI()

    def initUI(self):
        buttons_name = self.con.get_data("doctors", "DISTINCT position")
        for i, elem in enumerate(buttons_name):
            button = QPushButton(self)
            button.setText(elem[0])
            button.setFont(QFont("Times", 32))
            button.clicked.connect(self.doctors)
            button.resize(self.end_x - self.start_x,
                          (self.end_y - self.start_y) // 3)
            button.move(self.start_x,
                        (self.end_y - self.start_y) // 3 * (i + 1) + 25 * i)

    def doctors(self):
        position = self.sender().text()
        self.close()
        doctors = CertainDoctor(self.patients_id, position)
        doctors.show()
        doctors.exec()
