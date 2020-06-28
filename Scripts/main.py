#pylint: disable=E0602,W0603,W0614,C0413,E1101
#E0602: отключение "undefined variable" (для импорта констант)
#W0603: отключение "using global variable" (разрешается использовать глобальные переменные)
#W0614: отключение "unused import CONSTANT" (иначе разбить программу на модули не получится)
#C0413: импортировать библиотеки ранее строки 25 невозможно
#E1101: pylint не срассматривает содержание библиотеки Library

#ЗАМЕЧАНИЕ: дополнительные #pylint disable команды находятся ниже.
#Они позволяют использовать lower case глобальные переменные

"""
Проект: Питон в науке о данных
Авторы: Анатолий Лернер, Виталий Павленко
"""
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as fnt
from tkinter import filedialog as fbox

#import numpy as np
import pandas as pd

os.chdir('..')
sys.path.append(os.path.abspath(os.curdir))

import Library as lib
from constants import * #pylint: disable=W0401 # Отключить ошибку: не все константы используются
#разрешить подобное движение для архива с констнтами

#импортируем скрипты для формирования отчётов
from analysis_check import check_data_frame
from scatter_plot import clustered_scatter_plot
from box_plot import box_whisker_plot
from histogram_plot import clustered_hitogram
from column_plot import clustered_column_table
from simple_statistics import basic_statistics
from pivot_tables import pivot_table

#импортируем скрипты для загризки/сожранения pickle файлов
from database_save_load import call_load_source_database, \
call_save_source_database, call_new_database

#импортируем скрипты для фильтра
from filter_edit_window import show_edit_box, filter_entry_format_test

from tkwidgets import call_list_update, yes_no_box, error_box, warning_box, info_box

# =============== Фиункции Управления Интерфейса ============

main_status_tab = 0 #pylint: disable=C0103
# списки выбраных строк. Формат их локален.
main_status_sel_items = [] #pylint: disable=C0103

# список элементов что загружены в фильтр
main_status_filter_items = [] #pylint: disable=C0103
# список столбцов которые можно показать
main_status_show_col = [] #pylint: disable=C0103
# словарь, параметры для строчного фильтра
main_status_show_row = {} #pylint: disable=C0103
# метод по которому дата анализируется
main_status_analysis_choice = 'NONE' #pylint: disable=C0103

# на этих константах построено всё приложение, пользователю их менять
# никогда нельзя
TAG_LIST = ["Prod", "Comp", "Type", "Volt", "Bits", "Inps", "Moun", "Mfac", \
    "Coun", "Rati", "Cost", "Avai", "Prop"]
TAG_DICT = dict(zip(TAG_LIST, TAG_NAME_LIST))
TAB_TAGS = [TAG_LIST[0:2] + TAG_LIST[7:8] + TAG_LIST[10:12],
            TAG_LIST[1:7], TAG_LIST[7:10], TAG_LIST]

# глобальные таблицы
table_core = 0 #pylint: disable=C0103
table_comp = 0 #pylint: disable=C0103
table_manf = 0 #pylint: disable=C0103
table_all = 0 #pylint: disable=C0103
table_onscreen = 0 #pylint: disable=C0103

# путь к нынешнему файлу
current_database_path = ""  #pylint: disable=C0103


def call_main_hard_init():
    """
    Автор: Анатолий Лернер
    Цель: Жёсткая инициализация (когда программа запискается)
    Вход: Нет
    Выход: Изменённые глобальные переменные
    """
    global table_core #pylint: disable=C0103
    global table_comp #pylint: disable=C0103
    global table_manf #pylint: disable=C0103
    global table_all #pylint: disable=C0103
    global current_database_path #pylint: disable=C0103
    current_database_path = './Data/' + DEFAULT_DATABASE + DATABASE_FORMAT
    b_var, table_core, table_comp, table_manf, \
    table_all = call_load_source_database(current_database_path)
    # Датабаза из каталога "Data" не удалось загрузить
    if not b_var:
        error_box(MSG_OPENFAIL + current_database_path)
        table_core, table_comp, table_manf, table_all = call_new_database()
        root.title(W_WINDOW_TITLE + '-')
    else:
        root.title(W_WINDOW_TITLE + DEFAULT_DATABASE + DATABASE_FORMAT)
    call_main_init()


# иницализация
def call_main_init():
    """
    Автор: Анатолий Лернер
    Цель: Обычная инициализация (когда открывается новая база данных)
    Вход: Нет
    Выход: Изменённые глобальные переменные
    """
    global main_status_filter_items #pylint: disable=C0103
    global main_status_show_col #pylint: disable=C0103
    global main_status_show_row #pylint: disable=C0103
    global main_status_sel_items #pylint: disable=C0103
    global main_status_tab #pylint: disable=C0103

    # Инициализировать элемнты анализа, они никогда не меняются
    call_list_update(main_analysis_choice, ANALYSIS_NAMES, W_LIST_COL)

    # Инициализировать элемнты окон для фильтров
    items = lib.keys_to_values(table_core.columns, TAG_DICT)
    call_list_update(main_filter_cchoice, items, W_LIST_COL)
    call_list_update(main_filter_lchoice, items, W_LIST_COL, True)
    call_list_update(main_filter_rchoice, [" "] * len(items), W_LIST_COL, True)
    main_status_filter_items = table_core.columns

    # сбрасываем выбор фильтра и инициализируем список столбцов которые можно
    # показать
    main_filter_cchoice.selection_clear(0, tk.END)
    main_status_show_col = []
    # инициализируем параметры строчного фильтра
    main_status_show_row = {}

    # Инициализировать элемнты контоля
    main_status_tab = 0
    main_nb.select(0)
    main_status_sel_items = []
    # Отсортировать по первому столбцу
    call_table_sort('Prod')
    # Обновить статус специальных окон и разукрасить строки
    call_main_update()
    #print(main_tree.identify("Product", x=0,y=0))


