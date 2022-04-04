from audioop import reverse
import os
import json
import time

os.system('mkdir ./by_coins')

FILE_PATH = '2022_04_01_16_13/results.json'

d = open(FILE_PATH, 'r')

y = json.loads(d.read())
x = y.get('data')


def get_my_key(obj):
    return obj['coins_per_day']


x1 = x
x1.sort(key=get_my_key, reverse=True)
for i, v in enumerate(x1):
    v1 = {
        i: v
    }
    x1[i] = v1

y['data'] = x1

z = open('./by_coins/coins_{}.json'.format(time.time()), 'a')
z.write(json.dumps(y, indent=4))
z.close()
