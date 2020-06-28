#pylint: disable=E1101,R0915 #pylint не срассматривает содержание библиотеки Library. 50 равенств
"""
Автор: Анатолий Лернер, Виталий Павленко
Цель: Создаёт окно сосотоящие из Edit-boxes для атрибутов
"""

import tkinter as tk

import Library as lib
from constants import * #pylint: disable=W0401,W0614 # Отключить ошибку: не все константы используются
#разрешить подобное движение для архива с констнтами

from tkwidgets import error_box

# =============== Локальные переменные ======================

#Перенести эти по факту константы в скрипт "constants.py" нельзя.
#Поскольку Tags короые здесь изпользуются критичны для работы программы.
TAG_LIST = [
    "Prod", "Comp", "Type", "Volt", "Bits", "Inps", "Moun", \
    "Mfac", "Coun", "Rati", "Cost", "Avai", "Prop"]
TAG_DICT = dict(zip(TAG_LIST, TAG_NAME_LIST))

# ================================================

def show_edit_box(
        root,
        title,
        inp, #[entries, prohibited, required, formating]
        testfunction=None):
    """
    Автор: Анатолий Лернер
    Цель: Данная функция создаёт окно сосотоящие из Edit-boxes для атрибутов.
    Вход: Root - родитель(окно),
    Title - Имя окна,
    inp->Entries - Словарь состояший из атрибутов (ключи) которым надо предоставить
    активизированые Edit-boxes, ключам присвоены значения которые иницализируют Edit-box
    inp->Prohibited - Словарь состояший из атрибутов (ключи), которым просвоены списки
    с нелегальными значениями
    inp->Required - Словарь состояший из атрибутов (ключи), которым просвоены списки с
    обязательными значениями.
    Если ссловарь пуст то щитается что обезательных значений нет
    inp->Formating - Словарь состояший из атрибутов (ключи), которым просвоены форматы в
    котором они должны быть
    TestFunction - ссылка на функцию для дополнительнго анализа данных на легитивность
    Выход: Results - Словарь состояший из элемнтов которые надо было показать (ключи),
    и значения которые были этим элемтам присвоены (значения словаря).
    Словарь будет пуст если окно насильно закрыли.
    Зависимость: При построении окна функция считывает данные из глобальной
    переменной "TAG_DICT" чтобы иметь
    под рукой полный список всевозможных атрибутов
    """
    results = {}

    def call_local_ok():
        """
        Автор: Анатолий Лернер
        Цель: Вызывается кнопкой подтверждения Запускает проверку введённых данных.
        Вход: Нет
        Выход: Изменённые локальные переменные
        """
        nonlocal results
        # записываем содержание всех активных Editboxes в список, заодно
        # убираем все пробелы
        num = [(x_a.get()).replace(" ", "") for x_a in entry_list]
        # сшиваем значения с названиями атрибутов и записываем всё в словарь
        results = dict(zip(inp[0].keys(), num))
        # преверяем все введённые значения на легальность
        for x_var in results.keys():
            # преобразование и проверка на формат
            if x_var in inp[3].keys():
                if inp[3][x_var] == 'int':
                    try:
                        results[x_var] = int(results[x_var])
                    except BaseException:
                        results = {}
                        error_box(TAG_DICT[x_var] + MSG_EDIT_INT_ERROR)
                        return 0
                if inp[3][x_var] == 'float':
                    try:
                        results[x_var] = float(results[x_var])
                    except BaseException:
                        results = {}
                        error_box(TAG_DICT[x_var] + MSG_EDIT_FLOAT_ERROR)
                        return 0
            # проверка на нелигальные элементы
            if x_var in inp[1].keys():
                if results[x_var] in inp[1][x_var]:
                    results = {}
                    error_box(TAG_DICT[x_var] + MSG_EDIT_UNIQUE_ERROR)
                    # досрочный выход из функции
                    return 0
            # проверка на обязательные элементы
            if x_var in inp[2].keys():
                if not results[x_var] in inp[2][x_var]:
                    results = {}
                    error_box(TAG_DICT[x_var] + MSG_EDIT_SIMILAR_ERROR)
                    # досрочный выход из функции
                    return 0
        # дополнительная проверка данных на легитивность
        if not testfunction is None:
            flag, error_msg = testfunction(results)
            if not flag:
                results = {}
                error_box(error_msg)
                return 0
        # Убераем фокус с нашего окна
        entry_box.grab_release()
        # Уничтожаем его
        entry_box.destroy()
        return None

    def call_local_clear():
        """
        Автор: Анатолий Лернер
        Цель: Вызывается кнопкой очистить значения
        Вход: Нет
        Выход: Изменённые локальные переменные
        """
        # стираем содержание всех активных Editboxes
        for x_var in entry_list:
            x_var.delete(0, tk.END)

    # создаём окно и фокусируем его
    entry_box = tk.Toplevel()
    entry_box.grab_set()
    entry_box.focus_set()
    # размер и название окна
    entry_box.title(title)
    entry_box.geometry("350x470")
    entry_box.resizable(False, False)

    # устанавливаем грид
    for x_1 in range(47):
        entry_box.grid_rowconfigure(x_1, minsize=10)
        entry_box.rowconfigure(x_1, weight=1)
    for x_1 in range(35):
        entry_box.grid_columnconfigure(x_1, minsize=10)
        entry_box.columnconfigure(x_1, weight=1)

    # устанавливаем групповые коробки
    tk.LabelFrame(
        entry_box,
        text=E_GB_NAME).grid(
            column=1, row=1, columnspan=33, rowspan=45, sticky='NSEW')

    # список указателей на коробки с вводом
    entry_list = []
    # добавляем к окну labels и entry boxes
    for x_1, y_1 in zip(TAG_DICT.keys(), range(4, 100, 3)):
        # деактивизируем те коробки оторые не указаны в inp[0]
        # добовляем labels
        en_var = 'normal' if x_1 in inp[0].keys() else 'disable'
        tk.Label(
            entry_box,
            text=TAG_DICT[x_1],
            state=en_var).grid(column=3, row=y_1, columnspan=13, rowspan=2, sticky='W')
        # добовляем entry boxes
        e_var = tk.Entry(
            entry_box, state=en_var,
            textvariable=tk.StringVar(
                entry_box,
                value=inp[0][x_1] if x_1 in inp[0].keys() else ''))
        e_var.grid(column=17, row=y_1, columnspan=15, rowspan=2, sticky='EW')
        # доболяй к списку указателей только те кнопки которые активны
        if en_var == 'normal':
            entry_list.append(e_var)

    button_clear = tk.Button(entry_box, text=E_CB_TEXT, command=call_local_clear)
    button_clear.grid(column=3, row=41, columnspan=14, rowspan=3, sticky='EW')

    button_ok = tk.Button(entry_box, text=E_OKB_TEXT, command=call_local_ok)
    button_ok.grid(column=18, row=41, columnspan=14, rowspan=3, sticky='EW')

    # главное окно ждёт наше окно
    root.wait_window(entry_box)
    return results


