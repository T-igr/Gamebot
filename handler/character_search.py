import cv2
import pytesseract
import pyautogui

# Делаем скриншот заданной области и передаем на обработку и распознование содержащихся символов
def find_character(x_box, y_box, width_box, box_name):

    # Задаем координаты и размеры области скриншота
    left = x_box
    top = y_box
    width = width_box
    height = 24

    # Используем библиотеку PIL т.к. дает лучшее качество изображения
    box_screen = pyautogui.screenshot(region=(left, top, width, height))

    # Отображаем скриншот
    #box_screen.show()

    box_screen.save(f"temp/{box_name}")

    box_character = image_dev(f'temp/{box_name}')


    return box_character



#Функция распознования части цены у монетки
def image_dev(image_in:str) -> int:
    # Загрузка изображения
    image = cv2.imread(image_in)

    # Увеличение размера изображения
    scaled_image = increase_image_size(image, 400)

    # Предварительная обработка изображения
    gray = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Нахождение контуров
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Извлечение и распознавание цифр
    recognized_digits = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        digit_region = thresh[y:y + h, x:x + w]
        digit_text = pytesseract.image_to_string(digit_region,
                                                 config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        recognized_digits.append(digit_text.strip())

    # Фильтрация результатов
    recognized_digits = [digit for digit in recognized_digits if digit.isdigit()]

    digits = recognized_digits[0]
    if digits == '':
        digits = 0

    # Вывод распознанных цифр
    return digits





def increase_image_size(image:object, scale_percent:int) -> object:
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    new_size = (width, height)
    return cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)


