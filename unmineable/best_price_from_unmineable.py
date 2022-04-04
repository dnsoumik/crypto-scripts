import requests
import json
import time
import os
from datetime import datetime as date
today = date.now()
d1 = today.strftime("%Y_%m_%d_%H_%M")

ETA_HASHPOWER = 175

allCoins = []
allCoinDt = []

print('STARTED IN {}'.format(d1))

if (os.system('ls {}'.format(d1)) == 512):
    os.system('mkdir {}'.format(d1))
    response = requests.get("https://api.unminable.com/v4/coin")
    allCoinsRaw = json.loads(response.content)
    for idx, cn in enumerate(allCoinsRaw.get('data')):
        time.sleep(0.1)
        resp = requests.post(
            'https://api.unminable.com/v3/calculate/reward',
            data={
                "mh": str(ETA_HASHPOWER),
                "algo": "ethash",
                "coin": cn.get('symbol')
            }
        )
        cn['reward'] = json.loads(resp.content)
        print(idx+1, cn.get('name'), cn['reward'])

    af = open('./{}/coins.json'.format(d1), 'a')
    af.write(json.dumps(allCoinsRaw, indent=4))
    af.close()
    allCoins = allCoinsRaw.get('data')

    response = requests.get(
        'https://api.coinmarketcap.com/data-api/v3/map/all?listing_status=active,untracked&exchangeAux=is_active,status&cryptoAux=is_active,status&start=1&limit=10000')

    allCoinDtRaw = json.loads(response.content)
    ad = open('./{}/coin_details.json'.format(d1), 'a')
    ad.write(json.dumps(allCoinDtRaw, indent=4))
    ad.close()
    allCoinDt = allCoinDtRaw.get('data').get('cryptoCurrencyMap')

else:
    print('FILES ARE ALREADY DOWNLOADED')
    af = open('./{}/coins.json'.format(d1), 'r')
    allCoinsRaw = json.loads(af.read())
    allCoins = allCoinsRaw.get('data')
    af.close()

    ad = open('./{}/coin_details.json'.format(d1), 'r')
    allCoinDtRaw = json.loads(ad.read())
    allCoinDt = allCoinDtRaw.get('data').get('cryptoCurrencyMap')
    ad.close()


allPrices = {
    'data': []
}
print('FETCHING PRICE DETAILS IN INR')
for idx, coin in enumerate(allCoins):
    time.sleep(1)
    sym = coin.get('symbol')
    name = coin.get('name')
    reward = coin.get('reward')
    convert_id = None
    for ci in allCoinDt:
        if (sym == str(ci['symbol'])):
            resp = requests.get('https://api.coinmarketcap.com/data-api/v3/tools/price-conversion?amount={}&convert_id=2796&id={}'.format(
                1,
                ci['id']
            ))
            try:
                price = json.loads(resp.content).get('data').get('quote')[0]
                priceObj = {
                    'name': name,
                    'symbol': sym,
                    'price': price.get('price'),
                    'chains': coin.get('chains'),
                    'currency': 'INR',
                    'price_per_day': price.get('price') * reward.get('per_day'),
                    'price_per_month': price.get('price') * reward.get('per_month'),
                    'coins_per_day': reward.get('per_day'),
                    'coins_per_month': reward.get('per_month'),
                }
                print('\n', idx+1, ': ', priceObj)
                allPrices['data'].append(priceObj)
            except:
                continue

f = open('./{}/results.json'.format(d1), 'a')
f.write(json.dumps(allPrices, indent=4))
f.close()
