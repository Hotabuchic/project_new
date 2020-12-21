from PyQt5.QtWidgets import QDialog, QLabel, QTextEdit

from database import DataBase


class Information(QDialog):
    def __init__(self, name, time, day, doc_id):
        super().__init__()
        self.setGeometry(300, 300, 280, 350)

        self.name = QLabel(self)
        self.name.setText(name)
        self.name.move(120, 20)

        self.time = QLabel(self)
        self.time.setText(time)
        self.time.move(130, 50)

        self.day = QLabel(self)
        self.day.setText(day)
        self.day.move(135, 80)

        self.complaint_label = QLabel(self)
        self.complaint_label.setText("Жалобы:")
        self.complaint_label.move(130, 115)

        self.con = DataBase()

        complaint = self.con.get_data("appointments",
                                      "reasons",
                                      "id_patients="
                                      "(SELECT id FROM patients WHERE surname=? AND name=?)"
                                      " AND time=? AND day=? AND id_doctors=?",
                                      (name.split()[0], name.split()[1], time, day, doc_id))[0][0]
        self.complaint = QTextEdit(self)
        self.complaint.setText(complaint)
        self.complaint.move(10, 140)
        self.complaint.setEnabled(False)

