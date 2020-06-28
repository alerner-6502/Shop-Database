#pylint: disable=E1101 #pylint не срассматривает содержание библиотеки Library
"""
Автор: Анатолий Лернер
Цель: Формурует и илюстрирует отчёт гистограмма
"""
import numpy as np
import matplotlib.pyplot as plt

import Library as lib
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

def clustered_hitogram(df_var, save=False):
    """
    Автор: Анатолий Лернер
    Цель: Формурует и илюстрирует отчёт гистограмма
    Вход: dataframe, флаг: нужно ли спасти
    Выход: Нет (новое окно и спасённый файл)
    """
    # находим один качественный столбец
    category = df_var.select_dtypes(include=np.object)
    column_name = category.columns[0]
    # набор уникальнтых элемнтов в нём
    category = set(list(category[column_name]))
    data_list = []
    x_name = ""
    for z_var in category:
        # временный DataFrame содержащий все строки с данным качественным
        # атрибутом
        tmp = df_var.loc[df_var[column_name] == z_var]
        # выкидываем качественный столбец. После этого ровно один числовой
        # столбец должен остатся
        tmp = tmp.drop(column_name, axis=1)
        # формируем списки с информацией
        x_name = tmp.columns[0]
        data_list.append(list(tmp.iloc[:, 0]))
    # print(data_list)

    # гинерируем список уникальных цветов
    colors = lib.get_color_list(len(category))
    # устанавлуваем график
    plt.hist(
        data_list,
        G_HIST_POTS,
        density=1,
        histtype='bar',
        color=colors,
        label=list(category),
        zorder=3)
    plt.xlabel(
        TAG_DICT[x_name],
        labelpad=G_FONT_PAD,
        fontsize=G_FONT_SIZE,
        fontstyle=G_FONT_STYLE)
    plt.ylabel(
        G_HIST_YLABEL,
        labelpad=G_FONT_PAD,
        fontsize=G_FONT_SIZE,
        fontstyle=G_FONT_STYLE)
    plt.legend(
        framealpha=1,
        bbox_to_anchor=(
            G_XA_LABEL,
            G_YA_LABEL),
        loc=G_POS_LABEL)
    plt.grid(True, linestyle=G_GRID_LINE, axis=G_GRID_AXIS, zorder=0)
    plt.title(
        ANALYSIS_NAMES[3] +
        ": " +
        TAG_DICT[column_name],
        pad=G_TITLE_PAD,
        fontsize=G_TITLE_SIZE,
        fontstyle=G_FONT_STYLE)
    plt.tight_layout()

    if save:
        filename = ANALYSIS_NAMES[3] + " [" + \
            TAG_DICT[column_name] + "][" + TAG_DICT[x_name] + "]"
        plt.savefig('./Graphics/' + filename + G_EXP_FORMAT)
    else:
        plt.show()

# ==============================================================
