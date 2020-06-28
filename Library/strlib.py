"""
Цель: Набор общих функций
Автор: Виталий Павленко, Анатолий Лернер
"""

import os

def keys_to_values(lst, ref_dict):
    """
    Автор: Виталий Павленко
    Ввод: Список слов и словарь (dict)
    Вывод: Список новых слов (b) которые соответствуют ключам в словаре
    """
    ret = []
    for x_var in ref_dict.keys():
        if x_var in lst:
            ret.append(ref_dict[x_var])
    return ret


def split_path(path, ext):
    """
    Автор: Виталий Павленко
    Цель: Разбивает путь на три базовых элемента
    Вход: путь и формат которой при надобности добавляется
    Выход: список[каталог, имя файла, формат]
    """
    folder, name = os.path.split(path)
    name, extension = os.path.splitext(name)
    folder = folder + "/"
    if extension != ext:
        extension = extension + ext
    return [folder, name, extension]


def words_to_list(in_str):
    """
    Автор: Виталий Павленко
    Цель: Преобразует строку из слов (которые разделённы плюсами) в список слов
    Вход: строка
    Выход: Тупль содержащий список слов и error-флаг
    Если флаг лож, преобразование невозможно
    """
    # проверяем если строка пустая
    if not in_str:
        return ([], True)
    # проверяем чтобы не было знака + на начале и конце строки
    if in_str[0] == "+" or in_str[len(in_str) - 1] == "+":
        return ([], False)
    # если у нас только одно слово, то возвращаем его
    if in_str.count(" ") == 0 and in_str.count("+") == 0:
        return ([in_str], True)
    # так как мы вернули попытались вернуть одно слово, здесь могут быть
    # два слова без соеденения "+"
    if in_str.count("+") == 0:
        return ([], False)
    # считаем количество плюсов, чтобы понять сколько в итоге слов должно быть
    # в списке
    count_plus = in_str.count("+")
    # разделяем строку по знаку "+" на список
    listword = in_str.split("+")
    # так как у нас знак "+" стоит между слов, то количество слов должно быть равно
    # количеству знаков   "+" +1
    if len(listword) != count_plus + 1:
        return ([], False)
    return (listword, True)


def matplot_point_generator(init=False):
    """
    Автор: Виталий Павленко
    Цель: Генерирует новый точку-формат каждый раз эта функция вызывается
    Вход: Флаг для инициализации
    Выход: строка обозначающая формат
    """
    # инициализация
    if init:
        matplot_point_generator.col = 0
        matplot_point_generator.shp = 0
    # список цветов и фигур
    colors = ['k', 'g', 'r', 'c', 'm', 'y', 'b']
    shapes = ['o', 's', '^', 'D', '*', '+', ]
    ret = colors[matplot_point_generator.col] + \
        shapes[matplot_point_generator.shp]
    # счётчик первого уровня
    matplot_point_generator.col = (
        matplot_point_generator.col + 1) % len(colors)
    # счётчик второго уровня
    if matplot_point_generator.col == 0:
        matplot_point_generator.shp = (
            matplot_point_generator.shp + 1) % len(shapes)
    return ret


# обязательная глобальная инициализация
matplot_point_generator.col = 0
matplot_point_generator.shp = 0


def get_color_list(n_lst):
    """
    Автор: Анатолий Лернер
    Цель: Генерирует список уникальных цветов (произвольная длинна)
    Вход: Длинна списка
    Выход: Список цветов
    """
    colors = [
        '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0',
        '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8',
        '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff']
    return [colors[x_var % len(colors)] for x_var in range(n_lst)]

# ==============================================================
