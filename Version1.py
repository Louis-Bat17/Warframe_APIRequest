import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
import pyperclip

# TODO 
# - Secondary GUI with listed and double clickable item id's on market.
# - Look and Feel of GUI

class GenerateWindow:
    def __init__(self, master):
        # Before forming window, get all current id's
        url =  'https://api.warframe.market/v1/items'
        headers = {
            'accept': 'application/json',
            'Language': 'en'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.marketid = {}
            for itemData in data['payload']['items']:
                self.marketid[itemData['url_name']] = itemData['item_name']
        else:
            print(f'Request failed with status code {response.status_code}')

        self.master = master
        master.title("Warframe.Market Orders")
        
        groffitWindow = tk.Frame(master=master, width=600, height=300)
        groffitWindow.pack()
        
        tk.Label(master=groffitWindow, text="Warframe Orders App").place(x=10,y=5)

        self.ordertype = tk.StringVar()
        self.buy_radio = tk.Radiobutton(master=groffitWindow, text="Buy", variable=self.ordertype, value="buy")
        self.buy_radio.place(x=10,y=25)

        self.sell_radio = tk.Radiobutton(master=groffitWindow, text="Sell", variable=self.ordertype, value="sell")
        self.sell_radio.place(x=60,y=25)

        self.dealsClear = tk.Button(master=groffitWindow, text="Clear Deals", command=self.clearDeals)
        self.dealsClear.place(x=200,y=5)
        
        tk.Label(master=groffitWindow, text="Market Item:").place(x=10,y=50)
        # tk.Label(master=groffitWindow, text="Market Item:").pack()
        self.marketSearch = tk.Entry(master=groffitWindow)
        self.marketSearch.pack()
        self.marketSearch.insert(0, "mirage_prime_systems")
        self.marketSearch.place(x=10,y=75)

        tk.Label(master=groffitWindow, text="1st Deal").place(x=10,y=100)
        self.firstDeal = tk.Entry(master=groffitWindow, width=80)
        self.firstDeal.place(x=10,y=125)
        self.firstDeal.bind("<Double-Button-1>", self.copyDeal)
        
        tk.Label(master=groffitWindow, text="2nd Deal").place(x=10,y=150)
        self.secondDeal = tk.Entry(master=groffitWindow, width=80)
        self.secondDeal.place(x=10,y=175)
        self.secondDeal.bind("<Double-Button-1>", self.copyDeal)

        tk.Label(master=groffitWindow, text="3rd Deal").place(x=10,y=200)
        self.thirdDeal = tk.Entry(master=groffitWindow, width=80)
        self.thirdDeal.place(x=10,y=225)
        self.thirdDeal.bind("<Double-Button-1>", self.copyDeal)
        
        self.GetRequest = tk.Button(master=groffitWindow, text="Get Deals", command=self.submit)
        self.GetRequest.place(x=10,y=250)

        self.openWarframeMarket = tk.Button(master=groffitWindow, text="Open Market", command=self.openMarket)
        self.openWarframeMarket.place(x=100,y=250)
        
    def submit(self):
        self.clearDeals()
        self.getData()

    def copyDeal(self, buttonPress):
            getDeal = buttonPress.widget
            dealString = getDeal.get()
            pyperclip.copy(dealString)
            messagebox.showinfo("Deal Copied!", f"Deal Information Copied!.\n {dealString}")

    def clearDeals(self):
        clear = ""
        self.firstDeal.delete(0, tk.END)
        self.secondDeal.delete(0, tk.END)
        self.thirdDeal.delete(0, tk.END)

    def getData(self):
        ordertype = self.ordertype.get()
        item_id = self.marketSearch.get()
        marketSearch = self.marketid[item_id]
        url = f'https://api.warframe.market/v1/items/{item_id}/orders?include=item'
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
            noDealDat="No Deal Found."
            if ordertype == 'sell':
                offerData = sorted(offerData, key=lambda x: x['price'])
                if len(offerData) > 1:
                    offer = offerData[0]
                    offerstring = f'/w {offer["user"]} Hi, I want to buy: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                    self.firstDeal.insert(0,offerstring )
                    if len(offerData) >= 2:  
                        offer = offerData[1]
                        offerstring = f'/w {offer["user"]} Hi, I want to buy: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                        self.secondDeal.insert(0, offerstring)
                        if len(offerData) >= 3: 
                            offer = offerData[2]
                            offerstring = f'/w {offer["user"]} Hi, I want to buy: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                            self.thirdDeal.insert(0, offerstring)
                        else:
                            self.thirdDeal.insert(0, noDealDat)
                    else:
                        self.secondDeal.insert(0, noDealDat)
                        self.thirdDeal.insert(0, noDealDat)
                else:
                    messagebox.showerror("Whoops Tenno!", "No Deals Available!")
            elif ordertype == 'buy':
                offerData = sorted(offerData, key=lambda x: x['price'], reverse=True)
                if len(offerData) >= 1:
                    offer = offerData[0]
                    offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                    self.firstDeal.insert(0,offerstring )
                    if len(offerData) >= 2:  
                        offer = offerData[1]
                        offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                        self.secondDeal.insert(0, offerstring)
                        if len(offerData) >= 3:  
                            offer = offerData[2]
                            offerstring = f'/w {offer["user"]} Hi, I want to sell: "{marketSearch}" for {offer["price"]} platinum. (warframe.market)'
                            self.thirdDeal.insert(0, offerstring)
                        else:
                            self.thirdDeal.insert(0, noDealDat)
                    else:
                        self.secondDeal.insert(0, noDealDat)
                        self.thirdDeal.insert(0, noDealDat)
                else:
                    messagebox.showerror("Whoops Tenno!", "No Deals Available!")
            
    def openMarket(self):
        webbrowser.open(f"https://warframe.market/items/{self.marketSearch.get()}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = GenerateWindow(root)
    root.mainloop()