def call_main_update(table_update=True):
    """
    Автор: Анатолий Лернер
    Цель: Обновляет таблицу и статус кнопок на экране
    Вход: флаг: нужно ли обновить таблицу
    Выход: Изменённый статус глобальных переменных
    """
    i = len(main_status_sel_items)
    # Деактивизировать кнопку "Удалить" если ничего не выбрано
    if i > 0 and main_status_tab != 3:
        main_table_delete.configure(state="normal")
    else:
        main_table_delete.configure(state="disabled")
    # Деактивизировать кнопку "Правка" если выбран всего лишь один элемент
    if i == 1 and main_status_tab != 3 and not main_status_show_col:
        main_table_edit.configure(state="normal")
    else:
        main_table_edit.configure(state="disabled")
    if main_status_tab != 3:
        main_table_add.configure(state="normal")
    else:
        main_table_add.configure(state="disabled")

    if table_update:
        tabs = [table_core, table_comp, table_manf, table_all]
        # создаём полную копию нынешнего DataFrame, после этого будем к ней
        # применять фильтры
        tmp = tabs[main_status_tab].copy(deep=True)
        # начинаем AND-OR фильтровку строк (из этой структуры фильтра приходится
        # использовать циклы)
        # инициализируем логическию таблицу для AND логики
        and_table = pd.Series([1] * (tmp.shape)[0], dtype=bool)
        for x_1 in main_status_show_row:
            # если параметры фильтра не пустые
            if main_status_show_row[x_1]:
                # инициализируем логическию таблицу для ОR логики
                or_table = pd.Series([0] * (tmp.shape)[0], dtype=bool)
                # цикл логической OR фильтровки
                for y_1 in main_status_show_row[x_1]:
                    or_table = or_table | (tmp[x_1] == y_1)
                and_table = and_table & or_table
        # применяем фильтр
        tmp = tmp.loc[list(and_table)]
        # фильтровка столбцов (только если список фильтров не пуст)
        if main_status_show_col:
            tmp = tmp[main_status_show_col]
        # переводим отфильтрованый DataFrame в widget на экране
        dataframe_to_treeview(tmp)

    # Лист выбор
    t_1 = [X_TOTAL_ITEMS.format(len(main_tree.get_children(
        ''))), X_SELEC_ITEMS.format(len(main_status_sel_items))]
    call_list_update(main_table_choice, t_1, W_LIST_COL)

    ebl = "disabled"
    # проверяем если таблицу на экране можно проанализировать выбраным методом
    if check_data_frame(table_onscreen, main_status_analysis_choice):
        ebl = "normal"
    main_analysis_analyse.configure(state=ebl)
    main_analysis_export.configure(state=ebl)


def dataframe_to_treeview(frame):
    """
    Автор: Анатолий Лернер
    Цель: Заглузает содержимое dataframe в widget treeview
    Вход: Датафраме
    Выход: Обновлённая таблица (widget treeview)
    """
    global table_onscreen #pylint: disable=C0103
    # спасает копию того чо он сейчас выведет на экран
    table_onscreen = frame.copy(deep=True)
    main_tree.delete(*main_tree.get_children())
    frame_expanded = pd.DataFrame(columns=TAG_DICT.keys())
    frame_expanded = pd.concat(
        [frame_expanded, frame], ignore_index=True, sort=False)
    array = frame_expanded.values
    num_of_rows = array.shape[0]
    for x_1 in range(num_of_rows):
        main_tree.insert('', 'end', values=list(array[x_1, :]), tags=str(x_1 % 2))
    main_tree.configure(displaycolumns=list(frame.columns))
    main_tree.tag_configure("0", background=W_TREE_ROWCOLOR)


# =============== Функции Кнопок Главново Окна ==============

def call_main_table_add():
    """
    Автор: Анатолий Лернер
    Цель: Вызывается кнопкой "добавитьы"
    Вход: Нет
    Выход: Изменённые глобальные переменные
    """
    global table_core #pylint: disable=C0103
    global table_comp #pylint: disable=C0103
    global table_manf #pylint: disable=C0103
    # список атрибутов которые надо показать в окне редактированья
    atr = TAB_TAGS[main_status_tab]
    # пришиваем к атрибутам начальные значения и всё записываем словарь
    mydict = dict(zip(atr, [''] * len(atr)))
    # формуруем словари которые ограничивают вводиммые значения
    #(смотрите docstring "show_edit_box" функции)
    # заодно создаём словарь обязательных форматов
    prohibited = {}
    required = {}
    formats = {}
    if main_status_tab == 0:
        prohibited = {'Prod': table_core['Prod'].tolist()}
        required = {
            'Comp': table_comp['Comp'].tolist(),
            'Mfac': table_manf['Mfac'].tolist()}
        formats = {'Cost': 'float', 'Avai': 'int'}
    if main_status_tab == 1:
        prohibited = {'Comp': table_comp['Comp'].tolist()}
        formats = {'Volt': 'float', 'Bits': 'int', 'Inps': 'int'}
    if main_status_tab == 2:
        prohibited = {'Mfac': table_manf['Mfac'].tolist()}
        formats = {'Rati': 'float'}
    # запускаем окно и ждём результата
    #print(mydict, prohibited, required, sep="\n\n\n")
    elem = show_edit_box(root, X_ADD_ELEMENT, [mydict, prohibited, \
    required, formats], None)
    # если полученый словарь не пуст (ввод закончился успешно), мы добавляем
    # его атрибуты в таблицу
    if elem:
        if main_status_tab == 0:
            table_core = table_core.append(elem, ignore_index=True)
        if main_status_tab == 1:
            table_comp = table_comp.append(elem, ignore_index=True)
        if main_status_tab == 2:
            table_manf = table_manf.append(elem, ignore_index=True)
        call_main_update()


