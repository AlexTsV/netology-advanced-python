import vk_api
import re
import json
from tqdm import tqdm

user = vk_api.User('19194690bc8529107bf0fa0c12f529e6c734e75e8cb2233e1cdd5ec01e1353c099d14718b330b61994bbe', '3075212')


def search():
    res_list = user.search()
    return res_list


res_search = search()


def mutual_friends():
    mutual_friends_list = []
    for i in tqdm(res_search):
        mutual_friends = user.get_mutual_friend(i)
        if mutual_friends is not None and len(mutual_friends) != 0:
            d = {'id': i, 'mutual_friends': mutual_friends}
            mutual_friends_list.append(d)
    return mutual_friends_list


def mutual_groups():
    mutual_groups_list = []
    user_groups = user.get_user_groups(user.user_id)
    for i in tqdm(res_search):
        res_groups = user.get_user_groups(i)
        if res_groups is not None and len(res_groups) != 0:
            all_groups = res_groups + user_groups
            mutual_groups = [i for i in all_groups if all_groups.count(i) >= 2]
            if len(mutual_groups) != 0:
                d = {'id': i, 'mutual groups': mutual_groups}
                mutual_groups_list.append(d)
    return mutual_groups_list


def get_user_interests_music_books(uid):
    res = user.get_user_info(uid)
    if res is not None:
        res[0].setdefault('interests', '')
        res[0].setdefault('music', '')
        res[0].setdefault('books', '')
        d = {'interests': res[0]['interests'], 'music': res[0]['music'], 'books': res[0]['books']}
        return d


def get_res_interests_music_books():
    res_interests_music_books = []
    for i in tqdm(res_search):
        res = user.get_user_info(i)
        if res is not None:
            d = {'id': i}
            if 'interests' in res[0]:
                d['interests'] = res[0]['interests']
            if 'music' in res[0]:
                d['music'] = res[0]['music']
            if 'books' in res[0]:
                d['books'] = res[0]['books']
            res_interests_music_books.append(d)
    return res_interests_music_books


def mutual_interests():
    list_mutual_interests = []
    usr = get_user_interests_music_books(user.user_id)
    res = get_res_interests_music_books()
    for i in res:
        i.setdefault('interests', '')
        i.setdefault('music', '')
        i.setdefault('books', '')
        res_interests = i['interests']
        if len(res_interests) != 0 and len(usr['interests']) != 0:
            user_interests = usr['interests'].replace(',', '|')
            regex = re.compile(rf'(?i){re.escape(user_interests)}')
            interests_matches = re.findall(regex, res_interests)
        else:
            interests_matches = []
        res_music = i['music']
        if len(res_music) != 0 and len(usr['music']) != 0:
            user_music = usr['music'].replace(',', '|')
            regex = re.compile(rf'(?i){re.escape(user_music)}')
            music_matches = re.findall(regex, res_music)
        else:
            music_matches = []
        res_books = i['books']
        if len(res_books) != 0 and len(usr['books']) != 0:
            user_books = usr['books'].replace(',', '|')
            regex = re.compile(rf'(?i){re.escape(user_books)}')
            books_matches = re.findall(regex, res_books)
        else:
            books_matches = []
        d = {'id': i['id'], 'interests_matches': len(interests_matches), 'music_matches': len(music_matches),
             'books_matches': len(books_matches)}
        list_mutual_interests.append(d)
    return list_mutual_interests


def mutual_info():
    res = []
    for i in mutual_friends():
        res.append(i)
        if len(res) == 10:
            return res
    for i in mutual_groups():
        res.append(i)
        if len(res) == 10:
            return res
    for i in mutual_interests():
        res.append(i)
        if len(res) == 10:
            return res


def run():
    res_list = []
    for i in mutual_info():
        r = user.get_photo(i['id'])
        r.sort(key=lambda d: d['likes'], reverse=True)
        top3_photo = []
        for e in r[:3]:
            top3_photo.append(e['photo'])
        d = {'id': i['id'], 'photo': top3_photo}
        res_list.append(d)
    db = vk_api.User.connect_db.result(vk_api.usr.user_id, json.dumps(res_list))
    return db


print(run())
