"""Распаковывает json и достаёт только нужные поля"""

"""распаковка json"""
def json_unpacker(game_data):
    result = {}

    result['name']=game_data.get('name')
    result['appid']=game_data.get('steam_appid')
    result['min_age']=game_data.get('required_age')
    result['is_free']=game_data.get('is_free')
    result['description']=game_data.get('about_the_game')
    result['supported_languages']=game_data.get('supported_languages')
    result['header_image']=game_data.get('header_image')
    result['capsule_image']=game_data.get('capsule_image')
    result['website']=game_data.get('website')
    result['pc_requirements']=game_data.get('pc_requirements')
    result['mac_requirements']=game_data.get('mac_requirements')
    result['linux_requirements']=game_data.get('linux_requirements')
    result['developers']=game_data.get('developers')
    result['publishers']=game_data.get('publishers')
    result['price']=game_data.get('price_overview')
    result['platforms']=game_data.get('platforms')
    result['metacritic']=game_data.get('metacritic')
    result['categories']=game_data.get('categories')
    result['genres']=game_data.get('genres')
    result['screenshots']=game_data.get('screenshots')
    result['movies']=game_data.get('movies')
    result['release_date']=game_data.get('release_date')
    result['movies']=game_data.get('movies')

    return result # возвращает список