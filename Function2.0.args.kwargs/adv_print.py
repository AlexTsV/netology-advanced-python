def adv_print(*args, start='test', max_line=100, in_file=False):
    if not in_file:
        if start != '':
            string = start + ' ' + ' '.join(str(arg) for arg in args)
        else:
            string = ' '.join(str(arg) for arg in args)
        while len(string) > max_line:
            with open('log.txt', 'a') as f:
                f.write(f'{string[0:max_line]} \n')
                print(string[0:max_line])
                string = string[max_line:]
        if len(string) < max_line:
            with open('log.txt', 'a') as f:
                f.write(f'{string} \n')
            print(string)
    else:
        if start != '':
            string = start + ' ' + ' '.join(str(arg) for arg in args)
        else:
            string = ' '.join(str(arg) for arg in args)
        while len(string) > max_line:
            print(string[0:max_line])
            string = string[max_line:]
        if len(string) < max_line:
            print(string)


adv_print('qwertyu', 123, [1, 2, 3, 4, 5, 6, 7, 8])
