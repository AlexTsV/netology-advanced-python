import csv
import re

from pymongo import MongoClient

client = MongoClient()
mongo_db = client.mongo_db


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        collect = []
        for line in reader:
            collect.append({'Исполнитель': line['Исполнитель'], 'Цена': line['Цена'], 'Место': line['Место'],
                            'Дата': line['Дата']})
        res = db.artists.insert_many(collect)
        return res


def find_cheapest(db):
    """
    Найти самые дешевые билеты
    Документация: https://docs.mongodb.com/manual/reference/operator/aggregation/sort/
    """
    res = db.artists.aggregate([{'$sort': {'Цена': -1}}])
    print(list(res)[0])


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и выведите их по возрастанию цены
    """
    regex = re.compile(rf'(?i)[a-zA-Zа-яА-Я -]*?{re.escape(name)}')
    res = db.artists.find({'Исполнитель': regex}).sort([('Цена', 1)])
    for r in res:
        print(r)


if __name__ == '__main__':
    # read_data('artists.csv', mongo_db)
    # find_cheapest(mongo_db)
    find_by_name('шуф', mongo_db)
