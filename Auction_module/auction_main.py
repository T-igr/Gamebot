import cv2

from handler.bd_wok import *
from handler.pattern_control import auction_navigation  # Поиск товаров в окне аукциона
from handler.find_visual_object import find_many  # Поиск координат монетки в окне аукциона
from handler.find_visual_object import find_language  # Определение языка и переключение
from handler.character_search import find_character  # Поиск и распознавание значений


# Старт программы
def main_auction_process():

    # Загрузка листа интересующих позиций для сканирования из базы данных pgSQL
    my_find_list = load_bd()

    # Проверка языка системы и при необходимости переключение на русский
    find_language('rus')


    for i in range(len(my_find_list)):
    # Поиск товаров в окне аукциона
        auction_navigation(my_find_list[i])

        # Определение золота:
        money_img = cv2.imread('sourse/slvr.png', cv2.IMREAD_COLOR)  # Загружаем картинку монетки
        slvr_x, slvr_y = find_many(money_img)  # Получаем координаты монетки

        # Заспознаем сиволы в графе Золото
        gold = find_character(slvr_x - 80, slvr_y - 6, 32, 'gold.png')

        # Заспознаем сиволы в графе серебро
        silver = find_character(slvr_x - 28, slvr_y - 6, 25, 'silver.png')

        # Заспознаем сиволы в графе серебро
        value = find_character(slvr_x + 140, slvr_y - 6, 53, 'value.png')

        price = round(int(gold[0]) + int(silver[0]) / 100.0, 2)
        value_item = int(value[0])
        print(f'Цена товара {price}')
        print(f'Объем товара {value_item}')
        print(f'Передаю имя работы с БД: {my_find_list[i]}')

        save_price(my_find_list[i], price, value_item)  # Передаем имя для сохранения цены

    # Проверка языка системы и при необходимости переключение на русский
    find_language('eng')




if __name__ == '__main__':
    main_auction_process()
else:
    pass