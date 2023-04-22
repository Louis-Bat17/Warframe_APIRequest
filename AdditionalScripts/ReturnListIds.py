import requests

url =  'https://api.warframe.market/v1/items'
headers = {
    'accept': 'application/json',
    'Language': 'en'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    fullList = {}
    for itemData in data['payload']['items']:
        PartName=itemData['item_name']
        PartID=itemData['url_name']
        fullList[PartID] = PartName
    print(fullList["crash_course"])
else:
    print(f'Request failed with status code {response.status_code}')