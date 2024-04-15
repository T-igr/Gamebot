import psycopg2

from datetime import datetime
from handler.config_bd import *


# Загрузка листа интересующих позиций для сканирования из базы данных pgSQL
def load_bd() -> list:
    try:
        # Установка соединения с базой данных PostgreSQL
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

        # Создание курсора для выполнения SQL-запросов
        cursor = connection.cursor()

        # SQL-запрос для получения всех имен из таблицы
        select_query = "SELECT name FROM names"

        # Выполнение SQL-запроса
        cursor.execute(select_query)

        # Получение результатов выполнения запроса
        names = cursor.fetchall()

        # Вывод результатов
        print("Содержимое таблицы names:")
        for name in names:
            print(name[
                      0])  # name[0] потому что fetchall() возвращает список кортежей, где первый элемент кортежа - это значение поля 'name'

        return names  # Возвращаем все имена

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL:", error)

    finally:
        # Закрытие соединения с базой данных
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")




def save_price(name, price, value):
    try:
        # Установка соединения с базой данных PostgreSQL
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

        # Создание курсора для выполнения SQL-запросов
        cursor = connection.cursor()

        # Имя для добавления данных
        name_to_insert = name  # Используем переданное имя

        # Получение id имени из таблицы names
        select_id_query = "SELECT id FROM names WHERE name = %s"
        cursor.execute(select_id_query, (name_to_insert,))
        name_id = cursor.fetchone()[0]

        # Текущая дата и время
        today = datetime.today().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Данные для вставки в таблицу indicators
        insert_data_query = """
        INSERT INTO indicators (name_id, date, time, price, volume)
        VALUES (%s, %s, %s, %s, %s)
        """
        data_to_insert = (name_id, today, timestamp, price, value)  # Примерные данные для цены и объема

        # Выполнение SQL-запроса для вставки данных
        cursor.execute(insert_data_query, data_to_insert)

        # Подтверждение изменений в базе данных
        connection.commit()

        print(f"Данные успешно добавлены в таблицу indicators для имени '{name_to_insert}'")

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL:", error)

    finally:
        # Закрытие соединения с базой данных
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")