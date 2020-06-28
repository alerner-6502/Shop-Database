"""
Автор: Анатолий Лернер
Цель: Формурует и илюстрирует отчёт с коробками
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

def box_whisker_plot(df_var, save=False):
    """
    Автор: Анатолий Лернер
    Цель: Формурует и илюстрирует отчёт с коробками
    Вход: dataframe, флаг: нужно ли спасти
    Выход: Нет (новое окно и спасённый файл)
    """
    # находим один качественный столбец
    category = df_var.select_dtypes(include=np.object)
    column_name = category.columns[0]
    # набор уникальнтых элемнтов в нём
    category = set(list(category[column_name]))
    data_list = []
    title_list = []
    y_name = ""
    for z_var in category:
        # временный DataFrame содержащий все строки с данным качественным
        # атрибутом
        tmp = df_var.loc[df_var[column_name] == z_var]
        # выкидываем качественный столбец. После этого ровно один числовой
        # столбец должен остатся
        tmp = tmp.drop(column_name, axis=1)
        # формируем списки синформацией и загаловками
        y_name = tmp.columns[0]
        data_list.append(list(tmp.iloc[:, 0]))
        title_list.append(z_var)

    # создаём фигуру
    fig = plt.figure()
    axe = fig.add_subplot(1, 1, 1)
    my_box = axe.boxplot(data_list, patch_artist=True)

    # устанавливаем ореинтацию Labels
    axe.set_xticklabels(title_list, rotation=G_ROT_LABEL, ha=G_ALI_LABEL)

    plt.xlabel(TAG_DICT[column_name], labelpad=G_FONT_PAD,
               fontsize=G_FONT_SIZE, fontstyle=G_FONT_STYLE)
    plt.ylabel(TAG_DICT[y_name], labelpad=G_FONT_PAD,
               fontsize=G_FONT_SIZE, fontstyle=G_FONT_STYLE)
    plt.title(
        ANALYSIS_NAMES[4] +
        ": " +
        TAG_DICT[column_name],
        pad=G_TITLE_PAD,
        fontsize=G_TITLE_SIZE,
        fontstyle=G_FONT_STYLE)
    plt.grid(True, linestyle=G_GRID_LINE, axis=G_GRID_AXIS)
    plt.tight_layout()

    # меняем внутренний цвет коробок
    for x_var in my_box['boxes']:
        x_var.set(facecolor=G_BOX_COL)

    if save:
        filename = ANALYSIS_NAMES[4] + " [" + \
            TAG_DICT[column_name] + "][" + TAG_DICT[y_name] + "]"
        plt.savefig('./Graphics/' + filename + G_EXP_FORMAT)
    else:
        plt.show()

# ==============================================================
