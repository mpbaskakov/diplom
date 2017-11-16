import time
import json
import requests

USER_ID = 'tim_leary'


def api(method, params):
    parameters = {
        'access_token': '',
        'v': '5.69',
        }
    parameters.update(params)
    response = requests.get('https://api.vk.com/method/' + method + '.get', parameters)
    return response


def get_userid(user_id):
    response = api('users', {'user_ids': user_id, 'fields': 'id'})
    user_id = response.json()['response'][0]['id']
    return user_id


def get_friends(user_id):
    response = api('friends', {'user_id': user_id})
    friends = response.json()['response']['items']
    return friends


def get_groups(user_id):
    response = api('groups', {'user_id': user_id})
    groups = response.json()['response']['items']
    return groups


def get_unique_groups(user_id):
    friends = get_friends(user_id)
    main_groups = get_groups(user_id)
    groups = set()
    for f in friends:
        try:
            groups.update(get_groups(f))
            time.sleep(0.4)
            print('-')
        except KeyError:
            pass
    unique_groups = set(main_groups).difference(groups)
    return unique_groups


def get_group_info(user_id):
    response = api('groups', {'user_id': user_id, 'fields': 'members_count', 'extended': 1})
    group_info = response.json()['response']
    return group_info


def main():
    user_id = get_userid(USER_ID)
    unique_groups = list(get_unique_groups(user_id))
    user_groups = get_group_info(user_id)
    group_info = []
    for g in range(0, user_groups['count'] - 1):
        if unique_groups.count(user_groups['items'][g]['id']) > 0:
            group_info.append(dict(
                {'name': user_groups['items'][g]['name'], 'gid': user_groups['items'][g]['id'],
                 'members_count': user_groups['items'][g]['members_count']}))
        else:
            pass
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(group_info, f, ensure_ascii=False, indent=2)

main()
