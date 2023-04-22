import requests
import json
import pyperclip

def GetOrderData(ordertype, orderitem):
    url = f'https://api.warframe.market/v1/items/{orderitem}/orders?include=item'
    headers = {
        'accept': 'application/json',
        'Platform': 'pc'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for order in data['payload']['orders']:
            if order['user']['status'] == 'online' or order['user']['status'] == 'ingame':
                if ordertype and order['order_type'] == 'sell':
                    userSell=order['user']['ingame_name']
                    sellPrice=order['platinum']
                    print(f'/w {userSell} Hi, I want to buy: "{choice}" for {sellPrice} platinum. (warframe.market)')
                    print(order['platinum'])
                elif ordertype and order['order_type'] == 'buy':
                    userSell=order['user']['ingame_name']
                    sellPrice=order['platinum']
                    print(f'/w {userSell} Hi, I want to sell: "{choice}" for {sellPrice} platinum. (warframe.market)')
                    print(order['platinum'])
    else:
        print(f'Request failed with status code {response.status_code}')

if __name__ == "__main__":
    typeOrder="buy"
    choice="mirage_prime_systems"
    Price = GetOrderData(typeOrder, choice)