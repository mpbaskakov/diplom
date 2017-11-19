import time
import json
import requests

USER_ID = ''


def api(method, params):
    parameters = {
        'access_token': '',
        'v': '5.69',
        }
    parameters.update(params)
    response = requests.get('https://api.vk.com/method/{}'.format(method), parameters)
    return response.json()['response']


def get_userid(user_id):
    response = api('users.get', {'user_ids': user_id, 'fields': 'id'})
    user_id = response[0]['id']
    return user_id


def get_friends(user_id):
    response = api('friends.get', {'user_id': user_id})
    friends = response['items']
    return friends


def get_groups(user_id):
    response = api('groups.get', {'user_id': user_id})
    groups = response['items']
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
    group_info = api('groups.get', {'user_id': user_id, 'fields': 'members_count', 'extended': 1})
    return group_info


def main():
    user_id = get_userid(USER_ID)
    unique_groups = list(get_unique_groups(user_id))
    user_groups = get_group_info(user_id)
    group_info = []
    for g in user_groups['items']:
        if g['id'] in unique_groups:
            group_info.append(dict(name=g['name'], gid=g['id'], members_count=g['members_count']))
        else:
            pass
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(group_info, f, ensure_ascii=False, indent=2)

main()
