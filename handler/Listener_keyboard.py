from pynput import keyboard

def on_press(key, target_key):
    if key == keyboard.Key.esc:
        # Если нажата клавиша Esc, завершить программу
        return False
    elif key == target_key:
        # Если нажата указанная клавиша, продолжить выполнение программы
        return False

def wait_for_key( text, target_key):
    print(f"{text} {target_key}")

    # Преобразуем строку в код клавиши
    target_key = keyboard.KeyCode.from_char(target_key)

    # Настройка слушателя клавиатуры
    with keyboard.Listener(on_press=lambda key: on_press(key, target_key)) as listener:
        listener.join()


if __name__ == '__main__':
    print('Это модуль')
else:
    pass