def call_main_table_edit():
    """
    Автор: Анатолий Лернер
    Цель: Вызывается кнопкой "правка", редактирует выбранный элемент
    Вход: Нет
    Выход: Изменённые глобальные переменные
    """
    global table_core #pylint: disable=C0103
    global table_comp #pylint: disable=C0103
    global table_manf #pylint: disable=C0103
    global main_status_sel_items #pylint: disable=C0103
    # воспомогательная таблица
    # ключ выбраного элемнта. Нам гарантировано что он уникален
    item_id = str(
        main_tree.item(main_status_sel_items)['values'][list([0, 1, 7])[main_status_tab]])
    # местонахождение в рабочем DataFrame и сведенья о выбраном элемнте
    if main_status_tab == 0:
        tmp = table_core.loc[table_core['Prod'] == item_id]
    if main_status_tab == 1:
        tmp = table_comp[table_comp['Comp'] == item_id]
    if main_status_tab == 2:
        tmp = table_manf[table_manf['Mfac'] == item_id]
    idx = tmp.index[0]
    tmp = tmp.values.tolist()[0]
    # список атрибутов которые надо показать в окне редактированья
    # atr = TAB_TAGS[main_status_tab]
    # пришиваем к атрибутам начальные значения и всё записываем  в словарь
    mydict = dict(zip(TAB_TAGS[main_status_tab], tmp))
    # формуруем словари которые ограничивают вводиммые значения
    #(смотрите docstring "show_edit_box" функции)
    # заодно создаём словарь обязательных форматов
    prohibited = {}
    required = {}
    formats = {}
    if main_status_tab == 0:
        tmp = table_core['Prod'].tolist()
        tmp.remove(item_id)
        prohibited = {'Prod': tmp}
        required = {
            'Comp': table_comp['Comp'].tolist(),
            'Mfac': table_manf['Mfac'].tolist()}
        formats = {'Cost': 'float', 'Avai': 'int'}
    if main_status_tab == 1:
        tmp = table_comp['Comp'].tolist()
        tmp.remove(item_id)
        prohibited = {'Comp': tmp}
        formats = {'Volt': 'float', 'Bits': 'int', 'Inps': 'int'}
    if main_status_tab == 2:
        tmp = table_manf['Mfac'].tolist()
        tmp.remove(item_id)
        prohibited = {'Mfac': tmp}
        formats = {'Rati': 'float'}
    # запускаем окно и ждём результата
    elem = show_edit_box(root, X_EDIT_ELEMENT, [mydict, prohibited, \
	required, formats], None)
    if elem:
        if main_status_tab == 0:
            # обновляем атрибуты ряда
            table_core.iloc[idx] = elem.values()
        if main_status_tab == 1:
            # обновляем атрибуты ряда
            table_comp.iloc[idx] = elem.values()
            # при надобности обновляем имя под-ключа в основной таблице
            if item_id != elem['Comp']:
                table_core['Comp'] = table_core['Comp'].replace(
                    item_id, elem['Comp'])
                warning_box(MSG_CHANGED_COMP_KEY)
        if main_status_tab == 2:
            # обновляем атрибуты ряда
            table_manf.iloc[idx] = elem.values()
            # при надобности обновляем имя под-ключа в основной таблице
            if item_id != elem['Mfac']:
                table_core['Mfac'] = table_core['Mfac'].replace(
                    item_id, elem['Mfac'])
                warning_box(MSG_CHANGED_MFAC_KEY)
        main_status_sel_items = []
        call_main_update()


