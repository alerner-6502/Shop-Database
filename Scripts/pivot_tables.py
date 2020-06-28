#pylint: disable=R0915,E0611,R0915 #pylint не срассматривает содержание библиотеки Library.50 равенств
"""
Автор: Анатолий Лернер
Цель: Формурует сохраняет и илюстрирует отчёт сводная таблица
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as fnt

import numpy as np
import pandas as pd

from tkwidgets import call_list_update
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

def pivot_table(df_var, root, save=False):
    """
    Автор: Анатолий Лернер
    Цель: Формурует, сохраняет и илюстрирует отчёт сводная таблица
    Вход: dataframe, флаг: нужно ли спасти
    Выход: Нет (новое окно и спасённый файл)
    """
    def pivot_table_continue():
        nonlocal str_col
        nonlocal num_col
        nonlocal df_var

        # получаем метод анализа
        sel = method_choice.curselection()[0]
        method_arr = [np.sum, np.mean, np.min, np.max]

        method_box.grab_release()
        # Окно само сябя уничтожает
        method_box.destroy()

        # создаём сводную таблицу
        table_pivot = pd.pivot_table(
            df_var,
            num_col,
            index=str_col[0],
            columns=str_col[1],
            aggfunc=method_arr[sel],
            fill_value=0)
        table_pivot = table_pivot.round(2)

        # добовляем столбец на названиями рядов
        col_names = list(table_pivot.columns.levels[1])
        col_names = ["- " + TAG_DICT[str_col[0]] + " : " +
                     TAG_DICT[num_col[0]] + " -"] + col_names
        row_names = list(table_pivot.index)

        # создаём dataframe для загаловков
        dh_var = pd.DataFrame({'Row': row_names})
        # уничтожаем индексы table_pivot
        table_pivot.reset_index(drop=True, inplace=True)
        # совмещаем таблицы
        table_pivot = pd.concat([dh_var, table_pivot], axis=1, sort=False)
        # rename columns
        table_pivot.columns = col_names

        #print(table_pivot, col_names, row_names)

        if save:
            filename = ANALYSIS_NAMES[1] + \
            " [" + TAG_DICT[num_col[0]] + "]" + "[" + X_AGGREGATION[sel] + "]"
            table_pivot.to_excel(
                './Output/' +
                filename +
                EXP_FORMAT,
                index=False)
            return 0

        # создаём окно и фокусируем его
        analysis_box = tk.Toplevel()
        analysis_box.grab_set()
        analysis_box.focus_set()
        # размер и название окна
        analysis_box.title(ANALYSIS_NAMES[1])
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

        # форматируем столбцы
        for x_var in col_names:
            analysis_tree.heading(x_var, text=x_var)
            analysis_tree.column(
                x_var,
                width=50 +
                fnt.Font().measure(x_var),
                stretch=True,
                anchor='w' if x_var == col_names[0] else 'e')

        # построчно добовляем ряды в таблицу
        for x_var in range(table_pivot.shape[0]):
            lst = list(table_pivot.iloc[x_var])
            analysis_tree.insert('', 'end', values=lst, tags=str(x_var % 2))

        analysis_tree.tag_configure("0", background=W_TREE_ROWCOLOR)
        return 0

    colt = df_var.dtypes
    # список столбцов с качественными атрибутами
    str_col = list(colt[colt == np.object].keys())
    # столбец с числовыми атрибутами,
    num_col = colt[colt != np.object].keys()

    # создаём окно и фокусируем его
    method_box = tk.Toplevel()
    method_box.grab_set()
    method_box.focus_set()
    # размер и название окна
    method_box.title(X_AGG_WIN_NAME)
    method_box.geometry("240x180")
    method_box.resizable(False, False)

    # устанавливаем грид
    for x_var in range(18):
        method_box.grid_rowconfigure(x_var, minsize=10)
        method_box.rowconfigure(x_var, weight=1)
    for x_var in range(24):
        method_box.grid_columnconfigure(x_var, minsize=10)
        method_box.columnconfigure(x_var, weight=1)

    # устанавливаем групповые коробки
    tk.LabelFrame(
        method_box,
        text=X_AGG_GRP_NAME).grid(
            column=1,
            row=1,
            columnspan=22,
            rowspan=16,
            sticky='NSEW')
    tk.Label(
        method_box,
        text=X_AGG_LABEL).grid(
            column=2,
            row=3,
            columnspan=20,
            rowspan=2,
            sticky='NSEW')

    method_choice = tk.Listbox(
        method_box,
        height=4,
        selectmode=tk.SINGLE,
        activestyle='none',
        selectbackground=W_LB_ACTIVE_COL,
        selectforeground="black",
        exportselection=False)
    method_choice.grid(
        column=2,
        row=5,
        columnspan=20,
        rowspan=7,
        sticky='NSEW',
        padx=2)

    method_confirm = tk.Button(
        method_box,
        text=X_AGG_BUTTON,
        command=pivot_table_continue)
    method_confirm.grid(
        column=2,
        row=13,
        columnspan=20,
        rowspan=3,
        sticky='EW')

    call_list_update(method_choice, X_AGGREGATION, W_LIST_COL, False)
    method_choice.select_set(0, last=None)
    #method_box.mainloop()
    root.wait_window(method_box)


# ==============================================================
