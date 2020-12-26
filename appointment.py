from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPlainTextEdit, QPushButton

from database import DataBase


class NewAppointment(QDialog):
    def __init__(self, time, date, docId, patients_id=None):
        super().__init__()
        self.resize(400, 360)
        self.setWindowTitle('Новая запись')
        self.time, self.date, self.docid = time, date, docId
        day = date.strftime('%d %b')

        date_label = QLabel(self)
        date_label.setText(f'Дата:\t\t{day}')
        date_label.move(15, 10)

        time_label = QLabel(self)
        time_label.setText(f'Время:\t\t{time}')
        time_label.move(15, 40)

        patient_label = QLabel(self)
        patient_label.setText(f'Пациент:\t')
        patient_label.move(15, 70)

        self.con = DataBase()

        self.patients_combo = QComboBox(self)
        self.patients_combo.move(115, 65)
        if patients_id is not None:
            patient = self.con.get_data("patients", 'surname, name, '
                                                    'patronymic',
                                        "id = ?", (patients_id,))[0]
            self.patients_combo.addItem(f'{patient[0]} {patient[1]} '
                                        f'{patient[2]}')
            self.patients_combo.setEnabled(False)
        else:
            patients = self.con.get_data('patients', 'surname, name, '
                                                     'patronymic')
            for i in range(len(patients)):
                surname, name, patronymic = patients[i]
                self.patients_combo.addItem(f'{surname} {name} {patronymic}')

        appointments_label = QLabel(self)
        appointments_label.setText('Жалобы:\t\t')
        appointments_label.move(15, 100)

        self.appointments_input = QPlainTextEdit(self)
        self.appointments_input.setGeometry(125, 100, 250, 190)

        self.add_appointment_btn = QPushButton(self)
        self.add_appointment_btn.move(280, 305)
        self.add_appointment_btn.setText('Создать')