def call_main_table_delete():
    """
    Автор: Анатолий Лернер
    Цель: Вызывается кнопкой "удалить", удаляет выбранныe элементы
    Вход: Нет
    Выход: Изменённые глобальные переменные
    """
    # удалить весь выбор
    #[main_tree.delete(x) for x in main_tree.selection()]
    # анулировать выыбор
    global table_core #pylint: disable=C0103
    global table_comp #pylint: disable=C0103
    global table_manf #pylint: disable=C0103
    global main_status_sel_items #pylint: disable=C0103

    if main_status_tab == 0:
        # список treeview ключей из выбранных элемнтов
        key_list = [main_tree.item(x_2)['values'][0]
                    for x_2 in main_status_sel_items]
        for x_3 in key_list:
            # элеметы из таблицы с главным ключом могут удалятся свободно
            table_core = table_core[table_core['Prod'] != x_3]

    if main_status_tab == 1 and yes_no_box(MSG_DELETE_KEY):
        # список ключей из выбранных элемнтов
        key_list = [main_tree.item(x_4)['values'][1]
                    for x_4 in main_status_sel_items]
        for x_5 in key_list:
            # перед тем как удалять под-ключи надо проверить если он(они)
            # используется в таблице с главным ключом
            # если да, то придётся дать пользователю знать о том что элементы
            # которые используют этот под-ключ тоже придётся удалить
            table_core = table_core[table_core['Comp'] != x_5]
            table_comp = table_comp[table_comp['Comp'] != x_5]

    if main_status_tab == 2 and yes_no_box(MSG_DELETE_KEY):
        # список ключей из выбранных элемнтов
        key_list = [main_tree.item(x_6)['values'][7] for x_6 in main_status_sel_items]
        for x_7 in key_list:
            # перед тем как удалять под-ключи надо проверить если он(они)
            # используется в таблице с главным ключом
            # если да, то придётся дать пользователю знать о том что элементы
            # которые используют этот под-ключ тоже придётся удалить
            table_core = table_core[table_core['Mfac'] != x_7]
            table_manf = table_manf[table_manf['Mfac'] != x_7]

    # Очистить список выборов
    main_status_sel_items = []
    # Обновить статус специальных окон
    call_main_update()


def call_main_table_export():
    """
    Автор: Анатолий Лернер
    Цель: экспортирует текстовый отчёт таблицы которую в даный момент можно увидеть на экране
    Вход: Нет (глобальные переменные)
    Выход: Текстовый отчёт в виде ".xlsx" файла
    """
    tmp = table_onscreen.copy(deep=True)
    # эта функция экспортирует исключительно те данные которые можно увидить на экране
    # переименовываем столбцы в DataFrame: ('Prod', 'Price') -> ('Продукт',
    # 'Цена')
    tmp.columns = lib.keys_to_values(tmp.columns, TAG_DICT)
    # Open window
    path = fbox.asksaveasfilename(
        initialfile=INIT_EXPORT_NAME + EXP_FORMAT,
        initialdir="./Output/", title=EXPORTBOX_TITLE,
        filetypes=[(EXP_FORMAT_INTRO, "*" +EXP_FORMAT)])
    # экспортитуем только если путь существует
    if path != "":
        # Разбиваем путь на элемнты
        folder, name, extension = lib.split_path(path, EXP_FORMAT)
        tmp.to_excel(folder + name + extension, index=False)
        info_box(MSG_SAVEOK + "Work/Output")


def call_main_analysis_analyze(save=False):
    """
    Автор: Анатолий Лернер
    Цель: Вызывается кнопкой "анализ", распазнаёт выбор и запускает функции анализа
    Вход: флаг: нужно ли спасти анализ?
    Выход: Строку 'T' если отчёт был текстовый. Строку 'G' если графический
    """
    #корень главного окна
    global root #pylint: disable=C0103
    # получаем соответствующию строку
    selected = main_analysis_choice.curselection()[0]
    # массив указателей на функции
    caller = [basic_statistics, pivot_table, clustered_column_table,
              clustered_hitogram, box_whisker_plot, clustered_scatter_plot]
    # вызываем метод анализа
    if selected < 2:
        caller[selected](table_onscreen, root, save)
        return 'T'
    caller[selected](table_onscreen, save)
    return 'G'


def call_main_analysis_export():
    """
    Автор: Виталий Павленко
    Цель: Вызывается кнопкой "анализ", распазнаёт выбор и запускает функции анализа
    Вход: нет
    Выход: Строку 'T' если отчёт был текстовый. Строку 'G' если графический
    """
    atype = call_main_analysis_analyze(save=True)
    info_box(MSG_SAVEOK + ("Work/Output" if atype == 'T' else "Work/Graphics"))


def call_main_filter_edit():
    """
    Автор: Анатолий Лернер
    Цель: Вызувается кнопкой 'Поправить значения'
          Вызывает окно редактированья для фильтра. Присваивает значения
    Вход: Нет
    Выход: Нет (изменённые глобальные переменные)
    """
    global main_status_show_row #pylint: disable=C0103
    # список атрибутов которые надо показать в окне редактированья
    atr = TAB_TAGS[main_status_tab]
    # присвиваем к атрибутам начальные значения (то что в listbox на данный
    # момент) и всё записываем словарь
    init = list(main_filter_rchoice.get(0, tk.END))
    mydict = dict(zip(atr, init))
    # анулируем словари которые ограничивают вводиммые значения (смотрите
    # docstring "show_edit_box" функции)
    prohibited = {}
    required = {}
    formats = {}
    # запускаем окно и ждём результата
    elem = show_edit_box(root, X_EDIT_FILTER, [mydict, prohibited, required, \
    formats], filter_entry_format_test)
    # затем онбовляем listbox
    if elem:
        # спасаем вертикальное scroll положение нашего listbox
        ypos = main_filter_rchoice.yview()
        # перезагружаем таблицу
        call_list_update(main_filter_rchoice, elem.values(), W_LIST_COL, True)
        # востанавливаем вертикальное scroll положение нашего listbox
        main_filter_rchoice.yview_moveto(ypos[0])
        # конвертируем строки из слов разделённые плюсами в списки слов (или чисел)
        tmp_keys = list(elem.keys())
        for x_8 in tmp_keys:
            elem[x_8] = lib.words_to_list(elem[x_8])[0]
        # теперь нужно конвертировать некоторые строки в или float (по факту
        # все числа в программе имеют тип float)
        formats = ['Cost', 'Avai', 'Volt', 'Bits', 'Inps', 'Rati']
        for x_9 in elem:
            if x_9 in formats:
                elem[x_9] = list(map(float, elem[x_9]))
        main_status_show_row = elem

