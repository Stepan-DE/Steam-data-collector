"""Парсит данные"""
import requests

"""парсим данные по полученному appid и региону"""
def parsing(appid, country='ru'):
    try:
        url = f"https://store.steampowered.com/api/appdetails"
        params = {
            'appids': appid,
            'cc': country,
            'l': 'russian'
        }

        response = requests.get(url, params=params)
        result = response.json()
    except Exception as e:
        print(f"Ошибка при парсинге {appid}: {e}")
        return False
    if str(appid) in result and result[str(appid)].get('success'):
        return result[str(appid)]['data'] # словарь на выходе
    else:
        print(f"Ошибка: нет данных для игры {appid}")
        return False