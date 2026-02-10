"""РАБОТА С ФАЙЛАМИ СОДЕРЖАЩИМИ APPID"""


"""считывание рабочего appid"""
def read_appid():
    try:
        file_path = 'appids/working_appids.txt'
        with open(file_path, 'r') as f:
            lines = f.readlines()

        if not lines:
            print("Файл оказался пустым. Все строки считаны.")
            return 'end'

        first_line = lines[0].strip()

        with open(file_path, 'w') as f:
            f.writelines(lines[1:])

        return first_line

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None


"""сохранение appid отрабатонного с ошибкой"""
def save_failed_appids(appid):
    try:
        file_path = 'appids/failed_appids.txt'

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{appid}\n")

    except FileNotFoundError:
        print(f'Файл {file_path} не найден')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


"""сохранение appid отрабатонного без ошибок"""
def save_correct_appids(appid):
    try:
        file_path = 'appids/correct_appids.txt'

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{appid}\n")

    except FileNotFoundError:
        print(f'Файл {file_path} не найден')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


"""перезапись файла с рабочими appid"""
def copy_from_reference():
    try:
        referens_file_path = 'appids/working_appids(referens).txt'
        file_path = 'appids/working_appids.txt'
        with open(referens_file_path, 'r', encoding='utf-8') as source:
            content = source.read()

        with open(file_path, 'w', encoding='utf-8') as target:
            target.write(content)

        message = f'Данные из "{referens_file_path}" успешно записаны в "{file_path}"'
        return message

    except FileNotFoundError:
        print("Ошибка: Файл working_appids(referens).txt не найден.")
        return False
    except Exception as e:
        print(f"Произошла ошибка при копировании: {e}")
        return False

a = copy_from_reference()
print(a)