def call_main_filter_show():
    """
    Автор: Анатолий Лернер
    Цель: При нажатии кнопки "Показать" , эта функвуя обновляет список
    столбцов которые нужно показать.
    А затем просит функцию call_main_update обновить экран
    Вход: глобальные переменные для фильтра столбцов (main_filter_cchoice,
    main_status_show_col, main_status_filter_items)
    Выход: Обновлённая глобальная переменная main_status_show_col
    (список столбцов которые надо показать)
    """
    global main_status_show_col #pylint: disable=C0103
    global main_status_sel_items #pylint: disable=C0103
    # получаем список выбраных элемнтов: индексы
    lst = main_filter_cchoice.curselection()
    #values = [main_filter_cchoice.get(idx) for idx in lst]
    main_status_show_col = [main_status_filter_items[x] for x in lst]
    # Сбрасываем выбор элемнтов если имеется
    main_status_sel_items = []
    call_main_update()


def call_main_filter_clearall():
    """
    Автор: Виталий Павленко
    Цель: При нажатии кнопки "Сбросить всё" , эта функвуя очищает список
    столбцов которые нужно показать.
    Вход: нет
    Выход: Обновлённый глобальный переметр main_filter_cchoice (адрес Listbox)
    """
    # сбрасываем весь выбор и обновляем таблицу
    main_filter_cchoice.selection_clear(0, tk.END)


# =============== Функции Реакции (Event Functions) ==============

# сортировка столбцов таблицы
def call_table_sort(column_id):
    """
    Автор: Виталий Павленко
    Цель: Сортирует элемнтыы нынешнего DataFrame по убыванию в соответствии
    с указаным столбцом
    Нынешней DataFrame определяется содержанием глобальной переменной
    main_status_tab
    Вход: Имя столбца как Tag
    Следствие: Отсортированый столбец нынешнего DataFrame
    Выход: нет
    """
    global table_core #pylint: disable=C0103
    global table_comp #pylint: disable=C0103
    global table_manf #pylint: disable=C0103
    global table_all #pylint: disable=C0103
    # проверяем если Tag столбца легален
    if column_id in TAG_DICT.keys():
        # сортируем по возврастанию для каждого случая
        if main_status_tab == 0:
            table_core = table_core.sort_values(by=column_id)
        if main_status_tab == 1:
            table_comp = table_comp.sort_values(by=column_id)
        if main_status_tab == 2:
            table_manf = table_manf.sort_values(by=column_id)
        if main_status_tab == 3:
            table_all = table_all.sort_values(by=column_id)
        # Обновляем таблицу на экране
        call_main_update()


# переход на новую закладку
def call_notepad_tab(event):
    """
    Автор: Анатолий Лернер
    Цель: Вызывается нажатием мыши на новый tab. Организует переход.
    Вход: event объект
    Выход: Изменённые глобальные переменные
    """
    global main_status_tab #pylint: disable=C0103
    global main_status_sel_items #pylint: disable=C0103
    global table_all #pylint: disable=C0103
    global main_status_filter_items #pylint: disable=C0103
    global main_status_show_col #pylint: disable=C0103
    global main_status_show_row #pylint: disable=C0103
    # Находим индекс выбраной закладки
    i = main_nb.tk.call(main_nb, "identify", "tab", event.x, event.y)
    # если выбрана новая закладка
    if i != main_status_tab and i in range(4):
        main_status_tab = i
        # Сбрасываем выбор элемнтов если имеется
        main_tree.selection_set([])
        main_status_sel_items = []
        # Если закладка сотвествует "все элемты", необходимо зоново вычислить
        # эту таблицу
        if main_status_tab == 3:
            table_all = pd.merge(table_core, table_comp, on="Comp")
            table_all = pd.merge(table_all, table_manf, on="Mfac")
        # Сбрасываем и перезаглужаем параметы фильтров
        items = lib.keys_to_values(TAB_TAGS[main_status_tab], TAG_DICT)
        call_list_update(main_filter_cchoice, items, W_LIST_COL)
        call_list_update(main_filter_lchoice, items, W_LIST_COL, True)
        call_list_update(main_filter_rchoice, [" "] * len(items), W_LIST_COL, True)
        main_status_filter_items = TAB_TAGS[main_status_tab]
        main_status_show_col = []  # tabs[main_status_tab].columns
        main_status_show_row = {}
        # Обновляем экран ()
        call_main_update()


# выбор элемнта в таблице
def call_main_tree_click(event):
    """
    Автор: Анатолий Лернер
    Цель: Вызывается нажатием мыши на элемент таблицы.
    Вход: event объект
    Выход: Изменённые глобальные переменные
    """
    global main_status_sel_items #pylint: disable=C0103
    # список выборов !один клик назад!
    selected = list(main_tree.selection())
    # элемент который только что выбрали
    active = main_tree.identify_row(event.y)
    # Если была нажата кнопка Ctrl
    if event.state & 0x04:
        if active in selected:
            selected.remove(active)
        else:
            selected.append(active)
    elif active:
        selected = [active]
    main_status_sel_items = selected
    call_main_update(False)


