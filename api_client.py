"""Парсит данные"""
import requests
from colorama import init, Fore, Style
from configs.python_confiig import TOTAL_WIDTH

init(autoreset=True)

"""парсим данные по полученному appid и региону"""
def parsing(appid, game_count, max_appid):
    left_part = f"[{Style.BRIGHT + 'ID:' + Style.RESET_ALL} {appid}] ({game_count} / {max_appid})"
    dots = '.' * (TOTAL_WIDTH - len(left_part) - len('[ ERROR ]'))

    try:
        url = f"https://store.steampowered.com/api/appdetails"
        params = {
            'appids': appid,
            'cc': 'ru',
            'l': 'russian'
        }

        response = requests.get(url, params=params)
        result = response.json()

    except Exception as e:
        print(f"{left_part}{dots}{Fore.RED}[ ERROR ]")
        return False

    try:
        if str(appid) in result and result[str(appid)].get('success'):
            return result[str(appid)]['data'] # словарь на выходе
        else:
            return False
    except TypeError:
        print(f"{left_part}{dots}{Fore.RED}[ ERROR ]")
        return False
