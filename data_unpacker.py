"""Распаковывает json и достаёт только нужные поля"""

"""распаковка json"""
def json_unpacker(game_data):
    result = {}

    # общая инфомрация
    result['name'] = game_data.get('name')
    result['appid'] = game_data.get('steam_appid')
    result['required_age'] = game_data.get('required_age')
    result['is_free'] = game_data.get('is_free')
    result['about_the_game'] = game_data.get('about_the_game')
    result['supported_languages'] = game_data.get('supported_languages')
    result['header_image'] = game_data.get('header_image')
    result['website'] = game_data.get('website')
    result['developers'] = game_data.get('developers')
    result['publishers'] = game_data.get('publishers')

    # извлекаем цену
    result['price'] = None
    package_groups = game_data.get('package_groups', [])
    if package_groups:
        subs = package_groups[0].get('subs', [])
        if subs:
            result['price'] = subs[0].get('price_in_cents_with_discount')/100


    # поддержка платформ
    result['windows'] = game_data.get('platforms', {}).get('windows')
    result['mac'] = game_data.get('platforms', {}).get('mac')
    result['linux'] = game_data.get('platforms', {}).get('linux')

    # котегории и отзывы
    result['metacritic'] = game_data.get('metacritic', {}).get('score')

    genres_list = game_data.get('genres', [])
    result['genres_ids'] = [int(g['id']) for g in genres_list if g.get('id') is not None]

    # остальное
    screenshots = game_data.get('screenshots', [])
    result['screenshots'] = screenshots[0].get('path_full') if screenshots else None

    result['release_date'] = game_data.get('release_date', {}).get('date')
    result['support_url'] = game_data.get('support_info', {}).get('url')
    result['support_email'] = game_data.get('support_info', {}).get('email')

    return result
