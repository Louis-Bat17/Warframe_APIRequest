import tkinter as tk
import requests
import json
import pyperclip

class GenerateWindow:
    def __init__(self, master):
        self.master = master
        master.title("Warframe.Market Orders")
        
        canvas = tk.Canvas(master, width=400, height=300)
        canvas.pack()
        
        self.ordertype = tk.StringVar()
        buy_radio = tk.Radiobutton(canvas, text="Buy", variable=self.ordertype, value="buy")
        buy_radio.pack()
        sell_radio = tk.Radiobutton(canvas, text="Sell", variable=self.ordertype, value="sell")
        sell_radio.pack()
        
        tk.Label(canvas, text="Market Item:").pack()
        self.marketSearch = tk.Entry(canvas)
        self.marketSearch.pack()
        self.marketSearch.insert(0, "mirage_prime_systems")

        tk.Label(canvas, text="1st Deal").pack()
        self.firstDeal = tk.Entry(canvas)
        self.firstDeal.pack()
        
        tk.Label(canvas, text="2nd Deal").pack()
        self.secondDeal = tk.Entry(canvas)
        self.secondDeal.pack()

        tk.Label(canvas, text="3rd Deal").pack()
        self.thirdDeal = tk.Entry(canvas)
        self.thirdDeal.pack()
        
        self.GetRequest = tk.Button(canvas, text="Submit", command=self.submit)
        self.GetRequest.pack()
        
    def submit(self):
        clear = ""
        self.firstDeal.insert(0,clear )
        self.secondDeal.insert(0, clear)
        self.thirdDeal.insert(0, clear)
        self.getData()

    def getData(self):
        ordertype = self.ordertype.get()
        marketSearch = self.marketSearch.get()
        url = f'https://api.warframe.market/v1/items/{marketSearch}/orders?include=item'
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
                offer = offerData[0]
                offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                self.firstDeal.insert(0,offerstring )
                offer = offerData[1]
                offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                self.secondDeal.insert(0, offerstring)
                offer = offerData[2]
                offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                self.thirdDeal.insert(0, offerstring)
            elif ordertype == 'buy':
                offerData = sorted(offerData, key=lambda x: x['price'], reverse=True)
                offer = offerData[0]
                offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                self.firstDeal.insert(0,offerstring )
                offer = offerData[1]
                offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                self.secondDeal.insert(0, offerstring)
                offer = offerData[2]
                offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                self.thirdDeal.insert(0, offerstring)
            

if __name__ == "__main__":
    root = tk.Tk()
    gui = GenerateWindow(root)
    root.mainloop()
