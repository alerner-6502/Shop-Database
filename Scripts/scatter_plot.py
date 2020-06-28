#pylint: disable=R0915,E0611,E1101 #pylint не срассматривает содержание библиотеки Library
"""
Автор: Анатолий Лернер
Цель: Формурует и илюстрирует отчёт срассеиваньем
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

def clustered_scatter_plot(df_var, save=False):
    """
    Автор: Анатолий Лернер
    Цель: Формурует и илюстрирует отчёт срассеиваньем
    Вход: dataframe, флаг-нужно ли спасти
    Выход: Нет (новое окно и спасённый файл)
    """
    # находим один качественный столбец
    category = df_var.select_dtypes(include=np.object)
    column_name = category.columns[0]
    # набор уникальнтых элемнтов в нём
    category = set(list(category[column_name]))
    plot_dict = {}
    x_name = y_name = ""
    for z_var in category:
        # временный DataFrame содержащий все строки с данным качественным
        # атрибутом
        tmp = df_var.loc[df_var[column_name] == z_var]
        # выкидываем качественный столбец. После этого ровно два числовых
        # столбца должно остатся
        tmp = tmp.drop(column_name, axis=1)
        x_var = list(tmp.iloc[:, 0])
        y_var = list(tmp.iloc[:, 1])
        x_name = tmp.columns[0]
        y_name = tmp.columns[1]
        # формируем словарь состояший из уникальных качественных ключей и
        # списоки x-y точек
        plot_dict.update({z_var: [x_var, y_var]})
    x_name = TAG_DICT[x_name]
    y_name = TAG_DICT[y_name]

    # инициализируем генератор форматов точек
    lib.matplot_point_generator(True)
    # создаём точки
    for z_var in plot_dict:
        plt.plot(
            plot_dict[z_var][0],
            plot_dict[z_var][1],
            lib.matplot_point_generator(),
            label=z_var)

    plt.xlabel(
        x_name,
        labelpad=G_FONT_PAD,
        fontsize=G_FONT_SIZE,
        fontstyle=G_FONT_STYLE)
    plt.ylabel(
        y_name,
        labelpad=G_FONT_PAD,
        fontsize=G_FONT_SIZE,
        fontstyle=G_FONT_STYLE)
    plt.legend(
        framealpha=1,
        bbox_to_anchor=(
            G_XA_LABEL,
            G_YA_LABEL),
        loc=G_POS_LABEL)
    plt.grid(True, linestyle=G_GRID_LINE)
    plt.title(
        ANALYSIS_NAMES[5] +
        ": " +
        TAG_DICT[column_name],
        pad=G_TITLE_PAD,
        fontsize=G_TITLE_SIZE,
        fontstyle=G_FONT_STYLE)
    plt.tight_layout()
    if save:
        filename = ANALYSIS_NAMES[5] + " [" + \
            TAG_DICT[column_name] + "][" + x_name + "][" + y_name + "]"
        plt.savefig('./Graphics/' + filename + G_EXP_FORMAT)
    else:
        plt.show()

# ==============================================================
