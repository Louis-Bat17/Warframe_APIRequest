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
        offerData = []
        for order in data['payload']['orders']:
            if order['user']['status'] == 'online' or order['user']['status'] == 'ingame':
                if order["platform"] == "pc":
                    if ordertype  == 'sell' and order['order_type'] == 'sell':
                        offerData.append({'user': order['user']['ingame_name'], 'price': order['platinum']})
                    elif ordertype  == 'buy' and order['order_type'] == 'buy':
                        offerData.append({'user': order['user']['ingame_name'], 'price': order['platinum']})

        if ordertype == 'sell':
            offerData = sorted(offerData, key=lambda x: x['price'])
            for i in range(min(len(offerData), 3)):
                offer = offerData[i]
                print(f'/w {offer["user"]} Hi, I want to buy: "{orderitem}" for {offer["price"]} platinum. (warframe.market)')
        elif ordertype == 'buy':
            offerData = sorted(offerData, key=lambda x: x['price'], reverse=True)
            for i in range(min(len(offerData), 3)):
                offer = offerData[i]
                print(f'/w {offer["user"]} Hi, I want to sell: "{orderitem}" for {offer["price"]} platinum. (warframe.market)')
    else:
        print(f'Request failed with status code {response.status_code}')



if __name__ == "__main__":
    typeOrder="buy"
    choice="mirage_prime_systems"
    Price = GetOrderData(typeOrder, choice)