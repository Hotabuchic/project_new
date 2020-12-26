from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QPushButton

from patients import PatientsWidget
from my_appointments import ViewWidget


class ChoiceWidget(QDialog):
    def __init__(self, patients_id):
        super().__init__()
        self.setWindowTitle("Запись на прием")
        self.resize(400, 360)
        self.patients_id = patients_id

        self.check = QPushButton(self)
        self.check.setText("Просмотр моих записей")
        self.check.setFont(QFont("Times", 24))
        self.check.clicked.connect(self.view)
        self.check.resize(380, 150)
        self.check.move(10, 0)

        self.check = QPushButton(self)
        self.check.setText("Записаться")
        self.check.setFont(QFont("Times", 24))
        self.check.clicked.connect(self.start)
        self.check.resize(380, 150)
        self.check.move(10, 190)

    def view(self):
        self.close()
        view = ViewWidget(self.patients_id)
        view.show()
        view.exec()

    def start(self):
        self.close()
        patients = PatientsWidget(self.patients_id)
        patients.show()
        patients.exec()
