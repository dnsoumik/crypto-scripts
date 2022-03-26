from audioop import reverse
import os
import json
import time

os.system('mkdir ./by_price')

d = open('2022_03_23_03_01/results.json', 'r')

y = json.loads(d.read())
x = y.get('data')

def get_my_key(obj):
      return obj['price_per_day']
x1 = x
x1.sort(key=get_my_key, reverse=True)
y['data'] = x1

z = open('./by_price/price_{}.json'.format(time.time()), 'a')
z.write(json.dumps(y, indent=4))
z.close()