# Выбран метод анализа
def call_analysis_click(event):
    """
    Автор: Виталий Павленко
    Цель: Вызывается нажатием мыши на listbox со списком анализов.
    Вход: event объект
    Выход: Изменённые глобальные переменные
    """
    global main_status_analysis_choice #pylint: disable=C0103
    # получаем выбраных элемнт (индекс)
    i = main_analysis_choice.nearest(event.y)
    # получаем соответствующию строку
    main_status_analysis_choice = main_analysis_choice.get(i)
    call_main_update()


def call_main_menu_new():
    """
    Автор: Анатолий Лернер
    Цель: При нажатии вкладки 'Новый' в меню 'База данных'
    Организует создание новой базы данных
    Вход: Нет
    Выход: Изменённые глобальные переменные
    """
    global table_core #pylint: disable=C0103
    global table_comp #pylint: disable=C0103
    global table_manf #pylint: disable=C0103
    global table_all #pylint: disable=C0103
    global current_database_path #pylint: disable=C0103

    path = fbox.asksaveasfilename(
        initialfile=DEFAULT_NEW_DATABASE +
        DATABASE_FORMAT,
        initialdir="./Data/",
        title=SAVEAS_TITLE,
        filetypes=[
            (DATABASE_FORMAT_INTRO,
             "*" +
             DATABASE_FORMAT)])
    if path != "":
        current_database_path = path
        folder, name, extension = lib.split_path(path, DATABASE_FORMAT)
        table_core, table_comp, table_manf, table_all = call_new_database()
        call_save_source_database(folder + name + extension, table_core, table_comp, table_manf)
        root.title(W_WINDOW_TITLE + name + extension)
        call_main_init()


# Меню открыть базу данных
def call_main_menu_open():
    """
    Автор: Анатолий Лернер
    Цель: При нажатии вкладки 'Открыть' в меню 'База данных'
    Организует открытие новой базы данных
    Вход: Нет
    Выход: Изменённые глобальные переменные
    """
    global current_database_path # pylint: disable=invalid-name
    global table_core # pylint: disable=invalid-name
    global table_comp # pylint: disable=invalid-name
    global table_manf # pylint: disable=invalid-name
    global table_all # pylint: disable=invalid-name
    path = fbox.askopenfilename(
        initialdir="./Data/",
        title=OPEN_TITLE,
        filetypes=[
            (DATABASE_FORMAT_INTRO,
             "*" + DATABASE_FORMAT)])
    if path != "":
        current_database_path = path
        flag, table_core, table_comp, table_manf, \
        table_all = call_load_source_database(current_database_path)
        if not flag:
            error_box(MSG_OPENFAIL + path)
        name = os.path.split(path)[1]
        root.title(W_WINDOW_TITLE + name)
        call_main_init()


# Меню спасти базу данных
def call_main_menu_save():
    """
    Автор: Виталий Павленко
    Цель: При нажатии вкладки 'Сохранить' в меню 'База данных'
    Организует сохранение новой базы данных
    Вход: Нет
    Выход: Изменённые глобальные переменные
    """
    call_save_source_database(current_database_path, table_core, table_comp, table_manf)


# Меню спасти базу данных как
def call_main_menu_saveas():
    """
    Автор: Виталий Павленко
    Цель: При нажатии вкладки 'Сохранить как' в меню 'База данных'
    Организует сохранение новой базы данных
    Вход: Нет
    Выход: Нет
    """
    global current_database_path #pylint: disable=C0103
    path = fbox.asksaveasfilename(
        initialdir="./Data/",
        title=SAVEAS_TITLE,
        filetypes=[
            (DATABASE_FORMAT_INTRO,
             "*" + DATABASE_FORMAT)])
    if path != "":
        current_database_path = path
        folder, name, extension = lib.split_path(path, DATABASE_FORMAT)
        call_save_source_database(folder + name + extension, table_core, table_comp, table_manf)
        root.title(W_WINDOW_TITLE + name + extension)
        info_box(MSG_SAVEOK + "Work/Data")

#=============== Установка Главново Окна ===================

root = tk.Tk() #pylint: disable=C0103
root.title(X_MAINFRAME)
root.minsize(970, 570)

#устанавливаем грид
for x in range(50):
    root.grid_rowconfigure(x, minsize=10)
    root.rowconfigure(x, weight=1)
for x in range(93):
    root.grid_columnconfigure(x, minsize=10)
    root.columnconfigure(x, weight=1)

#устанавливаем групповые коробки
tk.LabelFrame(root, text=W_GB_TABLE_TEXT).grid(column=1, row=1, columnspan=19, \
rowspan=13, sticky='NSEW')
tk.LabelFrame(root, text=W_GB_ANLYSIS_TEXT).grid(column=21, row=1, columnspan=19, \
rowspan=13, sticky='NSEW')
tk.LabelFrame(root, text=W_GB_FILTER_TEXT).grid(column=41, row=1, columnspan=51, \
rowspan=13, sticky='NSEW')

#-- устанавливаем блокнот --
st = ttk.Style() #pylint: disable=C0103
st.configure("TNotebook")
#рармер панелей
st.configure("TNotebook.Tab", padding=[20, 4])
main_nb = ttk.Notebook(root) #pylint: disable=C0103
#присваеваем блокноту левую кнопку мыши
main_nb.bind('<Button-1>', call_notepad_tab)
main_nb_pages = [ttk.Frame(main_nb) for x in range(4)] #pylint: disable=C0103
#обозначаем палэли
for x in range(4):
    main_nb.add(main_nb_pages[x], text=TAB_NAMES[x])
