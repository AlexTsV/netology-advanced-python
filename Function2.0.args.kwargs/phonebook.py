class Contact:
    def __init__(self, first_name, last_name, phone_num, favorite_contact=False, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_num = phone_num
        self.favorite_contact = favorite_contact
        self.kwargs = kwargs

    def __str__(self):
        additional_info = ''
        for key, value in self.kwargs.items():
            additional_info = additional_info + f'       {key} : {value}\n'
        if not self.favorite_contact:
            return (
                f'Имя: {self.first_name} \nФамилия: {self.last_name} \nТелефон: {self.phone_num} \nВ избранных: нет '
                f'\nДополнительная информация: \n{additional_info}')
        else:
            return (
                f'Имя: {self.first_name} \nФамилия: {self.last_name} \nТелефон: {self.phone_num} \nВ избранных: да '
                f'\nДополнительная информация: \n{additional_info}')


class PhoneBook:
    contact_list = []

    def __init__(self, name):
        self.name = name

    def show_contact_list(self):
        print('Список контактов:')
        print('\n'.join(str(item) for item in PhoneBook.contact_list))

    def add_contact(self, contact):
        PhoneBook.contact_list.append(contact)
        print(contact.first_name, 'добавлен\n')

    def delete(self, num):
        for item in PhoneBook.contact_list:
            for k, v in item.items():
                if v == num:
                    PhoneBook.contact_list.remove(item)
                    print('Контакт', item.first_name, 'удален \n')

    def search_favorite(self):
        print('Избранные:')
        for item in PhoneBook.contact_list:
            if item.favorite_contact:
                print(item)

    def search(self, name, surname):
        print('Найдено: ')
        for item in PhoneBook.contact_list:
            if item.first_name == name and item.last_name == surname:
                print(item, '\n')


pb = PhoneBook('test')
jhon = Contact('Jhon', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com')
ivan = Contact('Ivan', 'Ivanov', '+79876543210', favorite_contact=True, email='ivan@ivanov.com')

pb.add_contact(jhon)
pb.add_contact(ivan)

pb.show_contact_list()
# pb.delete('+79876543210')
# pb.search_favorite()
pb.search('Jhon', 'Smith')
