import csv
import requests

# Before forming window, get all current id's
url =  'https://api.warframe.market/v1/items'
headers = {
    'accept': 'application/json',
    'Language': 'en'
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    marketid = {}
    for itemData in data['payload']['items']:
        marketid[itemData['url_name']] = itemData['item_name']
else:
    print(f'Request failed with status code {response.status_code}')

with open('idList.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for key, value in marketid.items():
        writer.writerow([key, value])