from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# print(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
name_list = []
for item in contacts_list:
    name = re.split(r"\W+", item[0])
    name_list.append(name[0])
duplicates = (set([x for x in name_list if name_list.count(x) > 1]))
unique_name_list = []
for i in duplicates:
    temp_list = []
    for item in contacts_list:
        if i in item[0]:
            item[0] = re.split(r"\W+", item[0])
            for k in item[0]:
                temp_list.append(k)
            temp_list += item[1:]
    unique_name_list.append(sorted(set(temp_list), key=lambda x: temp_list.index(x)))
for item in unique_name_list:
    for i in item:
        if '495' in i:
            index = (item.index(i))
            item[-1], item[index] = item[index], item[-1]
    for i in item:
        if '@' in i:
            index = (item.index(i))
            item[-1], item[index] = item[index], item[-1]
"""Не могу понять почему вторая запись Лагунцов не удаляется с первого раза, хотя с Мартиняхин всё ок"""
for item in contacts_list:
    for i in duplicates:
        if i in item[0]:
            contacts_list.remove(item)
for item in contacts_list:
    for i in duplicates:
        if i in item[0]:
            contacts_list.remove(item)
for item in unique_name_list:
    contacts_list.append(item)

my_string = '\n'.join(str(x) for x in contacts_list)
my_string = my_string.replace("'", '')
my_string = my_string.replace("[", '')
my_string = my_string.replace("]", '')

regex = (r"(^\w+[^lastname, firstname, surname, organization, position, phone, email\n"
	r"])(,\s|\s)(\w+)(,\s|\s)(\w+)(,\s,\s,\s|,\s,\s|,\s)(\w+)(,)(\s)(,)?(\s)?(.+[а-яёА-ЯЁ][^.доб]|\w+,)?(\s\+7|\+7|8|)"
         r"(\s\(|\(|\s)?(\d{3})?(\)\s|-|\))?(\d{3})?(\-)?(\d{2})?(\-)?(\d{2})?(,)?(\s\(|\s)?((доб.)+(\s)?(\d+)(,)?(\)?)"
         r"(,)?(\s)?)?(\d+|[A-z,a-z]+\.[A-z,a-z]+|[A-z,a-z]+)?(@+\w+\.\w+)?")

subst = "\\1,\\3,\\5,\\7\\8\\10\\30\\12+7(\\15)\\17-\\19-\\21\\26\\25\\27,\\32\\33"
my_string = re.sub(regex, subst, my_string, 0, re.MULTILINE)
my_list = []
my_string = my_string.split('\n')
for i in my_string:
    a = i.split(',')
    if 'firstname' in i:
        i = i.replace(' ', '')
    a = i.split(',')
    my_list.append(a)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(my_list)
