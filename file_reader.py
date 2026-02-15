"""РАБОТА С ФАЙЛАМИ СОДЕРЖАЩИМИ APPID"""
from configs.python_confiig import WORKING_APPIDS_REFERENCE, WORKING_APPIDS, CORRECT_APPIDS, FAILED_APPIDS

"""подсчёт длины файла (кол-во строк)"""
def line_count(file_name):
    try:
        with open(file_name, 'r') as f:
            count = sum(1 for line in f)
        return count

    except FileNotFoundError:
        print(f'Файл {file_name} не найден')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


"""считывание рабочего appid"""
def read_appid():
    try:
        file_path = WORKING_APPIDS
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
        return f"Файл {file_path} не найден."


"""сохранение appid отрабатонного с ошибкой"""
def save_failed_appids(appid):
    try:
        file_path = FAILED_APPIDS

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{appid}\n")

    except FileNotFoundError:
        return f'Файл {file_path} не найден'
    except Exception as e:
        return f'Произошла ошибка: {e}'


"""сохранение appid отрабатонного без ошибок"""
def save_correct_appids(appid):
    try:
        file_path = CORRECT_APPIDS

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{appid}\n")

    except FileNotFoundError:
        return f'Файл "{file_path}" не найден'
    except Exception as e:
        return f'Произошла ошибка: {e}'


"""перезапись файла с рабочими appid"""
def copy_from_reference():
    try:
        reference_file_path = WORKING_APPIDS_REFERENCE
        file_path = WORKING_APPIDS
        with open(reference_file_path, 'r', encoding='utf-8') as source:
            content = source.read()

        with open(file_path, 'w', encoding='utf-8') as target:
            target.write(content)

        return f'Данные из "{reference_file_path}" успешно записаны в "{file_path}"'

    except FileNotFoundError:
        return f"Ошибка: Файл '{WORKING_APPIDS_REFERENCE}' или '{WORKING_APPIDS}' не найден."
    except Exception as e:
        return f"Произошла ошибка при копировании: {e}"


"""очистка файла"""
def clean_file(file_name):
    try:
        open(file_name, 'w').close()
    except Exception as e:
        return f'Произошла ошибка при очистке файла: {e}'
