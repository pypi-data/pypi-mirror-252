from string import ascii_uppercase, ascii_lowercase

ru_uppercase = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦШЩЪЫЬЭЮЯ'
ru_lowercase = 'абвгдеёжзийклмнопрстуфхцшщъыьэюя'


def shift(string: str, rot: int, alphabet: str = ru_lowercase, side: int = 1):
    """
    Смещение символов строки с помощью шифра Цезаря по заранее заданному алфавиту и шагу смещения. Смещение происходит влево
    :param string: строка котору надо сместить
    :param rot: на сколько символов смещать
    :param alphabet: алфавит по которому будет смещение
    :param side: направление смещения, 1 - влево, -1 - вправо
    :return: смещённая строка
    """
    assert side in (-1, 1)

    shifted_string = ''
    for i in string:
        if alphabet.find(i) != -1:
            shifted_string += alphabet[(alphabet.find(i) - rot * side) % len(alphabet)]
        else:
            shifted_string += i
    return shifted_string


def decode(string: str, alphabet: str = ru_lowercase, side: int = -1):
    """
    Все возможные смещения символов строки с помощью шифра Цезаря по заранее заданному алфавиту. Смещение происходит вправо
    :param string: строка котору надо сместить
    :param alphabet: алфавит по которому будет смещение
    :param side: направление смещения, 1 - влево, -1 - вправо
    :return: список смещённых строк с указанием шага смещения
    """
    assert side in (-1, 1)

    a = []
    for rot in range(len(alphabet)):
        a.append([shift(string, rot, alphabet=alphabet, side=side), rot])
    return a
