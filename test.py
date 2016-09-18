
def set_new_value(name, value):
    f = open('users.json')
    result = []
    for elem in f:
        result.append(eval(elem))
    f.close()

    f = open('users.json', 'w')
    f.close()
    
    for elem in result:
        elem[name] = value
        save_res(elem)


def save_res(results):
    f = open('users.json', 'a')
    f.write(str(results) + '\n')
    f.close()
    #log.write(str('User ' + results['nickname'] + ' added to database.')+'\n')


    
