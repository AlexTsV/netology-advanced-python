import json
import wikipedia
import hashlib
from tqdm import tqdm

countries_list = []

with open('countries.json') as f:
    data = json.load(f)
    for i in data:
        for key, value in i.items():
            if key == 'name':
                countries_list.append(value['official'])


class My_iterator:
    def __init__(self, countries_list):
        self.countries_list = countries_list
        self.start = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start != len(self.countries_list):
            country = self.countries_list[self.start]
            try:
                country_page = wikipedia.page(country)
            except wikipedia.DisambiguationError as e:
                print(f'Ссылка для {country} изменена')
                country_for_url = e.options[0].replace(' ', '_')
                country_page = wikipedia.page(country_for_url)
                with open('wiki_links.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{country} - {country_page.url} \n')
            except wikipedia.PageError:
                print(f'Для {country} страницы не найдено')
            else:
                with open('wiki_links.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{country} - {country_page.url} \n')
        else:
            print('Finish')
            raise StopIteration


def my_generator(path_to_file):
    with open(path_to_file, 'r') as f:
        for line in f:
            yield hashlib.md5(line.encode('utf-8')).hexdigest()


for item in tqdm(My_iterator(countries_list)):
    pass

for item in my_generator('wiki_links.txt'):
    print(item)
