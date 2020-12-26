def check_phone(number):
    number = number.lstrip().replace("\t", "").replace("\n", "").replace(" ", "")
    # Удаление лишних элементов

    if number.startswith("8"):
        number = number.replace("8", "+7", 1)
        # Редактирование под более "удобный" формат

    count = sum(1 for i in number if i in "1234567890")
    # Считаем кол-во цифр

    if not (number.count("--") == 0 and ((number.count("(") == 0 and number.count(")") == 0)
                                         or (number.count("(") == 1 and number.count(")") == 1
                                             and number.find("(") < number.find(")"))) and
            number.replace("+", "").replace("-", "").replace("(", "").replace(")", "").isdigit()) \
            or not number.startswith("+"):
        raise Exception("Неверный формат!")
        # Проверка формата

    if not number.startswith("+7") and not number.startswith("+1") \
            and not number.startswith("+55") and not number.startswith("+359"):
        raise Exception("Не определяется код страны!")
        # Проверка кода страны

    if count != 11:
        raise Exception("Неверное количество цифр!")
        # Проверка кол-ва цифр

    number = number.replace("-", "").replace("(", "").replace(")", "")
    if number.startswith("+7") and int(number.replace("+7", "", 1)[:3]) \
            not in [i for i in range(902, 907)] + \
            [i for i in range(910, 940)] + [i for i in range(960, 970)] \
            + [i for i in range(980, 996)]:
        raise Exception("Не определяется оператор сотовой связи!")
        # Проверка оператора связи

    return True
