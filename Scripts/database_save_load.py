#pylint: disable=W0702 #Отключаем "No exception type(s) specified (bare-except)".
#Для этой функции подробности как/почему совсем ненужны
"""
Автор: Анатолий Лернер
Цель: Функци для работы в pickle файлами
"""

import pickle as pic
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
TAB_TAGS = [TAG_LIST[0:2] + TAG_LIST[7:8] + TAG_LIST[10:12],
            TAG_LIST[1:7], TAG_LIST[7:10], TAG_LIST]

# =============== Функци для работы в файлами ====================

def call_load_source_database(path):
    """
    Автор: Анатолий Лернер
    Цель: Загружает содержимое pickle файла в DataFrame обьекты.
    Содержимое в файле уже привидено в 3NF
    Вход: использует глобальные DataFrame обьекты
    Выход: Список состоящий из флага (False=ошибка) и указателей на 4 новых DataFrames
    """

    try:
        f_var = open(path, "rb")
    except:
        return [False, 0, 0, 0, 0]
    with f_var:
        try:
            a_var = pic.load(f_var)
        except BaseException:
            return [False, 0, 0, 0, 0]
        try:
            b_var = pic.load(f_var)
        except BaseException:
            return [False, 0, 0, 0, 0]
        try:
            c_var = pic.load(f_var)
        except BaseException:
            return [False, 0, 0, 0, 0]

    if set(a_var.columns) != set(TAB_TAGS[0]) or \
       len(a_var.columns) != len(TAB_TAGS[0]) or \
       set(b_var.columns) != set(TAB_TAGS[1]):
        if len(b_var.columns) != len(TAB_TAGS[1]) or \
           set(c_var.columns) != set(TAB_TAGS[2]) or \
           len(c_var.columns) != len(TAB_TAGS[2]):
            return [False, 0, 0, 0, 0]

    table_core = a_var.copy(deep=True)
    table_comp = b_var.copy(deep=True)
    table_manf = c_var.copy(deep=True)
    table_all = pd.merge(table_core, table_comp, on="Comp")
    table_all = pd.merge(table_all, table_manf, on="Mfac")
    return [True, table_core, table_comp, table_manf, table_all]

def call_save_source_database(path, table_core, table_comp, table_manf):
    """
    Автор: Анатолий Лернер
    Цель: Сохраняет датафраме в формате Pickle
    Вход: Путь
    Выход: Нет
    """
    with open(path, "wb") as f_var:
        pic.dump(table_core, f_var)
        pic.dump(table_comp, f_var)
        pic.dump(table_manf, f_var)
    f_var.close()

def call_new_database():
    """
    Автор: Анатолий Лернер
    Цель: загружает пустые dataframe
    Вход: Глобальные переменные dataframe
    Выход: Список состоящий из указателей на 4 новых DataFrames
    """
    # устанавливает пустые DataFrame с правельными столбцами
    table_core = pd.DataFrame(columns=TAB_TAGS[0])
    table_comp = pd.DataFrame(columns=TAB_TAGS[1])
    table_manf = pd.DataFrame(columns=TAB_TAGS[2])
    table_all = pd.merge(table_core, table_comp, on="Comp")
    table_all = pd.merge(table_all, table_manf, on="Mfac")
    return [table_core, table_comp, table_manf, table_all]

# ==============================================================
