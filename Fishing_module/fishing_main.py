import cv2
import pyautogui
import time
import numpy as np

from handler.Listener_keyboard import wait_for_key  # Ожидание нажатия клавиши
from handler.find_visual_object import find_object  # Поиск объекта на экране
from handler.find_visual_object import find_language # Проверка языка и его переключение


def module_fishing_process(program_name) -> str:  # доработать Запуск как модуль
    print(f'Запуск как модуль через {program_name}')
    pass


def main_fishing_process() -> None:  # Запуск как самостоятельное приложение

    fish_x, fish_y, bug_x, bug_y = fishing_preparation()  # Получаем первичные координаты рабочей области

    float_name = 'float.png'  # Задаем название скрина поплавка

    wait_for_key('наведите мышку на поплавок и нажмите -> анг.',
                 'p')
    floal_img = flot_screen(float_name)  # Получаем numpy.ndarray объекта изображения попалвка

    start_fishing(fish_x, fish_y, bug_x, bug_y, floal_img) # Запускаем рыбалку и передаем вводные данные



# Сбор первичных данных перед началом процесса рыбалки
def fishing_preparation() -> [float, float, float, float]:
    """
    Ищет на экране иконку рыбалки и сумки, фиксирует и возвращяет их координаты.
    """
    find_language('eng')

    wait_for_key('Откройте окно игры и нажмите -> анг.',
                 'p')
    print('Определяю рабочую область...')

    fish_img = cv2.imread('sourse/fishing.png', cv2.IMREAD_COLOR)  # Загружаем иконку
    # Делаем скин всего экрана
    fish_x, fish_y, fish_val = find_object(fish_img, 1, None, 'base_screen.png')

    # Если иконка рыбалки не найдена, то ищем кнопку переключения набора иконок на панели
    if fish_val < 0.55:
        panel_img = cv2.imread('sourse/panel_button.png', cv2.IMREAD_COLOR)
        panel_x, panel_y, panel_val = find_object(panel_img, 1)

        pyautogui.moveTo(panel_x, panel_y, 0.5, pyautogui.easeInOutQuad)
        pyautogui.click()

        # Повторный поиск иконки рыбалки
        fish_x, fish_y, fish_val = find_object(fish_img, 1, None, 'base_screen.png')

        if fish_val < 0.55:
            print('Иконока рыбалки не найдена, бот завершает работу')
            exit()

    bug_img = cv2.imread('sourse/bugs.png', cv2.IMREAD_COLOR)
    bug_x, bug_y, bug_val = find_object(bug_img, 1)

    # Визуальная проверка точности координат через перемещение мышкой
    pyautogui.moveTo(bug_x, bug_y, 0.5, pyautogui.easeInOutQuad)
    time.sleep(0.5)
    pyautogui.moveTo(fish_x, fish_y, 0.5, pyautogui.easeInOutQuad)
    pyautogui.click()

    print(f'Иконка рыбалки: x= {fish_x} y= {fish_y} val= {fish_val}')
    print(f'Иконка сумки: x= {bug_x} y= {bug_y} val= {bug_val}')
    print('рабочая область определена')

    return fish_x, fish_y, bug_x, bug_y


def flot_screen(float_name: str) -> np.ndarray:
    # Считывание текущих координат мыши
    mouse_x, mouse_y = pyautogui.position()
    print(f'Мыш на координатах х= {mouse_x}  y= {mouse_y}')

    # Создание скриншота
    screen_float = pyautogui.screenshot(region=(mouse_x, mouse_y, 33, 33))
    screen_float.save(f'sourse/{float_name}')
    print('Поплавок обновлен!')

    float_img = cv2.imread(f'sourse/{float_name}', cv2.IMREAD_COLOR)

    return float_img



def start_fishing(fish_x:float, fish_y:float, bug_x:float, bug_y:float, floal_img:np.ndarray) -> None:

    start_time = time.time()  # Фиксируем время начала
    online_time = 120  #Задаем время онлайн сессии, в минутах
    end_time = 0  # Инициализация переменной для отслеживания времени работы программы
    player_active = 0  # Инициализация переменной для сброса простоя персонажа в игре

    while end_time < online_time:

        if player_active == 0:
            pyautogui.press('down')  # Нажатие клавиши "down"

        if player_active < 20:  # Если количество прыжков меньше 20
            player_active += 1  # Увеличение количества прыжков на 1
        else:
            player_active = 0  # Сброс счетчика активности игрока
            pyautogui.press('up')
            pyautogui.press('5')
            time.sleep(1)


        # Закидываем удочку
        pyautogui.moveTo(fish_x, fish_y, 1.2, pyautogui.easeInOutQuad)  # Перемещение курсора мыши
        pyautogui.click()
        time.sleep(3.3)

        # Задаем рабочую область скриншота
        left = int(0)
        top = int(0)
        width = int(bug_x - 200)
        height = int(bug_y - 220)

        # Ищем, где появился поплавок в пределах рабочей области
        float_x, float_y, float_val = find_object(floal_img, None, (left, top,  width, height,))
        print(f'Поплавок найден по x={float_x}, y={float_y}')
        print(f'Значение совпадения = {float_val}')

        # Создание скриншота актуального поплавка
        float_screen = pyautogui.screenshot(region=(float_x, float_y, 33, 33))
        float_screen_np = np.array(float_screen)
        float_screen_np = cv2.cvtColor(float_screen_np, cv2.COLOR_RGB2BGR)

        pyautogui.moveTo(float_x, float_y, 0.6, pyautogui.easeInOutQuad)  # Перемещение курсора к поплавку

        warning = 0  # Задаем счетчик ошибок распознавания

        while True:
            warning += 1
            # Ловим момент, когда поплавок окунется в воду (клюнет рыба)
            _float_zone_x, _float_zone_y, float_zone_val = find_object(float_screen_np,
                                                                       None,
                                                                       (float_x - 20, float_y - 20, 80, 80),
                                                                       None,
                                                                       '1'
                                                                        )

            print(f'Проверка состояния поплавка: {float_zone_val}')

            if warning > 230:
                print('Критическое количество ошибок')
                break  # Делаем повторное забрасывание удочки

            if float_zone_val < 0.65: # Условие окунание поплавка в воду
                print(f'клюнуло на {float_zone_val}')

                pyautogui.moveTo(float_x + 16, float_y + 20, 0.4)
                pyautogui.mouseDown(button='right')  # Нажатие левой кнопки мыши
                time.sleep(0.2)  # Пауза на 0.2 секунды
                pyautogui.mouseUp(button='right')  # Отпускание левой кнопки мыши

                break  # Делаем повторное забрасывание удочки

        end_time = round((time.time() - start_time) / 60, 1)
        print(f'Время работы программы: {end_time} мин')




if __name__ == '__main__':
    main_fishing_process()
else:
    pass
