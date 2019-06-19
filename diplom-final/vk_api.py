import requests
import time
from datetime import datetime
import db_app


class User:
    connect_db = db_app.Postgres('postgres', 'postgres', '123')

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def parametres(self):
        param = {
            'v': 5.92,
            'access_token': self.token,
            'user_id': self.user_id,
        }
        return param

    def get_user_info(self, id):
        params = {
            'v': 5.92,
            'access_token': self.token,
            'user_ids': id,
            'fields': 'bdate, sex, city, interests, music, books',
        }
        counter = 1
        try:
            response = requests.get('https://api.vk.com/method/users.get', params)
            for key, value in response.json().items():
                if key == 'response':
                    return value
                else:
                    counter += 1
                    raise Warning

        except Warning:
            while counter == 1:
                time.sleep(1)
                response = requests.get('https://api.vk.com/method/groups.get', params)
                for key, value in response.json().items():
                    if key == 'response':
                        return value
                    else:
                        for k, v in value.items():
                            if k == 'error_msg' and v != 'Too many requests per second':
                                counter = 0

    def get_mutual_friend(self, target):
        params = {
            'v': 5.92,
            'access_token': self.token,
            'id': self.user_id,
            'source_uid': self.user_id,
            'target_uids': target,
        }
        counter = 1
        try:
            response = requests.get('https://api.vk.com/method/friends.getMutual', params)
            for key, value in response.json().items():
                if key == 'response':
                    return value[0]['common_friends']
                else:
                    counter += 1
                    raise Warning
        except Warning:
            while counter == 1:
                time.sleep(1)
                response = requests.get('https://api.vk.com/method/friends.getMutual', params)
                for key, value in response.json().items():
                    if key == 'response':
                        return value[0]['common_friends']
                    else:
                        for k, v in value.items():
                            if k == 'error_msg' and v != 'Too many requests per second':
                                counter = 0

    def get_user_groups(self, id):
        params = {
            'v': 5.92,
            'access_token': self.token,
            'user_id': id,
        }
        groups = []
        counter = 0
        try:
            response = requests.get('https://api.vk.com/method/groups.get', params)
            for key, value in response.json().items():
                if key == 'response':
                    for k, v in value.items():
                        if k == 'items':
                            for group_id in v:
                                groups.append(group_id)
                else:
                    counter += 1
                    raise Warning
        except Warning:
            while counter == 1:
                time.sleep(1)
                response = requests.get('https://api.vk.com/method/groups.get', params)
                for key, value in response.json().items():
                    if key == 'response':
                        for k, v in value.items():
                            if k == 'items':
                                if len(v) != 0:
                                    for group_id in v:
                                        groups.append(group_id)
                                        counter = 0
                                else:
                                    groups.append(v)
                                    counter = 0
                    else:
                        for k, v in value.items():
                            if k == 'error_msg' and v != 'Too many requests per second':
                                counter = 0
        return groups

    def get_age_user(self):
        try:
            res = User.get_user_info(self, self.user_id)
            bdate = datetime.strptime(res[0]['bdate'], '%d/%m/%Y').date()
            age = datetime.today().year - bdate.year
            return age
        except ValueError:
            age = 30
            return age

    def search(self):
        list_id = []
        params = {
            'v': 5.89,
            'access_token': self.token,
            'id': self.user_id,
            'q': '',
            'city': '1',
            'age_from': self.get_age_user() - 5,
            'age_to': self.get_age_user() + 5,
            'status': 6,
            'has_photo': 1,
            'is_closed': False,
            'count': '1000',
            'sex': '',
        }
        sex = self.get_user_info(self.user_id)[0]['sex']
        if sex == 1:
            params['sex'] = 0
        if sex == 0:
            params['sex'] = 1
        vk_offset = self.connect_db.get_offset(self.user_id)
        if len(vk_offset) != 0:
            if vk_offset[0][0] >= 990:
                self.connect_db.update_offset(0)
                params['offset'] = 0
            else:
                params['offset'] = vk_offset[0][0]
        else:
            self.connect_db.user_info(self.user_id, 0)
            params['offset'] = 0
        counter = 0
        try:
            response = requests.get('https://api.vk.com/method/users.search', params)
            for key, value in response.json().items():
                if key == 'response':
                    for k, v in value.items():
                        if k == 'items':
                            for i in v:
                                list_id.append(i['id'])
                else:
                    counter += 1
                    raise Warning
        except Warning:
            while counter == 1:
                time.sleep(1)
                response = requests.get('https://api.vk.com/method/groups.get', params)
                for key, value in response.json().items():
                    if key == 'response':
                        for k, v in value.items():
                            if k == 'items':
                                for i in v:
                                    list_id.append(i['id'])
                        counter = 0
                    else:
                        for k, v in value.items():
                            if k == 'error_msg' and v != 'Too many requests per second':
                                counter = 0
        offset = len(list_id) + self.connect_db.get_offset(self.user_id)[0][0]
        self.connect_db.update_offset(offset)
        return list_id

    def get_photo(self, id):
        photo_list = []
        counter = 0
        params = {
            'v': 5.92,
            'access_token': self.token,
            'owner_id': id,
            'album_id': 'profile',
            'extended': 1,
        }
        try:
            response = requests.get('https://api.vk.com/method/photos.get', params)
            for key, value in response.json().items():
                if key == 'response':
                    for k, v in value.items():
                        if k == 'items':
                            for i in v:
                                d = {'id': id, 'photo': i['sizes'][-1]['url'], 'likes': i['likes']['count']}
                                photo_list.append(d)
                else:
                    counter += 1
                    raise Warning

        except Warning:
            while counter == 1:
                time.sleep(1)
                response = requests.get('https://api.vk.com/method/photos.get', params)
                for key, value in response.json().items():
                    if key == 'response':
                        for k, v in value.items():
                            if k == 'items':
                                for i in v:
                                    d = {'id': id, 'photo': i['sizes'][-1]['url'], 'likes': i['likes']['count']}
                                    photo_list.append(d)
                        counter = 0
                    else:
                        for k, v in value.items():
                            if k == 'error_msg' and v != 'Too many requests per second':
                                counter = 0
        return photo_list


usr = User('19194690bc8529107bf0fa0c12f529e6c734e75e8cb2233e1cdd5ec01e1353c099d14718b330b61994bbe', '3075212')