class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


combination = ["qwertyuiop"[i:i + 3] for i in range(len("qwertyuiop") - 2)] + \
              ["asdfghjkl"[i:i + 3] for i in range(len("asdfghjkl") - 2)] + \
              ["zxcvbnm"[i:i + 3] for i in range(len("zxcvbnm") - 2)] + \
              ["йцукенгшщзхъ"[i:i + 3] for i
               in range(len("йцукенгшщзхъ") - 2)] + \
              ["фывапролджэ"[i:i + 3] for i
               in range(len("фывапролджэ") - 2)] + \
              ["ячсмитьбю"[i:i + 3] for i
               in range(len("ячсмитьбю") - 2)] + ["жэё"]


# "Запрещенные" комбинации


def check_password(password):
    if len(password) < 9:
        raise LengthError("Слишком маленькая длина пароля!")
        # Проверка длины пароля

    elif password.lower() == password or password.upper() == password:
        raise LetterError("В пароле все буквы одного регистра!")
        # Проверка регистра пароля

    elif not any([i in "1234567890" for i in password]):
        raise DigitError("В пароле нет цифр!")
        # Проверка на наличие цифр в пароле

    for i in range(len(password)):
        if password[i:i + 3].lower() in combination:
            raise SequenceError("В пароле есть легкие комбинации букв")
        # Проверка на "запрещённые" комбинации в пароле
    return True