main_nb.grid(column=1, row=16, columnspan=91, rowspan=33, sticky='NESW')

#устанавливаем текст
tk.Label(root, text=W_LAB1).grid(column=2, row=3, columnspan=17, rowspan=1, sticky='NSEW')
tk.Label(root, text=W_LAB2).grid(column=22, row=3, columnspan=17, rowspan=1, sticky='NSEW')
tk.Label(root, text=W_LAB3).grid(column=42, row=3, columnspan=15, rowspan=1, sticky='NSEW')
tk.Label(root, text=W_LAB4).grid(column=57, row=3, columnspan=15, rowspan=1, sticky='NSEW')
tk.Label(root, text=W_LAB5).grid(column=74, row=3, columnspan=15, rowspan=1, sticky='NSEW')

#устанавливаем списки
main_table_choice = tk.Listbox( #pylint: disable=C0103
    root, height=3, selectmode=tk.SINGLE, activestyle='none', selectbackground="white", \
    selectforeground="black", highlightthickness=0)
main_table_choice.grid(column=2, row=4, columnspan=17, rowspan=5, sticky='NSEW', padx=2)

main_analysis_choice = tk.Listbox( #pylint: disable=C0103
    root, height=4, selectmode=tk.SINGLE, activestyle='none', selectbackground=W_LB_ACTIVE_COL, \
    selectforeground="black", exportselection=False)
main_analysis_choice.grid(column=22, row=4, columnspan=15, rowspan=6, sticky='NSEW')

main_filter_lchoice = tk.Listbox( #pylint: disable=C0103
    root, height=4, selectmode=tk.SINGLE, activestyle='none', selectbackground="white", \
    selectforeground="black", highlightthickness=0)
main_filter_lchoice.grid(column=42, row=4, columnspan=15, rowspan=6, sticky='NSEW')

main_filter_rchoice = tk.Listbox( #pylint: disable=C0103
    root, height=4, selectmode=tk.SINGLE, activestyle='none', selectbackground="white", \
    selectforeground="black", highlightthickness=0)
main_filter_rchoice.grid(column=57, row=4, columnspan=15, rowspan=6, sticky='NSEW')

main_filter_cchoice = tk.Listbox( #pylint: disable=C0103
    root, height=4, selectmode=tk.MULTIPLE, activestyle='none', selectbackground=W_LB_ACTIVE_COL, \
    selectforeground="black", exportselection=False)
main_analysis_choice.bind('<Button-1>', call_analysis_click)
main_filter_cchoice.grid(column=74, row=4, columnspan=15, rowspan=6, sticky='NSEW')

#устанавливаем кнопки
main_table_add = tk.Button( #pylint: disable=C0103
    root, text=W_BT_ADD_TEXT, command=call_main_table_add)
main_table_add.grid(column=2, row=10, columnspan=8, rowspan=1, sticky='EW')

main_table_edit = tk.Button( #pylint: disable=C0103
    root, text=W_BT_EDIT_TEXT, command=call_main_table_edit)
main_table_edit.grid(column=11, row=10, columnspan=8, rowspan=1, sticky='EW')

main_table_delete = tk.Button( #pylint: disable=C0103
    root, text=W_BT_DELETE_TEXT, command=call_main_table_delete)
main_table_delete.grid(column=2, row=12, columnspan=8, rowspan=1, sticky='EW')

main_table_export = tk.Button( #pylint: disable=C0103
    root, text=W_BT_EXPORT_TEXT, command=call_main_table_export)
main_table_export.grid(column=11, row=12, columnspan=8, rowspan=1, sticky='EW')

main_analysis_analyse = tk.Button( #pylint: disable=C0103
    root, text=W_BT_ANALYSIS_TEXT, command=call_main_analysis_analyze, state="disable")
main_analysis_analyse.grid(column=22, row=12, columnspan=8, rowspan=1, sticky='EW')

main_analysis_export = tk.Button( #pylint: disable=C0103
    root, text=W_BT_EXPORTA_TEXT, command=call_main_analysis_export, state="disable")
main_analysis_export.grid(column=31, row=12, columnspan=8, rowspan=1, sticky='EW')

main_filter_filter = tk.Button( #pylint: disable=C0103
    root, text=W_BT_FILTER_TEXT, command=call_main_filter_show)
main_filter_filter.grid(column=42, row=12, columnspan=14, rowspan=1, sticky='EW')

main_filter_clear = tk.Button( #pylint: disable=C0103
    root, text=W_BT_EDITF_TEXT, command=call_main_filter_edit)
main_filter_clear.grid(column=58, row=12, columnspan=14, rowspan=1, sticky='EW')

main_filter_clearall = tk.Button( #pylint: disable=C0103
    root, text=W_BT_DROPF_TEXT, command=call_main_filter_clearall)
main_filter_clearall.grid(column=75, row=12, columnspan=14, rowspan=1, sticky='EW')

#устанавливаем scroll bars
main_analysis_choice_xs = tk.Scrollbar( #pylint: disable=C0103
    root, orient=tk.HORIZONTAL, command=main_analysis_choice.xview)
main_analysis_choice.config(xscrollcommand=main_analysis_choice_xs.set)
main_analysis_choice_xs.grid(column=22, row=10, columnspan=15, rowspan=1, sticky='EW')

