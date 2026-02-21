def map_practice():
    key = range(10)
    value = map(lambda x: x * 2, range(10))
    dict1 = dict(zip(key, value))
    dict2 = {x: x * 2 for x in range(10)}
    print('='*20)
    for key,val in dict1.items():
        print(key,val)
    print('='*20)
    for key,val in dict2.items():
        print(key,val)

if __name__ == '__main__':
    map_practice()