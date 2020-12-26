from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(260, 140)
        self.setWindowTitle("Вход")
        # Название окна

        self.label_login = QLabel(self)
        self.label_login.setText('Вход')
        self.label_login.setGeometry(120, 10, 40, 16)
        # Текст "Вход"

        self.label2 = QLabel(self)
        self.label2.setText('Логин')
        self.label2.setGeometry(10, 50, 60, 16)
        # Текст "Логин"

        self.output_login = QLineEdit(self)
        self.output_login.setGeometry(70, 47, 160, 20)
        # Поле "Логин"

        self.label3 = QLabel(self)
        self.label3.setText('Пароль')
        self.label3.setGeometry(10, 80, 60, 16)
        # Текст "Пароль"

        self.output_password = QLineEdit(self)
        self.output_password.setGeometry(70, 77, 160, 20)
        self.output_password.setEchoMode(QLineEdit.Password)
        # Поле "Пароль"

        self.ok = QPushButton(self)
        self.ok.setText('Войти')
        self.ok.setGeometry(120, 100, 117, 32)
        # Кнопка "Войти"

        self.error = QLabel(self)
        self.error.setGeometry(10, 110, 90, 16)
        # Для вывода ошибок
