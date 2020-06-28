"""
Автор: Анатолий Лернер
Цель: Формурует, сохраняет и илюстрирует отчёт основные статистики
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as fnt

import numpy as np
import pandas as pd

from constants import * #pylint: disable=W0401,W0614 # Отключить ошибку: не все константы используются
#разрешить подобное движение для архива с констнтами

# =============== Локальные переменные ======================

#Перенести эти по факту константы в скрипт "constants.py" нельзя.
#Поскольку Tags короые здесь изпользуются критичны для работы программы.
TAG_LIST = [
    "Prod", "Comp", "Type", "Volt", "Bits", "Inps", "Moun", \
    "Mfac", "Coun", "Rati", "Cost", "Avai", "Prop"]
TAG_DICT = dict(zip(TAG_LIST, TAG_NAME_LIST))

# =============== Функции для текстовых отчётов =============

def basic_statistics(df_var, root, save=False):
    """
    Автор: Анатолий Лернер
    Цель: Формурует, сохраняет и илюстрирует отчёт основные статистики
    Вход: dataframe, флаг: нужно ли спасти
    Выход: Нет (новое окно и спасённый файл)
    """
    # dataframe с основной статистикой
    da_var = df_var.describe(include='all')
    da_var = da_var.round(2)
    # describe не обязательно возвращает таблицу с 11'Ю столбцами. Чтоб
    # обеспечить постояннный размер мы соеденяем его.
    full_index = [
        'count',
        'unique',
        'top',
        'freq',
        'mean',
        'std',
        'min',
        '25%',
        '50%',
        '75%',
        'max']
    dm_var = pd.DataFrame(np.NaN, index=full_index, columns=df_var.columns)
    dm_var.update(da_var)
    da_var = dm_var.fillna('-')

    # создаём dataframe для загаловков
    dh_var = pd.DataFrame({'Prop': X_STATLIST})
    # уничтожаем индексы da
    da_var.reset_index(drop=True, inplace=True)
    # совмещаем таблицы
    da_var = pd.concat([dh_var, da_var], axis=1, sort=False)

    if save:
        TAG_DICT.update({'Prop': X_STATISTICS})
        da_var.columns = [TAG_DICT[x] for x in da_var.columns]
        del TAG_DICT['Prop']
        filename = ANALYSIS_NAMES[0]
        da_var.to_excel('./Output/' + filename + EXP_FORMAT, index=False)
        return None

    # создаём окно и фокусируем его
    analysis_box = tk.Toplevel()
    analysis_box.grab_set()
    analysis_box.focus_set()
    # размер и название окна
    analysis_box.title(ANALYSIS_NAMES[0])
    analysis_box.geometry("770x370")
    analysis_box.resizable(False, False)

    # устанавливаем грид
    for x_var in range(37):
        analysis_box.grid_rowconfigure(x_var, minsize=10)
        analysis_box.rowconfigure(x_var, weight=1)
    for x_var in range(77):
        analysis_box.grid_columnconfigure(x_var, minsize=10)
        analysis_box.columnconfigure(x_var, weight=1)

    # устанавливаем групповые коробки
    tk.LabelFrame(
        analysis_box,
        text=E_GB_NAME).grid(
            column=1,
            row=1,
            columnspan=75,
            rowspan=35,
            sticky='NSEW')

    col_names = (list(da_var.columns))

    analysis_tree = ttk.Treeview(
        analysis_box,
        columns=col_names,
        show="headings",
        height=3,
        padding=0,
        selectmode='none')
    analysis_tree_ys = ttk.Scrollbar(
        analysis_box,
        orient="vertical",
        command=analysis_tree.yview)
    analysis_tree_xs = ttk.Scrollbar(
        analysis_box,
        orient="horizontal",
        command=analysis_tree.xview)
    analysis_tree.configure(
        yscrollcommand=analysis_tree_ys.set,
        xscrollcommand=analysis_tree_xs.set)
    analysis_tree.grid(
        column=2,
        row=4,
        columnspan=71,
        rowspan=29,
        sticky='NSEW')
    analysis_tree_xs.grid(
        column=2,
        row=33,
        columnspan=71,
        rowspan=2,
        sticky='NSEW')
    analysis_tree_ys.grid(
        column=73,
        row=4,
        columnspan=2,
        rowspan=29,
        sticky='NSEW')

    # временно добавляем элемент
    TAG_DICT.update({'Prop': X_STATISTICS})
    # форматируем столбцы
    for x_var in col_names:
        analysis_tree.heading(x_var, text=TAG_DICT[x_var])
        analysis_tree.column(
            x_var,
            width=50 +
            fnt.Font().measure(
                TAG_DICT[x_var]),
            stretch=True,
            anchor='w' if x_var == 'Prop' else 'e')
    del TAG_DICT['Prop']

    # построчно добовляем ряды в таблицу
    for x_var in range(da_var.shape[0]):
        lst = list(da_var.iloc[x_var])
        analysis_tree.insert('', 'end', values=lst, tags=str(x_var % 2))

    analysis_tree.tag_configure("0", background=W_TREE_ROWCOLOR)
    # главное окно ждёт наше окно
    root.wait_window(analysis_box)
    return None

# ==============================================================
