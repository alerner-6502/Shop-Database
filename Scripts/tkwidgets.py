"""
Цель: Набор общих tkinter функций
Автор: Виталий Павленко
"""

import tkinter as tk
from tkinter import messagebox

from constants import * #pylint: disable=W0401,W0614 # Отключить ошибку: не все константы используются
#разрешить подобное движение для архива с констнтами

# перезагружает элемены любово листа
def call_list_update(my_lst, str_lst, col, color=False):
    """
    Автор: Виталий Павленко
    Цель: Загружает listbox элементами, раскрашивает их если надо
    Ввод: ссылка на обьект Listbox (my_lst), список строк (str_lst),
    цвет, флаг (истина = использовать цвет)
    Вывод: Модифицированый Listbox
    """
    my_lst.delete(0, 'end')
    for x_var, y_var in zip(str_lst, range(100)):
        my_lst.insert(tk.END, x_var)
        if color and y_var % 2 == 0:
            my_lst.itemconfig(y_var, bg=col)


def yes_no_box(question):
    """
    Автор: Виталий Павленко
    Цель: Открывает окно с вопросом
    Вход: Сообщение в виде строки
    Выход: True если нажат 'Yes', иначе возвращает ложь
    """
    ret = messagebox.askquestion(X_MESSAGEBOX, question, icon='warning')
    return ret == 'yes'


def error_box(message):
    """
    Автор: Виталий Павленко
    Цель: Открывает окно с ощибкой
    Вход: Сообщение в виде строки
    Выход: Нет
    """
    messagebox.showerror(X_ERRORBOX, message)


def warning_box(message):
    """
    Автор: Виталий Павленко
    Цель: Открывает окно с предупрежнением
    Вход: Сообщение в виде строки
    Выход: Нет
    """
    messagebox.showwarning(X_WARNINGBOX, message)


def info_box(message):
    """
    Автор: Виталий Павленко
    Цель: Открывает окно с информацией
    Вход: Сообщение в виде строки
    Выход: Нет
    """
    messagebox.showinfo(X_INFOBOX, message)

# ==============================================================
