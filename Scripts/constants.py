"""
Цель: Коллекция констант для главного скрипта
Автор: Анатолий Лернер
"""
# параметры для работы с файлами
DATABASE_FORMAT = ".pickle"
DATABASE_FORMAT_INTRO = "pickle files"
DEFAULT_DATABASE = "database"
DEFAULT_NEW_DATABASE = "new"
INIT_EXPORT_NAME = "table"
EXPORTBOX_TITLE = "Экспорт"
OPEN_TITLE = "Открыть"
SAVEAS_TITLE = "Сохранить как"
EXP_FORMAT_INTRO = "excel files"
EXP_FORMAT = ".xlsx"

# параметры для графических отчётов
G_FONT_PAD = 15
G_FONT_SIZE = 11
G_FONT_STYLE = "italic"
G_POS_LABEL = "center left"
G_XA_LABEL = 1.04
G_YA_LABEL = 0.5
G_GRID_LINE = "--"
G_GRID_AXIS = "y"
G_EXP_FORMAT = ".png"
G_TITLE_PAD = 20
G_TITLE_SIZE = 13
G_ROT_LABEL = 40
G_ALI_LABEL = "right"
G_BOX_COL = "white"
G_HIST_YLABEL = "Частота"
G_HIST_POTS = 5
G_COLTAB_DROP = 0.05
G_COLTAB_YLABEL = "Количество"

# параметры для текстовых отчётов
X_STATISTICS = "- Свойства -"
X_STATLIST = [
    "Количество элементов :",
    "Уникальные элемнты :",
    "Самый частый элемент :",
    "Количество повторений :",
    "Среднее значение :",
    "Среднеквадратическое :",
    "Минимум :",
    "25 процентов :",
    "50 процентов :",
    "75 процентов :",
    "Максимум :",
]
X_AGGREGATION = [
    "Сумма",
    "Среднее",
    "Минимум",
    "Максимум"]
X_AGG_WIN_NAME = "Настройка"
X_AGG_GRP_NAME = "Параметры таблицы"
X_AGG_LABEL = "Метод агрегации"
X_AGG_BUTTON = "Получить таблицу"

# параметры для widgets на главном окне
W_LIST_COL = "#DDDDDD"
W_WINDOW_TITLE = "База Данных : "
W_TREE_ROWCOLOR = "#AAFFFF"
W_GB_TABLE_TEXT = "Таблица"
W_GB_ANLYSIS_TEXT = "Анализ"
W_GB_FILTER_TEXT = "Фильтры"
W_LAB1 = "Выбор"
W_LAB2 = "Метод Анализа"
W_LAB3 = "Параметры"
W_LAB4 = "Значения"
W_LAB5 = "Столбцы"
W_LB_ACTIVE_COL = "#FFBBFF"
W_BT_ADD_TEXT = "Добавить"
W_BT_EDIT_TEXT = "Правка"
W_BT_DELETE_TEXT = "Удалить"
W_BT_EXPORT_TEXT = "Экспорт"
W_BT_ANALYSIS_TEXT = "Анализ"
W_BT_EXPORTA_TEXT = "Экспорт"
W_BT_FILTER_TEXT = "Отфильтровать"
W_BT_EDITF_TEXT = "Изменить значения"
W_BT_DROPF_TEXT = "Сбросить выбор"
W_INIT_SIZE = "970x570"

# параметры для меню
M_NEW_TEXT = "Новая"
M_OPEN_TEXT = "Открыть"
M_SAVE_TEXT = "Сохранить"
M_SAVEAS_TEXT = "Сохранить как"
M_HOST_TEXT = "База Данных"

# параметры для widgets на корректировочном окне
E_GB_NAME = "Параметры"
E_CB_TEXT = "Очистить значения"
E_OKB_TEXT = "Подтвердить"

# пояснения
X_TOTAL_ITEMS = "Количество элементов: {0:8d}" #Т_TOTAL_ITEMS
X_ADD_ELEMENT = "Добавить элемент"
X_SELEC_ITEMS = "Выбрано: {0:34d}"
X_EDIT_ELEMENT = "Редактировать элемeнт"
X_EDIT_FILTER = "Параметры фильтра"
X_MESSAGEBOX = "Предупреждение"
X_ERRORBOX = "Ошибка"
X_WARNINGBOX = "Предупреждение"
X_INFOBOX = "Сообщение"
X_MAINFRAME = "База данных: -"

# сообщения
MSG_OPENFAIL = "Файл не удалось открыть.\n"
MSG_SAVEOK = "Файл сохранён успешно.\nКаталог: "
MSG_CHANGED_COMP_KEY = "Изменённое имя компонента отразится на всех продуктах что его используют."
MSG_CHANGED_MFAC_KEY = ("Изменённое имя производителя отразится на всех продуктах что "
                        "его используют.")
MSG_DELETE_KEY = (
    "При выполнении этой операции все продукты что используют этот компонент будут удалены."
    " Продолжить?")
MSG_PLUS_ERROR_P1 = "В атрибуте "
MSG_PLUS_ERROR_P2 = " разделители используются неверно."
MSG_INT_ERROR = " содержит не целые числа."
MSG_FLOAT_ERROR = " содержит строки."
MSG_EDIT_INT_ERROR = " должен содержать целые числа.\nВведите пожалуйста другое значение."
MSG_EDIT_FLOAT_ERROR = " должен содержать числа.\nВведите пожалуйста другое значение."
MSG_EDIT_UNIQUE_ERROR = " с подобным именем уже существует.\nВведите пожалуйста другое значение."
MSG_EDIT_SIMILAR_ERROR = " с подобным именем не существует.\nНеобходимо его сначала добавить к " +\
"соответствующей таблице."

# систематичные константы
TAG_NAME_LIST = [
    "Продукт",
    "Компонент",
    "Тип",
    "Источник Питания (V)",
    "Кол-во Бит",
    "Кол-во Каналов",
    "Упаковка",
    "Производитель",
    "Страна",
    "Рейтинг (5)",
    "Цена (USD)",
    "Кол-во",
]
ANALYSIS_NAMES = [
    "Базовая Статистика",
    "Сводная Таблица",
    "Столбчатая Диаграмма",
    "Гистограмма",
    "Диаграмма Бокса-Вискера",
    "Диаграмма Рассеивания",
]
TAB_NAMES = ["Товары", "Компоненты", "Производители", "Полный список"]
TAG_ALIGNMENT = ["w", "w", "w", "e", "e", "e", "w", "w", "w", "e", "e", "e"]