main_analysis_choice_ys = tk.Scrollbar( #pylint: disable=C0103
    root, orient=tk.VERTICAL, command=main_analysis_choice.yview)
main_analysis_choice.config(yscrollcommand=main_analysis_choice_ys.set)
main_analysis_choice_ys.grid(column=37, row=4, columnspan=1, rowspan=6, sticky='NSEW')

main_filter_lchoice_xs = tk.Scrollbar( #pylint: disable=C0103
    root, orient=tk.HORIZONTAL, command=main_filter_lchoice.xview)
main_filter_lchoice.config(xscrollcommand=main_filter_lchoice_xs.set)
main_filter_lchoice_xs.grid(column=42, row=10, columnspan=15, rowspan=1, sticky='EW')

main_filter_rchoice_xs = tk.Scrollbar( #pylint: disable=C0103
    root, orient=tk.HORIZONTAL, command=main_filter_rchoice.xview)
main_filter_rchoice.config(xscrollcommand=main_filter_rchoice_xs.set)
main_filter_rchoice_xs.grid(column=57, row=10, columnspan=15, rowspan=1, sticky='EW')

def scroll_binder(*args):
    """
    Автор: Анатолий Лернер
    Цель: Соеденяет scrollbar двух listboxes
    Вход: event объект
    """
    main_filter_lchoice.yview(*args)
    main_filter_rchoice.yview(*args)
def wheel_scroll_binder(event):
    """
    Автор: Анатолий Лернер
    Цель: Соеденяет scrollbar двух listboxes через колесо мышки
    Вход: event объект
    """
    main_filter_lchoice.yview("scroll", event.delta, "units")
    main_filter_rchoice.yview("scroll", event.delta, "units")
    return "break"
main_filter_lrchoice_ys = tk.Scrollbar(root, orient=tk.VERTICAL) #pylint: disable=C0103
main_filter_lrchoice_ys.config(command=scroll_binder)
main_filter_lchoice.config(yscrollcommand=main_filter_lrchoice_ys.set)
main_filter_rchoice.config(yscrollcommand=main_filter_lrchoice_ys.set)
main_filter_lchoice.bind("<MouseWheel>", wheel_scroll_binder)
main_filter_rchoice.bind("<MouseWheel>", wheel_scroll_binder)
main_filter_lrchoice_ys.grid(column=72, row=4, columnspan=1, rowspan=6, sticky='NSEW')

main_filter_cchoice_xs = tk.Scrollbar( #pylint: disable=C0103
    root, orient=tk.HORIZONTAL, command=main_filter_cchoice.xview, highlightcolor='black')
main_filter_cchoice_xs.grid(column=74, row=10, columnspan=15, rowspan=1, sticky='EW')
main_filter_cchoice_ys = tk.Scrollbar( #pylint: disable=C0103
    root, orient=tk.VERTICAL, command=main_filter_cchoice.yview)
main_filter_cchoice_ys.grid(column=89, row=4, columnspan=1, rowspan=6, sticky='NSEW')
main_filter_cchoice.config(
    yscrollcommand=main_filter_cchoice_ys.set, xscrollcommand=main_filter_cchoice_xs.set)

#устанавливаем главную таблицу
col_str = list(TAG_DICT.keys()) #pylint: disable=C0103
col_lbl = list(TAG_DICT.values()) #pylint: disable=C0103
main_tree = ttk.Treeview( #pylint: disable=C0103
    columns=col_str, show="headings", height=3, padding=0)
main_tree.bind('<Button-1>', call_main_tree_click)
main_tree_ys = ttk.Scrollbar(orient="vertical", command=main_tree.yview) #pylint: disable=C0103
main_tree_xs = ttk.Scrollbar(orient="horizontal", command=main_tree.xview) #pylint: disable=C0103
main_tree.configure(yscrollcommand=main_tree_ys.set, xscrollcommand=main_tree_xs.set)
main_tree.grid(column=2, row=20, columnspan=87, rowspan=27, sticky='NSEW')
main_tree_xs.grid(column=2, row=47, columnspan=87, rowspan=1, sticky='NSEW')
main_tree_ys.grid(column=89, row=20, columnspan=1, rowspan=27, sticky='NSEW')
#форматируем столбцы
for x, y in enumerate(col_str):
    main_tree.heading(col_str[x].title(), text=col_lbl[x]+"\u2800\u2800\u25BC", \
	command=lambda y=col_str[x]: call_table_sort(y))
    main_tree.column(col_str[x], width=50+fnt.Font().measure(col_lbl[x].title()), \
	stretch=True, anchor=TAG_ALIGNMENT[x])

#Добовляем меню
menubar = tk.Menu(root) #pylint: disable=C0103
filemenu = tk.Menu(menubar, tearoff=0) #pylint: disable=C0103
filemenu.add_command(label=M_NEW_TEXT, command=call_main_menu_new)
filemenu.add_command(label=M_OPEN_TEXT, command=call_main_menu_open)
filemenu.add_separator()
filemenu.add_command(label=M_SAVE_TEXT, command=call_main_menu_save)
filemenu.add_command(label=M_SAVEAS_TEXT, command=call_main_menu_saveas)
menubar.add_cascade(label=M_HOST_TEXT, menu=filemenu)
root.config(menu=menubar)

#Конец
root.geometry(W_INIT_SIZE)
#инициализация
call_main_hard_init()
root.mainloop()
# ===========================================================
