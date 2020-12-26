from sys import argv, exit

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from database import DataBase
from doc import DocWidget
from login import Login
from password_check import check_password
from phone_check import check_phone
from registration import Registration
from choice import ChoiceWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("project.ui", self)
        # Подключение главного интерфейса

        self.picture.setPixmap(QPixmap("help.png"))
        # Подключение картинки к главному интерфейсу

        self.database = DataBase()
        self.refresh_database()
        # Берем данные из бд

        self.initUI()

    def initUI(self):
        self.reg.clicked.connect(self.registration)
        self.login_patients.clicked.connect(self.login_for_patients)
        self.login_doc.clicked.connect(self.login_for_doc)
        # Подключение кнопок к функциям

    def refresh_database(self):
        self.auth_doc = self.database.get_data("auth_doctors")
        self.doc = self.database.get_data("doctors")
        self.auth_patients = self.database.get_data("auth_patients")
        self.patients = self.database.get_data("patients")

    def registration(self):
        self.reg_patients = Registration()
        self.reg_patients.show()
        self.reg_patients.finish.clicked.connect(self.add_patients)
        self.reg_patients.exec()
        # Подключение интерфейса регистрации

    def add_patients(self):
        try:
            if self.reg_patients.surname.text() == "":
                self.reg_patients.error.resize(100, 16)
                self.reg_patients.error.setText("Введите фамилию!")
                self.reg_patients.error.setStyleSheet("color : red")
                return
                # Проверка поля "Фамилия" на наличие данных

            elif self.reg_patients.name.text() == "":
                self.reg_patients.error.resize(70, 16)
                self.reg_patients.error.setText("Введите имя!")
                self.reg_patients.error.setStyleSheet("color : red")
                return
                # Проверка поля "Имя" на наличие данных

            elif self.reg_patients.phone.text() == "":
                self.reg_patients.error.resize(100, 16)
                self.reg_patients.error.setText("Введите телефон!")
                self.reg_patients.error.setStyleSheet("color : red")
                return
                # Проверка поля "Телефон" на наличие данных

            check_phone(self.reg_patients.phone.text())
            # Проверка поля "Телефон" на корректность данных

            if self.reg_patients.address.text() == "":
                self.reg_patients.error.resize(85, 16)
                self.reg_patients.error.setText("Введите адрес!")
                self.reg_patients.error.setStyleSheet("color : red")
                return
                # Проверка поля "Адрес" на наличие данных

            elif self.reg_patients.login.text() == "":
                self.reg_patients.error.resize(85, 16)
                self.reg_patients.error.setText("Введите логин!")
                self.reg_patients.error.setStyleSheet("color : red")
                return
                # Проверка поля "Логин" на наличие данных

            elif any([self.reg_patients.login.text().strip() == str(i[1])
                      for i in self.auth_patients]):
                self.reg_patients.error.resize(150, 16)
                self.reg_patients.error.setText("Такой логин уже занят!")
                self.reg_patients.error.setStyleSheet("color : red")
                return
                # Проверка данных поля "Логин" на совпадение в бд

            elif self.reg_patients.password.text() == "":
                self.reg_patients.error.resize(90, 16)
                self.reg_patients.error.setText("Введите пароль!")
                self.reg_patients.error.setStyleSheet("color : red")
                return
                # Проверка поля "Пароль" на наличие данных

            elif self.reg_patients.password2.text() == "":
                self.reg_patients.error.resize(150, 16)
                self.reg_patients.error.setText("Введите пароль повторно!")
                self.reg_patients.error.setStyleSheet("color : red")
                return
                # Проверка поля "Повторите пароль" на наличие данных

            check_password(self.reg_patients.password.text())
            # Проверка поля "Пароль" на корректность данных

            if self.reg_patients.password.text() != \
                    self.reg_patients.password2.text():
                self.reg_patients.error.resize(120, 16)
                self.reg_patients.error.setText("Пароли не совпадают!")
                self.reg_patients.error.setStyleSheet("color : red")
                # Сравнение поля "Пароль" и поля "Повторите пароль"

            else:
                date = list(self.reg_patients.
                            birthdate.selectedDate().getDate())
                date2 = " ".join(map(str, date))
                # Дата рождения

                self.database.add_data("auth_patients(login, password)",
                                       (self.reg_patients.login.text(),
                                        self.reg_patients.password.text()))
                self.database.add_data("patients(surname, name, patronymic,"
                                       " gender, phone_number, address,"
                                       " birthdate)",
                                       (self.reg_patients.name.text(),
                                        self.reg_patients.surname.text(),
                                        self.reg_patients.patronymic.text(),
                                        self.reg_patients.
                                        gender.currentText(),
                                        self.reg_patients.phone.text(),
                                        self.reg_patients.address.text(),
                                        date2))
                self.refresh_database()
                # Добавление всех данных в бд

                self.reg_patients.close()
                # Закрытие интерфейса
        except Exception as exc:
            self.reg_patients.error.resize(len(str(exc)) * 6 - 5, 16)
            self.reg_patients.error.setText(str(exc))
            self.reg_patients.error.setStyleSheet("color : red")
            # Отлавливаем ошибки

    def login_for_patients(self):
        self.login_patients = Login()
        self.login_patients.show()
        self.login_patients.ok.clicked.connect(self.check_patients)
        self.login_patients.exec()
        # Подключение интерфейса входа

    def check_patients(self):
        if self.login_patients.output_login.text() != "":
            # Проверка поля "Логин" на наличие данных

            for patients in self.auth_patients:
                id, login, password = patients
                if self.login_patients.output_login.text() == str(login):
                    # Проверка поля "Логин" на корректность данных
                    if self.login_patients.output_password.text() == \
                            str(password):
                        self.login_patients.close()
                        self.load_data_for_patients(id_patients=id)
                        break
                    elif self.login_patients.output_password.text() != "":
                        self.login_patients.error.setText("Неверный "
                                                          "пароль!!!")
                        self.login_patients.error.setStyleSheet("color : red")
                        break
                    else:
                        self.login_patients.error.setText("Введите пароль!!!")
                        self.login_patients.error.setStyleSheet("color : red")
                        break
                    # Проверка поля "Пароль" на корректность данных

            else:
                self.login_patients.error.setText("Неверный логин!!!")
                self.login_patients.error.setStyleSheet("color : red")
        else:
            self.login_patients.error.setText("Введите логин!!!")
            self.login_patients.error.setStyleSheet("color : red")

    def load_data_for_patients(self, id_patients):
        patients = ChoiceWidget(id_patients)
        patients.show()
        patients.exec()
        # Загрузка интерфейса для пациента

    def login_for_doc(self):
        self.login_doc = Login()
        self.login_doc.show()
        self.login_doc.ok.clicked.connect(self.check_doc)
        self.login_doc.exec()
        # Подключение интерфейса входа

    def check_doc(self):
        if self.login_doc.output_login.text() != "":
            # Проверка поля "Логин" на наличие данных

            for doc in self.auth_doc:
                id, login, password = doc
                if self.login_doc.output_login.text() == str(login):
                    # Проверка поля "Логин" на корректность данных

                    if self.login_doc.output_password.text() == str(password):
                        self.login_doc.close()
                        self.load_data_for_doc(id_doc=id)
                        break
                    elif self.login_doc.output_password.text() != "":
                        self.login_doc.error.setText("Неверный пароль!!!")
                        self.login_doc.error.setStyleSheet("color : red")
                        break
                    else:
                        self.login_doc.error.setText("Введите пароль!!!")
                        self.login_doc.error.setStyleSheet("color : red")
                        break
                    # Проверка поля "Пароль" на корректность данных

            else:
                self.login_doc.error.setText("Неверный логин!!!")
                self.login_doc.error.setStyleSheet("color : red")
        else:
            self.login_doc.error.setText("Введите логин!!!")
            self.login_doc.error.setStyleSheet("color : red")

    def load_data_for_doc(self, id_doc):
        doc = DocWidget(id_doc)
        doc.show()
        doc.exec()
        # Загрузка интерфейса для врача


if __name__ == '__main__':
    app = QApplication(argv)
    ex = Window()
    ex.show()
    exit(app.exec())
