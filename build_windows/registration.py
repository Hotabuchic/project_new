from PyQt5 import QtCore, QtWidgets


class Registration(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.resize(420, 700)

        self.label_reg = QtWidgets.QLabel(self)
        self.label_reg.setGeometry(QtCore.QRect(160, 10, 100, 20))
        # Заголовок "Регистрация"

        self.label_surname = QtWidgets.QLabel(self)
        self.label_surname.setGeometry(QtCore.QRect(10, 40, 60, 16))
        # Текст "Фамилия"

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setGeometry(QtCore.QRect(10, 80, 40, 16))
        # Текст "Имя"

        self.label_patronymic = QtWidgets.QLabel(self)
        self.label_patronymic.setGeometry(QtCore.QRect(10, 120, 60, 16))
        # Текст "Отчество"

        self.label_patronymic_help = QtWidgets.QLabel(self)
        self.label_patronymic_help.setGeometry(QtCore.QRect(10, 140, 60, 16))
        # Текст "(если есть)"

        self.label_gender = QtWidgets.QLabel(self)
        self.label_gender.setGeometry(QtCore.QRect(10, 180, 35, 16))
        # Текст "Пол"

        self.label_phone = QtWidgets.QLabel(self)
        self.label_phone.setGeometry(QtCore.QRect(10, 220, 100, 16))
        # Текст "Номер телефона"

        self.label_address = QtWidgets.QLabel(self)
        self.label_address.setGeometry(QtCore.QRect(10, 260, 40, 16))
        # Текст "Адрес"

        self.label_date = QtWidgets.QLabel(self)
        self.label_date.setGeometry(QtCore.QRect(10, 320, 85, 16))
        # Текст "Дата рождения"

        self.birthdate = QtWidgets.QCalendarWidget(self)
        self.birthdate.setGeometry(QtCore.QRect(100, 310, 311, 181))
        # Календарь для ввода даты рождения

        self.label_login = QtWidgets.QLabel(self)
        self.label_login.setGeometry(QtCore.QRect(10, 520, 40, 16))
        # Текст "Логин"

        self.label_password = QtWidgets.QLabel(self)
        self.label_password.setGeometry(QtCore.QRect(10, 560, 40, 16))
        # Текст "Пароль"

        self.label_password2 = QtWidgets.QLabel(self)
        self.label_password2.setGeometry(QtCore.QRect(10, 600, 100, 16))
        # Текст "Повторите пароль"

        self.error = QtWidgets.QLabel(self)
        self.error.setGeometry(QtCore.QRect(10, 650, 230, 16))
        # Для вывода ошибок

        self.finish = QtWidgets.QPushButton(self)
        self.finish.setGeometry(QtCore.QRect(240, 640, 170, 40))
        self.finish.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        # Кнопка "Завершить регистрацию"

        self.surname = QtWidgets.QLineEdit(self)
        self.surname.setGeometry(QtCore.QRect(80, 40, 300, 20))
        # Поле "Фамилия"

        self.name = QtWidgets.QLineEdit(self)
        self.name.setGeometry(QtCore.QRect(80, 80, 300, 20))
        # Поле "Имя"

        self.patronymic = QtWidgets.QLineEdit(self)
        self.patronymic.setGeometry(QtCore.QRect(80, 120, 300, 20))
        # Поле "Отчество"

        self.phone = QtWidgets.QLineEdit(self)
        self.phone.setGeometry(QtCore.QRect(120, 220, 200, 20))
        # Поле "Телефон"

        self.address = QtWidgets.QLineEdit(self)
        self.address.setGeometry(QtCore.QRect(70, 260, 320, 20))
        # Поле "Адрес"

        self.login = QtWidgets.QLineEdit(self)
        self.login.setGeometry(QtCore.QRect(70, 520, 300, 20))
        # Поле "Логин"

        self.password = QtWidgets.QLineEdit(self)
        self.password.setGeometry(QtCore.QRect(70, 560, 300, 20))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # Поле "Пароль"

        self.password2 = QtWidgets.QLineEdit(self)
        self.password2.setGeometry(QtCore.QRect(120, 600, 250, 20))
        self.password2.setEchoMode(QtWidgets.QLineEdit.Password)
        # Поле "Повторите пароль"

        self.gender = QtWidgets.QComboBox(self)
        self.gender.move(50, 180)
        self.gender.addItem("Мужской")
        self.gender.addItem("Женский")
        # Combobox для ввода пола

        QtCore.QMetaObject.connectSlotsByName(self)
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("self", "Регистрация"))
        self.label_reg.setText(_translate("self", "<html><head/><body><p>"
                                                  "<span style=\" font-size:12pt;"
                                                  "\">Регистрация</span>"
                                                  "</p></body></html>"))
        self.label_surname.setText(_translate("self", "Фамилия"))
        self.label_name.setText(_translate("self", "Имя"))
        self.label_patronymic.setText(_translate("self", "Отчество"))
        self.label_gender.setText(_translate("self", "Пол"))
        self.label_phone.setText(_translate("self", "Номер телефона"))
        self.label_address.setText(_translate("self", "Адрес"))
        self.label_date.setText(_translate("self", "Дата рождения"))
        self.label_login.setText(_translate("self", "Логин"))
        self.label_password.setText(_translate("self", "Пароль"))
        self.label_password2.setText(_translate("self", "Повторите пароль"))
        self.finish.setText(_translate("self", "Закончить регистрацию"))
        # Установка стилей и т.д.
