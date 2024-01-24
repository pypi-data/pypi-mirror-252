from string import digits, ascii_uppercase

HEX = digits + ascii_uppercase  # алфавит символов от 0 до Z (36 символов)


def convert_to_base(num: int, base: int):
    """
    Перевод из десятичной СИ в необходимую СИ\n
    Если base > 36 возвращает список цифр числа в десятичной СИ
    :param num: исходное число в десятичной СИ
    :param base: в какую СИ
    :return: новое число
    """
    if base <= 36:
        r = ''
        while num > 0:
            r += HEX[num % base]
            num //= base
        return r[::-1]
    else:
        r = []
        while num > 0:
            r.append(num % base)
            num //= base
        return r[::-1]


def convert_from_base_to_base(num: str | list[int], fbase: int, tbase: int):
    """
    Перевод числа из исходной СИ в необходимую СИ\n
    Если fbase > 36 нужно вводить число списком цифр исходного числа в десятичной СИ\n
    Если tbase > 36 возвращает список цифр числа в десятичной СИ
    :param num: исходное число
    :param fbase: из какой СИ
    :param tbase: в какую СИ
    :return: новое число
    """
    if fbase <= 36:
        num = int(str(num), fbase)
    else:
        k = 0
        num_temp = 0
        while num:
            num_temp += num.pop() * (fbase ** k)
            k += 1
        num = num_temp
    return convert_to_base(num, tbase)


def convert_3(num: int):
    """
    Перевод числа из десятичной СИ в троичную СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 3)
def convert_4(num: int):
    """
    Перевод числа из десятичной СИ в четверичную СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 4)
def convert_5(num: int):
    """
    Перевод числа из десятичной СИ в пятеричную СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 5)
def convert_6(num: int):
    """
    Перевод числа из десятичной СИ в шестеричную СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 6)
def convert_7(num: int):
    """
    Перевод числа из десятичной СИ в семеричную СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 7)
def convert_9(num: int):
    """
    Перевод числа из десятичной СИ в девятеричную СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 9)
def convert_11(num: int):
    """
    Перевод числа из десятичной СИ в одиннадцатеричную СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 11)
def convert_12(num: int):
    """
    Перевод числа из десятичной СИ в двенадцатеричную СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 12)
def convert_13(num: int):
    """
    Перевод числа из десятичной СИ в тринадцатеричная СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 13)
def convert_14(num: int):
    """
    Перевод числа из десятичной СИ в четырнадцатеричной СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 14)
def convert_15(num: int):
    """
    Перевод числа из десятичной СИ в пятнадцетеричной СИ
    :param num: исходное число в десятичной СИ
    :return: новое число
    """
    return convert_to_base(num, 15)