"""Работа с базой данных"""
import psycopg2
import json
from psycopg2 import Error
from configs.postgre_config import host, database, user, password, port

connection = None
cursor = None


def connect_db():
    global connection, cursor
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()
        print("Подключение к БД установлено")
        return True
    except Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return False


def create_game_record(game_dict):
    global connection, cursor

    if connection is None or cursor is None:
        print("Сначала вызови connect_db()")
        return False

    try:
        appid_value = game_dict.get('appid') or game_dict.get('steam_appid')

        if appid_value is None:
            print(f"ВНИМАНИЕ: В переданном словаре нет ключа 'appid' или 'steam_appid'.")
            print(f"Доступные ключи: {list(game_dict.keys())}")
            print(f"Пропускаем игру: {game_dict.get('name', 'Без названия')}")
            return False

        insert_query = """
        INSERT INTO steam_games_raw_data (
            name, appid, min_age, is_free, description,
            supported_languages, header_image, capsule_image, website,
            pc_requirements, mac_requirements, linux_requirements,
            developers, publishers, price, platforms, metacritic,
            categories, genres, screenshots, movies, release_date
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s::jsonb, %s::jsonb, %s::jsonb,
            %s, %s, %s::jsonb, %s::jsonb, %s::jsonb,
            %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb
        )
        ON CONFLICT (appid) DO UPDATE SET
            name = EXCLUDED.name,
            price = EXCLUDED.price,
            updated_at = CURRENT_TIMESTAMP
        """

        values = (
            game_dict.get('name'),
            appid_value,  # Используем извлечённое значение
            game_dict.get('min_age', 0),
            game_dict.get('is_free', False),
            game_dict.get('description', ''),
            game_dict.get('supported_languages', ''),
            game_dict.get('header_image', ''),
            game_dict.get('capsule_image', ''),
            game_dict.get('website', ''),
            json.dumps(game_dict.get('pc_requirements', {})),
            json.dumps(game_dict.get('mac_requirements', {})),
            json.dumps(game_dict.get('linux_requirements', {})),
            game_dict.get('developers', []),
            game_dict.get('publishers', []),
            json.dumps(game_dict.get('price', {})),
            json.dumps(game_dict.get('platforms', {})),
            json.dumps(game_dict.get('metacritic', {})),
            json.dumps(game_dict.get('categories', [])),
            json.dumps(game_dict.get('genres', [])),
            json.dumps(game_dict.get('screenshots', [])),
            json.dumps(game_dict.get('movies', [])),
            json.dumps(game_dict.get('release_date', {}))
        )

        cursor.execute(insert_query, values)
        connection.commit()
        print(f"Игра '{game_dict.get('name')}' (AppID: {appid_value}) сохранена.")
        return True

    except Error as e:
        print(f"Ошибка при сохранении игры '{game_dict.get('name')}': {e}")
        connection.rollback()
        return False


def close_db():
    global connection, cursor
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Соединение с БД закрыто")
        connection = None
        cursor = None
    except Error as e:
        print(f"Ошибка при закрытии соединения: {e}")