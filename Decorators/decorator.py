import datetime
import hashlib


def logger(path_to_log):
    def replacement(old_function):
        def new_function(*args):
            start = datetime.datetime.now()
            name = old_function.__name__
            with open(path_to_log, 'w') as f:
                f.write(f'{start} {name}({args}) \n')
            for item in old_function(*args):
                with open(path_to_log, 'a') as f:
                    f.write(f'{item} \n')
        return new_function
    return replacement


@logger('log.txt')
def my_generator(path_to_file):
    with open(path_to_file, 'r') as f:
        for line in f:
            yield hashlib.md5(line.encode('utf-8')).hexdigest()


my_generator('wiki_links.txt')
