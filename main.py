"""ОСНОВНОЙ ФАЙЛ"""
import sys
import atexit
import time
import file_reader
import api_client
import data_unpacker
import db_client
import create_statistics
from configs.python_confiig import WORKING_APPIDS_REFERENCE, WORKING_APPIDS, CORRECT_APPIDS, FAILED_APPIDS, TOTAL_WIDTH
from datetime import datetime
from colorama import init, Fore, Style
init(autoreset=True)


"""выполняет при завершении программы"""
def final_action():  # выполниться после завершения основной программы
    db_client.close_db(cursor, connection)  # закрываем соединение c БД

    # создаем отчет по сессии
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    create_statistics.create_session_report(start_time, end_time, session_game_count)
atexit.register(final_action)  # регестрируем финальную функцию

connect = db_client.connect_db() # подключаемся к БД
cursor = connect[1]
connection = connect[2]

start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

max_appid = file_reader.line_count('appids/working_appids(reference).txt') # находим максимальный appid
game_count = file_reader.line_count(WORKING_APPIDS_REFERENCE) - file_reader.line_count(WORKING_APPIDS)

# создаем счетчики
session_game_count = 0
output_serial_num = 0

# очищаем файлы с отработанными id
file_reader.clean_file(CORRECT_APPIDS)
file_reader.clean_file(FAILED_APPIDS)


"""основной цикл"""
if connect[0] == True:
    try:
        while True:
            appid = file_reader.read_appid() # читаем рабочий id
            if appid=='end': # завершаем когда полностью прочитали works_appids
                break

            game_data = api_client.parsing(appid, game_count, max_appid) # парсим по полученному id

            if isinstance(game_data, (bool, type(None))):
                file_reader.save_failed_appids(appid) # сохраняем appid с ошибкой

                left_part = f"[{Style.BRIGHT + 'ID:' + Style.RESET_ALL} {appid}] ({game_count} / {max_appid})"
                dots = '.' * (TOTAL_WIDTH - len(left_part) - len('[ ERROR ]'))

                print(f"{left_part}{dots}{Fore.RED}[ ERROR ]")
            else:
                game_dict = data_unpacker.json_unpacker(game_data) # распаковываем json

                db_load = db_client.create_game_record(cursor, connection, game_dict, game_count, max_appid) # создаем запись в БД
                if db_load == True:
                    file_reader.save_correct_appids(appid) # сохраняем корректно отрбатанный appid

            session_game_count += 1
            game_count += 1

            output_serial_num += 1
            if output_serial_num == 50: # период вывода промежуточной аналитики
                output_serial_num = 0
                # выводим промежуточную аналитику
                create_statistics.create_intermediate_session_report(session_game_count)

            time.sleep(0.1) # делаем перерыв, чтобы не нагружать API

    except KeyboardInterrupt:
        sys.exit(0)
