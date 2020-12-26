from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QPushButton

from database import DataBase
from final_patients import PatientsFinalWidget


class CertainDoctor(QDialog):
    def __init__(self, patients_id, position):
        super().__init__()
        self.setWindowTitle("Запись на прием")
        self.patients_id, self.position = patients_id, position
        size = (QDesktopWidget().availableGeometry().width(),
                QDesktopWidget().availableGeometry().height())
        self.start_x, self.start_y = size[0] // 4, size[1] // 4
        self.end_x, self.end_y = self.start_x * 3, round(self.start_y * 2.5)
        self.resize(*size)
        self.con = DataBase()
        self.initUI()

    def initUI(self):
        buttons_name = self.con.get_data("doctors", "surname, name",
                                         "position = ?", (self.position,))
        for i, elem in enumerate(buttons_name):
            button = QPushButton(self)
            button.setText(" ".join(elem))
            button.clicked.connect(self.load)
            button.setFont(QFont("Times", 32))
            button.resize(self.end_x - self.start_x, (self.end_y -
                                                      self.start_y) // 3)
            button.move(self.start_x, (self.end_y - self.start_y)
                        // 3 * (i + 1) + 25 * i)

    def load(self):
        surname, name = self.sender().text().split()
        doc_id = self.con.get_data("doctors", "id", "surname = ? AND name = ?",
                                   (surname, name))[0][0]
        self.close()
        patients = PatientsFinalWidget(doc_id, self.patients_id)
        patients.show()
        patients.exec()
