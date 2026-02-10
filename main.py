"""основной файл"""
import sys
import atexit
import time
import file_reader
import api_client
import data_unpacker
import db_loader

db_loader.connect_db() # подключаемся к БД

def final_action(): # выполниться после завершения основной программы
    db_loader.close_db()  # закрываем соединение c БД

atexit.register(final_action)

"""основной цикл"""
try:
    while True:
        appid = file_reader.read_appid() # читаем рабочий id
        if appid=='end': # завершаем когда полностью прочитали works_appids
            break

        game_data = api_client.parsing(appid) # парсим по полученному id
        if game_data == False:
            file_reader.save_failed_appids(appid) # сохраняем appid с ошибкой
        else:
            file_reader.save_correct_appids(appid) # сохраняем корректно отрбатанный appid

        game_dict = data_unpacker.json_unpacker(game_data) # распаковываем json

        db_loader.create_game_record(game_dict) # создаем запись в БД

        time.sleep(0.1) # делаем перерыв, чтобы не нагружать API

except KeyboardInterrupt:
    sys.exit(0)