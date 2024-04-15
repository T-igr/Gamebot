import pyautogui
import keyboard
import time

def switch_language():
    # Нажать клавиши
    keyboard.press('alt')
    keyboard.press('shift')
    time.sleep(0.5)
    keyboard.release('alt')
    keyboard.release('shift')

    print('Смена языка выполнена')

# Управляет мышью на панели окно аукциона, берет из списка названия и открывает панель с ценами
def auction_navigation(item_name:list) -> None:

    # очистка поля поиска
    pyautogui.moveTo(580, 208, duration=1, tween=pyautogui.easeInQuad)
    # Клик левой кнопкой мыши
    pyautogui.click()
    time.sleep(0.5)

    # Поиск товара
    pyautogui.moveTo(400, 210, duration=1, tween=pyautogui.easeInQuad)
    # Клик левой кнопкой мыши
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.click()

    print(f"Элемент {item_name} в работе")


    # Побуквенный ввод названия предмета в после поиска
    for char in item_name:
        keyboard.write(char)
        time.sleep(0.5)  # Пауза между нажатиями клавиш

    time.sleep(0.5)

    # Нажимаем поиск выбранного товара
    pyautogui.moveTo(900, 210, duration=1, tween=pyautogui.easeInQuad)
    # Клик левой кнопкой мыши
    pyautogui.click()
    time.sleep(0.5)

    # Нажимаем выбираем строку с товаром
    pyautogui.moveTo(500, 280, duration=1, tween=pyautogui.easeInQuad)
    # Клик левой кнопкой мыши
    pyautogui.click()
    time.sleep(0.5)