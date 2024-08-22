"""
Игра в города. Игрок играет против машины.
"""
from cities import cities_list
import json


def get_cities_list_from_json(file_name: str) -> list[dict] | None:
    """
    Функция загрузки данных городов из json файла
    :param file_name: Имя файла для загрузки
    :return: возвращаем список словарей городов
    """
    try:
        with open(file_name, 'r', encoding='cp1251') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def save_dict_to_json(file_name: str, cities_list_dict: list[dict]) -> bool:
    """
    Функция сохранения массива словарей городов в json файл
    :param file_name: имя файла для сохранения
    :param cities_list_dict: список словарей городов
    :return: возвращаем True если успешно сохранено, иначе False
    """
    try:
        with open(file_name, 'w', encoding='cp1251') as file:
            json.dump(cities_list_dict, file, ensure_ascii=False, indent=4)
        return True
    except Exception as error_info:
        print(error_info)
        return False


def get_cities_set(dict_cities: list[dict]) -> set:
    """
    Функция возврата множества городов из списка словарей городов
    :param dict_cities: список словарей
    :return: множество городов
    """
    return {city['name'] for city in dict_cities}


def del_bad_cities_name(cities_set: set) -> set:
    """
    Удаление городов из множества, которые заканчиваются на плохие буквы
    :param cities_set: множество названий городов
    :return: возвращает новое множество городов
    """
    # создаём список с первыми буквами городов. Все буквы делаем маленькие.
    first_cities_name = [city_name[0].lower() for city_name in cities_set]
    # проверяем последняя буква названия города есть ли в списке первых букв названий городов городов
    return {city_name for city_name in cities_set if city_name[-1].lower() in first_cities_name}


def get_user_city_name(first_letter_city_name: str) -> str:
    """
    Функция запроса названия города у игрока
    :param first_letter_city_name: Буква, с которой должно начинаться название города
    :return: возвращаем город, который написал игрок
    """
    return input(f'Введите название города начинающийся на букву {first_letter_city_name} \n')


def get_machine_city_name(first_letter_city_name: str, cities_set: set) -> str | None:
    """
    Функция выбора города машиной.
    :param first_letter_city_name: Первая буква, с которой должно начинаться название города
    :param cities_set: множество городов
    :return: возвращаем название города или None
    """
    print(f"Машина должна выбрать название города начинающийся на букву {first_letter_city_name}")
    for fist_char_city_name in cities_set:
        if first_letter_city_name.lower() == fist_char_city_name[0].lower():
            print(f"Машина выбрала название города {fist_char_city_name}")
            return fist_char_city_name
    print(f"Машина не смогла найти город начинающийся на букву {first_letter_city_name}")
    return None


def check_user_stop(user_stop_name: str) -> bool:
    """
    Функция проверки желания игрока закончить игру
    :param user_stop_name: проверка ввода игрока на стоп
    :return: True если игрок ввёл стоп, иначе False
    """
    return user_stop_name.lower() == 'стоп'


def check_city_name(city_name: str, cities_set: set) -> bool:
    """
    Функция проверки наличия названия города в списке.
    :param city_name: Название города
    :param cities_set: Множество с названиями городов
    :return: Возвращаем True, если название города есть в списке, иначе False
    """
    cities_name_list = [city_name_from_set.lower() for city_name_from_set in cities_set]
    return city_name.lower() in cities_name_list


def load_result_game_json(file_name: str) -> list[dict] | None:
    """
    Функция загрузки результатов прошлых игр
    :param file_name: название json файла с результатами игр
    :return: При успешной загрузке результатов вернёт список словарей иначе None
    """
    try:
        with open(file_name, 'r', encoding='cp1251') as file:
            return json.load(file)
    except ValueError:
        return None
    except FileNotFoundError:
        return None


# сохранение результатов игры в json файл
def save_result_game_json(file_name_json: str, result_game: dict) -> bool:
    """
    Функция сохранения результата последних 5 игр в json файл.
    :param file_name_json: Имя json файла для сохранения результата игры
    :param result_game: результат игры Игрока против Машины
    :return: результат сохранения True(успешно), False(ошибки при сохранении)
    """
    list_result_game = load_result_game_json(file_name_json)
    if list_result_game is None:
        list_result_game = []
    else:
        if len(list_result_game) >= 5:
            list_result_game.pop(0)
    list_result_game.append(result_game)
    with open(file_name_json, 'w+', encoding='cp1251') as file:
        try:
            json.dump(list_result_game, file, ensure_ascii=False, indent=4)
        except ValueError:
            print('Error save game result')
            return False
    return True


def print_game_statistics(list_game_result: list[dict]) -> None:
    """
    Функция вывода на экран статистики прошлых игр
    :param list_game_result: список результатов игр
    :return: Ничего не возвращаем
    """
    print('Результаты прошлых игр:')
    [print(game_result) for game_result in list_game_result]
    return None


def main():
    """
    основная функция игры в города.
    :return:
    """
    file_name_game_result = 'result_game.json'
    file_name_cities_json = 'cities.json'

    # загружаем прошлую статистику игр
    statistic_game_json = load_result_game_json(file_name_game_result)
    if statistic_game_json is None:
        print('Игр ещё небыло или статистика не найдена')
    else:
        print_game_statistics(statistic_game_json)

    # загружаем json списка словарей городов
    cities_list_json = get_cities_list_from_json(file_name_cities_json)
    if cities_list_json is None:
        cities_list_json = cities_list
        save_dict_to_json(file_name_cities_json, cities_list_json)
    # формируем множество городов из списка словарей
    cities_set = get_cities_set(cities_list)
    # удаляем названия городов, заканчивающиеся на плохую букву
    cities_set = del_bad_cities_name(cities_set)

    start = True
    char_city_name = ''
    user_id = 1
    while True:
        if user_id == 1:
            if start:
                input_user_city_name = get_user_city_name('любую')
                start = False
            else:
                input_user_city_name = get_user_city_name(char_city_name)
            # проверка на остановку игры
            if check_user_stop(input_user_city_name):
                print('Вы проиграли!')
                break
            # проверка на наличие города
            if not check_city_name(input_user_city_name, cities_set):
                print("Вы проиграли")
                break
        else:
            input_user_city_name = get_machine_city_name(char_city_name, cities_set)
            if input_user_city_name == '':
                print('Вы выиграли!')
                break
        # удаляем из множества название города
        cities_set.discard(input_user_city_name)
        # присваем букву, с которой должно начинаться название города
        char_city_name = input_user_city_name[-1].upper()
        user_id = user_id ^ 1
    if user_id == 1:
        result_game_dict = {'user': '0', 'machine': '1'}
    else:
        result_game_dict = {'user': '1', 'machine': '0'}
    if not save_result_game_json(file_name_game_result, result_game_dict):
        print('Ошибка при сохранении результатов игры')


if __name__ == "__main__":
    main()
