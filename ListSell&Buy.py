import requests

choice="mirage_prime_systems"
url = f'https://api.warframe.market/v1/items/{choice}/orders?include=item'
headers = {
    'accept': 'application/json',
    'Platform': 'pc'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    for order in data['payload']['orders']:
        if order['user']['status'] == 'online' or order['user']['status'] == 'ingame':
            if order['order_type'] == 'sell':
                userSell=order['user']['ingame_name']
                sellPrice=order['platinum']
                print(f'/w {userSell} Hi, I want to buy: "{choice}" for {sellPrice} platinum. (warframe.market)')
                print(order['platinum'])
            # if order['order_type'] == 'buy':
            #     userSell=order['user']['ingame_name']
            #     sellPrice=order['platinum']
            #     print(f'/w {userSell} Hi, I want to sell: "{choice}" for {sellPrice} platinum. (warframe.market)')
            #     print(order['platinum'])
else:
    print(f'Request failed with status code {response.status_code}')