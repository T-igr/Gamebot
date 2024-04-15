import cv2
import pyautogui
import numpy as np
from handler.pattern_control import switch_language

def find_object(object, Centre=None, region=None, save_file=None, gaus=None) -> [float, float, float]:
    """
    Функция для поиска объекта на скриншоте и возврата его координат и коэффициента совпадения.

    Args:
        object (numpy.ndarray): объект изображения numpy, который нужно найти на скриншоте.
        region (tuple, optional): Область скриншота, в которой будет произведен поиск. По умолчанию None.
        save_file (str, optional): Путь для сохранения скриншота. По умолчанию None.
        gaus (str, optional): Включение функции обраотки изображений по гаусу. По умолчанию None.

    Returns:
        tuple: Кортеж с координатами объекта на скриншоте (x, y) и коэффициентом совпадения.
    """

    # Создаем скриншот
    if region is None:
        screen = pyautogui.screenshot()
    else:
        screen = pyautogui.screenshot(region=region)

    # Создаем скриншот
    if save_file is None:
        pass
    else:
        screen.save(f'temp/{save_file}')

    # Преобразование изображений под необходимый формат
    screen_np = np.array(screen)
    screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

    if gaus is None:
        object_img = object
    else:  # Метод размытия по гаусу
        object_img = cv2.GaussianBlur(object, (5, 5), 0)
        screen_bgr = cv2.GaussianBlur(screen_bgr, (5, 5), 0)


    # Поиск шаблона объекта на скриншоте
    result = cv2.matchTemplate(screen_bgr, object_img, cv2.TM_CCOEFF_NORMED)
    result_min_val, result_max_val, result_min_loc, result_max_loc = cv2.minMaxLoc(result)

    result_x, result_y = result_max_loc[0], result_max_loc[1]  # Получение координат левого верхнего угла совпадения

    # Вычисление координат центра объекта
    if Centre is not None:
        result_x = result_x + object_img.shape[1] / 2
        result_y = result_y + object_img.shape[0] / 2


    return result_x, result_y, result_max_val


# Проверка языка системы и при небходимости переключение на заданный
def find_language(language: str) -> None:

    lang_img = cv2.imread('sourse/eng.png', cv2.IMREAD_COLOR)  # Загружаем иконку зыка

    # Делаем скин всего экрана и ищем какой язык включен в системе
    _lang_x, _lang_y, lang_val = find_object(lang_img)


    # Если иконка языка найдена, то значит в системе английский язык
    if lang_val < 0.6:
        lang_status = 'rus'
        print('Русский язык')
    else:
        lang_status = 'eng'
        print('Английский язык')

    if language != lang_status:
        switch_language()



# Поиск координат с ценой
def find_many(money_img: np.ndarray) -> [float, float]:
# money_img (numpy.ndarray): объект изображения numpy, который нужно найти на скриншоте.
# возвращаем координаты найденого объекта

    # Координаты начала поля с ценами в окне аукциона
    x_auc_windows = 725
    y_auc_windows = 285

    # Делаем скин всего экрана
    money_x, money_y, money_val = find_object(money_img,
                                              None,
                                              (x_auc_windows, y_auc_windows, 105, 23), 'money_zona.png')
    # Получаем координаты серебряной монетки
    money_x = money_x + x_auc_windows
    money_y = money_y + y_auc_windows

    print(f'монета найдена по x={money_x}, y={money_y}')
    print(f'Значение совпадения = {money_val}')
    pyautogui.moveTo(money_x, money_y, 1)

    if money_val < 0.6:
        print('Цифра не найдена, проверь аук!')

    return money_x, money_y

