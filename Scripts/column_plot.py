"""
Автор: Анатолий Лернер
Цель: Формурует и илюстрирует отчёт столбчатая таблица
"""

import numpy as np
import matplotlib.pyplot as plt

from constants import * #pylint: disable=W0401,W0614 # Отключить ошибку: не все константы используются
#разрешить подобное движение для архива с констнтами

# =============== Локальные переменные ======================

#Перенести эти по факту константы в скрипт "constants.py" нельзя.
#Поскольку Tags короые здесь изпользуются критичны для работы программы.
TAG_LIST = [
    "Prod", "Comp", "Type", "Volt", "Bits", "Inps", "Moun", \
    "Mfac", "Coun", "Rati", "Cost", "Avai", "Prop"]
TAG_DICT = dict(zip(TAG_LIST, TAG_NAME_LIST))

# =============== Функции Графического Анализа ==============

def clustered_column_table(df_var, save=False):
    """
    Автор: Анатолий Лернер
    Цель: Формурует и илюстрирует отчёт столбчатая таблица
    Вход: dataframe, флаг: нужно ли спасти
    Выход: Нет (новое окно и спасённый файл)
    """
    # берём первый качественный столбец (ключи)
    category = df_var.iloc[:, 0]
    cat_name = df_var.columns[0]
    # набор уникальнтых элемнтов в нём
    category = set(list(category))

    players = df_var.iloc[:, 1]
    ply_name = df_var.columns[1]
    # берём второй качественный столбец и находим уникальных соревнователий
    players = set(list(players))

    data_dict = {}
    for x_var in players:
        scores = []
        # временный DataFrame содержащий все строки с данным элемнтом
        # категории
        tmp = df_var.loc[df_var[ply_name] == x_var]
        # выкидываем качественный столбец. После этого ровно один качественный
        # столбец должен остатся
        tmp = tmp.drop(ply_name, axis=1)
        tmp = list(tmp.iloc[:, 0])
        for y_var in category:
            # записываем сколько раз каждая категория появлялось у игрока
            scores.append(tmp.count(y_var) + G_COLTAB_DROP)
        # добавляем категорию + очки для каждого игрока в обший словарь
        data_dict.update({x_var: scores})

    # создаём место для обработки
    tmp = plt.subplots()[1]

    # местонахождение категорий
    ind = np.arange(len(category))
    # автоматическое расстояние между категориями
    sep = 3 / ((len(players) + 2) * len(category))
    # добовляем элемны
    el_list = []
    for x_var, y_var in zip(data_dict.keys(), np.arange(0, 2, sep)):
        b_var = tmp.bar(
            ind + y_var, data_dict[x_var], width=sep, bottom=-G_COLTAB_DROP, zorder=3)
        el_list.append(b_var)

    # обозначаем категории
    tmp.set_xticks(ind + (sep * len(players) / 2))
    tmp.set_xticklabels(category, rotation=G_ROT_LABEL, ha=G_ALI_LABEL)
    # формируем легенду
    tmp.legend(el_list, players, bbox_to_anchor=(G_XA_LABEL, G_YA_LABEL), loc=G_POS_LABEL)

    plt.xlabel(
        TAG_DICT[cat_name], labelpad=G_FONT_PAD, fontsize=G_FONT_SIZE, fontstyle=G_FONT_STYLE)
    plt.ylabel(
        G_COLTAB_YLABEL, labelpad=G_FONT_PAD, fontsize=G_FONT_SIZE, fontstyle=G_FONT_STYLE)

    plt.title(
        ANALYSIS_NAMES[2] + ": " + TAG_DICT[cat_name], pad=G_TITLE_PAD, \
        fontsize=G_TITLE_SIZE, fontstyle=G_FONT_STYLE)
    plt.grid(True, linestyle=G_GRID_LINE, axis=G_GRID_AXIS, zorder=0)
    plt.tight_layout()

    if save:
        tmp = ANALYSIS_NAMES[2] + " [" + \
        TAG_DICT[cat_name] + "][" + TAG_DICT[ply_name] + "]"
        plt.savefig('./Graphics/' + tmp + G_EXP_FORMAT)
    else:
        plt.show()

# ==============================================================