# дополнительный тест для проверки формата (можно использовать)
def filter_entry_format_test(results):
    """
    Автор: Виталий Павленко
    Цель: Проверяет если введённые значения для атрибутов
    соответствует тому или иному типу
    Вход: Словарь содержащий введённые атрибуты и значения что им присвоил пользователь
    Выход: Тупль из флага (легален ли ввод) и строку с ошибкой
    """
    formats = {
        'Cost': 'float',
        'Avai': 'int',
        'Volt': 'float',
        'Bits': 'int',
        'Inps': 'int',
        'Rati': 'float'}
    for x_var in results.keys():
        lst, flg = lib.words_to_list(results[x_var])
        # проверяем что разделитель '+' используется правильно
        if not flg:
            return (
                False,
                MSG_PLUS_ERROR_P1 +
                TAG_DICT[x_var] +
                MSG_PLUS_ERROR_P2)
        # проверяем что некоротые строки содержат числа в правильном формате
        if x_var in formats.keys():
            if formats[x_var] == 'int':
                try:
                    lst = list(map(int, lst))
                except BaseException:
                    return (False, TAG_DICT[x_var] + MSG_INT_ERROR)
            if formats[x_var] == 'float':
                try:
                    lst = list(map(float, lst))
                except BaseException:
                    return (False, TAG_DICT[x_var] + MSG_FLOAT_ERROR)
    return (True, "")

# ==============================================================
