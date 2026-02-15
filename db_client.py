"""Работа с базой данных"""
import psycopg2
from psycopg2 import Error
from configs.python_confiig import TOTAL_WIDTH
from configs.postgre_config import host, database, user, password, port
from colorama import init, Fore, Style
init(autoreset=True)


"""подключаемся к БД"""
def connect_db():
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()
        print(f"{Style.BRIGHT + Fore.CYAN + '[ INFO ]:' + Style.RESET_ALL} Успешное подключение к Postgre")

        return True, cursor, connection
    except Error as e:
        response = (f"{Style.BRIGHT + Fore.CYAN + '[ INFO ]:' + Style.RESET_ALL} Подключение к Postgre: {Style.BRIGHT + Fore.RED + '[ ERROR ]:' + Style.RESET_ALL} {e}")
        return False, response


"""создаем запись в БД"""
def create_game_record(cursor, connection, game_dict, game_count, max_appid):
    try:
        sql = """
            INSERT INTO steam_data (
                name, appid, required_age, is_free, about_the_game, 
                supported_languages, header_image, website, developers, 
                publishers, price, windows, mac, linux, metacritic, 
                genres_ids, screenshots, release_date, support_url, support_email
            ) VALUES (
                %(name)s, %(appid)s, %(required_age)s, %(is_free)s, %(about_the_game)s, 
                %(supported_languages)s, %(header_image)s, %(website)s, %(developers)s, 
                %(publishers)s, %(price)s, %(windows)s, %(mac)s, %(linux)s, %(metacritic)s, 
                %(genres_ids)s, %(screenshots)s, %(release_date)s, %(support_url)s, %(support_email)s
            );
        """

        cursor.execute(sql, game_dict)
        connection.commit()

        appid = game_dict.get('appid')


        left_part = f"[{Style.BRIGHT + 'ID:' + Style.RESET_ALL} {appid}] ({game_count} / {max_appid}) '{game_dict.get('name')}'"
        dots = '.' * (TOTAL_WIDTH - len(left_part) - len('[ OK ]'))

        if appid is None:
            dots = '.' * (TOTAL_WIDTH - len(left_part) - len('[ ERROR ]'))
            print(f"{left_part}{dots}{Fore.RED}[ ERROR ]")
            return False

        print(f"{left_part}{dots}{Fore.GREEN}[ OK ]")
        return True

    except Exception as e:
        connection.rollback()
        dots = '.' * (TOTAL_WIDTH - len(left_part) - len('[ ERROR ]'))
        print(f"{left_part}{dots}{Fore.RED}[ ERROR ]")
        return False


"""закрываем соединение с БД"""
def close_db(cursor, connection, ):
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print(f"{Style.BRIGHT + Fore.CYAN + '[ INFO ]:' + Style.RESET_ALL} Соединение с БД успешно закрыто")

    except Error as e:
        print(f"{Fore.BLUE + '[ INFO ]:' + Style.RESET_ALL} Ошибка при закрытии соединения: {Style.BRIGHT + Fore.RED + '[ ERROR ]:' + Style.RESET_ALL} {e}")
