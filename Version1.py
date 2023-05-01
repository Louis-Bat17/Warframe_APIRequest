import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
import pyperclip

# TODO 
# - Secondary GUI with listed and double clickable item id's on market.
# - Add background image
# begin with sell, change option display instead of Seller to Sell, search engine
# lower case, exchange space with underscore

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
        
        self.groffitWindow = tk.Frame(master=master, width=600, height=300, bg="#273746")
        self.groffitWindow.pack(fill=tk.BOTH, expand=True)
      
        tk.Label(master=self.groffitWindow, text="Warframe Orders App", bg="#273746", fg="#FFFFFF").place(x=10,y=5)

        self.ordertype = tk.StringVar()
        self.buy_radio = tk.Radiobutton(master=self.groffitWindow, text="Sell", variable=self.ordertype, value="buy", bg="#273746", fg="#FFFFFF", selectcolor="#273746")
        self.buy_radio.place(x=10,y=25)

        self.sell_radio = tk.Radiobutton(master=self.groffitWindow, text="Buy", variable=self.ordertype, value="sell", bg="#273746", fg="#FFFFFF", selectcolor="#273746")
        self.sell_radio.place(x=60,y=25)

        self.dealsClear = tk.Button(master=self.groffitWindow, text="Clear Deals", command=self.clearDeals, bg="#17202A", fg="#FFFFFF")
        self.dealsClear.place(x=200,y=5)
        
        tk.Label(master=self.groffitWindow, text="Market Item:", bg="#273746", fg="#FFFFFF").place(x=10,y=50)
        self.marketSearch = tk.Entry(master=self.groffitWindow)
        self.marketSearch.pack()
        self.marketSearch.insert(0, "mirage_prime_systems")
        self.marketSearch.place(x=10,y=75)
        self.marketSearch.bind('<KeyRelease>', self.updateSuggested)

        self.filteroption = tk.StringVar()
        self.filteroption.set("")

        self.og_option = tk.StringVar()
        self.MarketItems = tk.OptionMenu(self.groffitWindow, self.og_option, *self.marketid.keys(), command=self.updateMarketSearch)
        self.MarketItems.place(x=350,y=70)
        self.og_option.set('Select an option')

        # Buttons for getting deals and opening warframe.market
        self.GetRequest = tk.Button(master=self.groffitWindow, text="Get Deals", command=self.submit, bg="#17202A", fg="#FFFFFF")
        self.GetRequest.place(x=350,y=110)

        self.openWarframeMarket = tk.Button(master=self.groffitWindow, text="Open Market", command=self.openMarket, bg="#17202A", fg="#FFFFFF")
        self.openWarframeMarket.place(x=490,y=110)

        tk.Label(master=self.groffitWindow, text="1st Deal", bg="#273746", fg="#FFFFFF").place(x=10,y=130)
        self.firstDeal = tk.Entry(master=self.groffitWindow, width=80)
        self.firstDeal.place(x=10,y=155)
        self.firstDeal.bind("<Double-Button-1>", self.copyDeal)
        
        tk.Label(master=self.groffitWindow, text="2nd Deal", bg="#273746", fg="#FFFFFF").place(x=10,y=180)
        self.secondDeal = tk.Entry(master=self.groffitWindow, width=80)
        self.secondDeal.place(x=10,y=205)
        self.secondDeal.bind("<Double-Button-1>", self.copyDeal)

        tk.Label(master=self.groffitWindow, text="3rd Deal", bg="#273746", fg="#FFFFFF").place(x=10,y=230)
        self.thirdDeal = tk.Entry(master=self.groffitWindow, width=80)
        self.thirdDeal.place(x=10,y=255)
        self.thirdDeal.bind("<Double-Button-1>", self.copyDeal)
        
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
        # self.marketSearch.delete(0, tk.END)
        self.firstDeal.delete(0, tk.END)
        self.secondDeal.delete(0, tk.END)
        self.thirdDeal.delete(0, tk.END)

    def updateSuggested(self, event=None):
        filter_text = self.marketSearch.get()
        filtered_items = [key for key in self.marketid.keys() if filter_text.lower() in key.lower()]       
        self.first_check = False
        
        if self.first_check == False: 
            self.first_check = True
            self.filteroption.set(filtered_items[0])
            self.suggestedItems = tk.OptionMenu(self.groffitWindow, self.filteroption, *filtered_items, command=self.updateMarketSearch)
            self.suggestedItems.place(x=10,y=100)                    
        else:
            if(len(filtered_items) > 0):
                self.filteroption.set(filtered_items[0])
                for newParts in filtered_items:
                    # Clear Set
                    self.suggestedItems['menu'].delete(0, 'end')
                    # Add new suggestions
                    self.suggestedItems['menu'].add_command(label=newParts, command=tk._setit(filtered_items[0], newParts))
            else:
                self.filteroption.set("No Match")       

    def updateMarketSearch(self, buttonPress):
        # Clear input field
        self.marketSearch.delete(0, tk.END)
        # Update input field
        self.marketSearch.insert(0, buttonPress)


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