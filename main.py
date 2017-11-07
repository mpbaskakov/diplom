from pprint import pprint
import time
import json
import requests

ACCESS_TOKEN = ''
USER_ID = 100000


def get_friends(user_id):
    params = {
        'user_id': user_id,
        'access_token': ACCESS_TOKEN,
        'v': '5.69'
    }
    response = requests.get('https://api.vk.com/method/friends.get', params)
    if user_id == 0:
        friends = dict.fromkeys(response.json()['response']['items'])
    else:
        friends = response.json()['response']['items']
    return friends


def get_groups(user_id):
    params = {
        'user_id': user_id,
        'access_token': ACCESS_TOKEN,
        'v': '5.69'
    }
    response = requests.get('https://api.vk.com/method/groups.get', params)
    groups = response.json()['response']['items']
    return groups


def get_unique_groups(user_id):
    friends = get_friends(user_id)
    main_groups = get_groups(user_id)
    groups = []
    for f in friends:
        try:
            groups += get_groups(f)
            time.sleep(0.4)
            print('-')
        except KeyError:
            pass
    unique_groups = set(main_groups) & set(groups)
    return unique_groups


def get_group_info(group_id):
    params = {
        'group_id': group_id,
        'access_token': ACCESS_TOKEN,
        'fields': 'name',
        'fields': 'members_count'
    }
    response = requests.get('https://api.vk.com/method/groups.getById', params)
    group_info = response.json()['response'][0]
    return group_info


def main():
    unique_groups = get_unique_groups(USER_ID)
    group_info = []
    for g in unique_groups:
        try:
            group_info.append({'name': get_group_info(g)['name'], 'gid': g, 'members_count': get_group_info(g)['members_count']})
            time.sleep(0.4)
        except KeyError:
            pass
    with open('groups.json', 'w') as f:
        json.dump(group_info, f)

main()
