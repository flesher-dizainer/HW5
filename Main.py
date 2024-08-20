from cities import cities_list
from os import path
import json


# загружаем список городов из json файла
def get_cities_list_from_json(file_name):
    try:
        with open(file_name, 'r', encoding='cp1251') as file:
            return json.load(file)
    except FileNotFoundError:
        return ''


# сохраняем список городов в json
def save_dict_to_json(file_name, cities_list_dict):
    with open(file_name, 'w', encoding='cp1251') as file:
        json.dump(cities_list_dict, file, ensure_ascii=False, indent=4)


# возврат множества городов
def get_cities_set(dict_cities):
    result = {i['name'] for i in dict_cities}
    return result


# удаление городов из множества, которые заканчиваются на плохие буквы
def del_bad_cities_name(cities_set):
    first_cities_name = [char[0].lower() for char in cities_set]
    new_cities_set = {city_name for city_name in cities_set if city_name[-1].lower() in first_cities_name}
    return new_cities_set


def get_user_city_name(first_letter_city_name):
    return input(f'Введите название города начинающийся на букву {first_letter_city_name} \n')


def get_machine_city_name(first_letter_city_name, cities_set):
    print(f"Машина должна выбрать название города начинающийся на букву {first_letter_city_name}")
    for fist_char_city_name in cities_set:
        if first_letter_city_name.lower() == fist_char_city_name[0].lower():
            print(f"Машина выбрала название города {fist_char_city_name}")
            return fist_char_city_name
    print(f"Машина не смогла найти город начинающийся на букву {first_letter_city_name}")
    return ''


# проверка на желание игрока закончить игру
def check_user_stop(user_city_name):
    return user_city_name.lower() == 'стоп'


# проверка на наличие названия города в списке
def check_city_name(city_name, cities_set):
    cities_name_list = [city_name_from_set.lower() for city_name_from_set in cities_set]
    return city_name.lower() in cities_name_list


# загрузка списка результатов игр в json
def load_result_game_json():
    try:
        with open('result_game.json', 'r', encoding='cp1251') as file:
            return json.load(file)
    except:
        return None


# сохранение результатов игры в json файл
def save_result_game_json(result_game: dict):
    list_result_game = []
    try:
        with open('result_game.json', 'r+', encoding='cp1251') as file:
            try:
                list_result_game = json.load(file)
            except:
                list_result_game = []
            if len(list_result_game) >= 5:
                list_result_game.pop(0)
    except FileNotFoundError:
        pass
    list_result_game.append(result_game)
    with open('result_game.json', 'w+', encoding='cp1251') as file:
        try:
            json.dump(list_result_game, file, ensure_ascii=False, indent=4)
        except:
            print('Error save game result')


def main():
    if path.exists('cities.json'):
        cities_list_json = get_cities_list_from_json('cities.json')
        cities_set = get_cities_set(cities_list_json)
    else:
        # формируем множество городов
        cities_set = get_cities_set(cities_list)
        save_dict_to_json('cities.json', cities_list)
    # удаляем названия городов, заканчивающиеся на плохую букву
    cities_set = del_bad_cities_name(cities_set)
    # загружаем прошлую статистику игр
    statistic_game_json = load_result_game_json()
    if statistic_game_json == None:
        print('Игр ещё небыло или статистика не найдена')
    else:
        for game_result in statistic_game_json:
            print(game_result)
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
        save_result_game_json([{'user': '0', 'machine': '1'}])
    else:
        save_result_game_json([{'user': '1', 'machine': '0'}])


if __name__ == "__main__":
    main()
