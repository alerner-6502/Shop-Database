"""
Автор: Анатолий Лернер
Цель: Проверяет если можно построить заданный отчёт для заданной dataframe
"""
import numpy as np
#import pandas as pd #pylint: disable=W0611 #Pandas здесь на самом деле используется!

from constants import * #pylint: disable=W0401,W0614 # Отключить ошибку: не все константы используются
#разрешить подобное движение для архива с констнтами

# =============== Функции Графического Анализа ==============

def check_data_frame(data_frame, frame_type=""):
    """
    Автор: Виталий Павленко
    Цель: Функция проверяет data_frame на возможность построить frame_type анализ
    Вход: DataFrame обьект
    Выход: Если возможно возвращает True, иначе - False
    """

    if frame_type == ANALYSIS_NAMES[0]:  # "Базовая Статистика":
        return True

    # разбиваем известные виды анализа на типы
    table_type1 = ANALYSIS_NAMES[2:3]  # ["Столбчатая Диаграмма"]
    # ["Гистограмма", "Диаграмма Бокса-Вискера"]
    table_type2 = ANALYSIS_NAMES[3:5]
    table_type3 = ANALYSIS_NAMES[5:6]  # ["Диаграмма Рассеивания"]
    table_type4 = ANALYSIS_NAMES[1:2]  # ["Сводная Таблица"]

    # список типив столбцов
    column_types = [data_frame[x].dtype for x in data_frame.columns]

    # два качественных столбца
    if frame_type in table_type1:
        if len(data_frame.columns) == 2 and column_types.count(np.object) == 2:
            return True
    # один качественный столбец и один численый столбец
    if frame_type in table_type2:
        if len(data_frame.columns) == 2 and column_types.count(np.object) == 1:
            return True
    # один качественный столбец и два численых столбца
    if frame_type in table_type3:
        if len(data_frame.columns) == 3 and column_types.count(np.object) == 1:
            return True
    if frame_type in table_type4:
        if len(data_frame.columns) == 3 and column_types.count(np.object) == 2:
            return True

    return False

#==========================================================
