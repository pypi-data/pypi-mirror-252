from string import ascii_uppercase, ascii_lowercase
ru_uppercase = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦШЩЪЫЬЭЮЯ'
ru_lowercase = 'абвгдеёжзийклмнопрстуфхцшщъыьэюя'


def caesar_cipher_shift(string: str, rot: int, alphabet=ru_lowercase, side='l'):
    """
    Смещение символов строки с помощью шифра Цезаря по заранее заданному алфавиту и шагу смещения. Смещение происходит влево
    :param string: строка котору надо сместить
    :param rot: на сколько символов смещать
    :param alphabet: алфавит по которому будет смещение
    :param side: направление смещения, l - влево, r - вправо
    :return: смещённая строка
    """
    shifted_string = ''
    if side == 'l':
        for i in string:
            if alphabet.find(i) != -1:
                shifted_string += alphabet[alphabet.find(i) - rot]
            else:
                shifted_string += i
    elif side == 'r':
        for i in string:
            if alphabet.find(i) != -1:
                shifted_string += alphabet[(alphabet.find(i) + rot) % len(alphabet)]
            else:
                shifted_string += i
    return shifted_string


def caesar_cipher_decode(string: str, alphabet=ru_lowercase, side='r'):
    """
    Все возможные смещения символов строки с помощью шифра Цезаря по заранее заданному алфавиту. Смещение происходит вправо
    :param string: строка котору надо сместить
    :param alphabet: алфавит по которому будет смещение
    :param side: направление смещения, l - влево, r - вправо
    :return: список смещённых строк с указанием шага смещения
    """
    a = []
    for rot in range(len(alphabet)):
        a.append([caesar_cipher_shift(string, rot, alphabet=alphabet, side=side), rot])
    return a
