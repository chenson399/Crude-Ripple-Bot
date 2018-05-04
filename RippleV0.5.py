from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np

binanceprice = []
bitstampprice = []
krakenprice = []
exmoprice = []
coinmarketcapprice = []

binanceBrowser = webdriver.Chrome()
ethBrowser = webdriver.Chrome()
bitstampBrowser = webdriver.Chrome()
krakenBrowser = webdriver.Chrome()
exmoBrowser = webdriver.Chrome()
cmcBrowser = webdriver.Chrome()

class binanceInstance:
    binanceBrowser.get('https://www.binance.com/trade.html?symbol=XRP_ETH')

class ethInstance:
    ethBrowser.get("https://coinmarketcap.com/currencies/ethereum/")

class bitstampInstance:
    bitstampBrowser.get('https://www.bitstamp.net')
    bitstampBrowser.find_element_by_xpath('//*[@id="overview-pairs"]/li[4]/a').click()

class krakenInstance:
    krakenBrowser.get('https://www.kraken.com/charts')
    time.sleep(1)
    krakenBrowser.find_element_by_xpath('//*[@id="pairselect-button"]').click()
    wait = WebDriverWait(krakenBrowser, .5)
    actions = ActionChains(krakenBrowser)
    xrpusd = krakenBrowser.find_element_by_xpath('//*[@id="topside"]/div[2]/div/div/div/div[1]/ul/li[19]/a')
    actions.move_to_element(xrpusd).perform()
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="topside"]/div[2]/div/div/div/div[1]/ul/li[19]/ul/li[4]/a'))).click()

class exmoInstance:
    exmoBrowser.get('https://exmo.com/en/trade#?pair=XRP_USD')

class cmcInstance:
    cmcBrowser.get('https://coinmarketcap.com/currencies/ripple/')

class gatherData:

    def binance(self):
        x = 0
        content = binanceBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        binprice = soup.find("strong", {"ng-class":
                                            "{'green':currentProduct.close>trades[1].price,"
                                            "'magenta':currentProduct.close<trades[1].price}"}).text
        content = ethBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        ethprice = soup.find("span", {"class": "text-large2"}).text
        ethprice = ethprice.strip('$')
        price1 = float(binprice) * float(ethprice)
        price1 = round(price1, 6)
        binanceprice.insert(x, price1)
        x += 1

    def bitstamp(self):
        x = 0
        content = bitstampBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        price2 = soup.find("span", {'id': 'ticker-price'}).text
        bitstampprice.insert(x, price2)
        x += 1

    def kraken(self):
        x = 0
        content = krakenBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        price3 = soup.find("div", {'class': 'val mono'}).text
        price3 = price3.strip('$')
        krakenprice.insert(x, price3)
        x += 1

    def exmo(self):
        x = 0
        content = exmoBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        price4 = soup.find("td", {'class': 'tcol_price ng-binding'}).text
        exmoprice.insert(x, price4)
        x += 1

    def coinmarketcap(self):
        x = 0
        content = cmcBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        price5 = soup.find("span", {'class': 'text-large2'}).text
        price5 = price5.strip('$')
        coinmarketcapprice.insert(x, price5)
        x += 1


call = gatherData()

class rundata:

    for i in range(1, 6):
        print(i)
        call.binance()
        call.bitstamp()
        call.kraken()
        call.exmo()
        call.coinmarketcap()
        if i % 5 == 0:
            cmcBrowser.refresh()
            ethBrowser.refresh()
        time.sleep(8)

    binanceBrowser.quit()
    ethBrowser.quit()
    bitstampBrowser.quit()
    krakenBrowser.quit()
    exmoBrowser.quit()
    cmcBrowser.quit()

class graph():
    bintrace = go.Scatter(
        y=binanceprice,
        name='Current Binance Prices',
        line=dict(
            color='rgb(57, 106, 177)',
            width=4
        )
    )
    bittrace = go.Scatter(
        y=bitstampprice,
        name='Current Bitstamp Price',
        line=dict(
            color='rgb(218, 124, 48)',
            width=4
        )
    )
    krakentrace = go.Scatter(
        y=krakenprice,
        name='Current Kraken Prices',
        line=dict(
            color='rgb(62, 150, 81)',
            width=4
        )
    )
    exmotrace = go.Scatter(
        y=exmoprice,
        name='Current Exmo Prices',
        line=dict(
            color='rgb(204, 37, 41)',
            width=4
        )
    )
    cointrace = go.Scatter(
        y=coinmarketcapprice,
        name='Current CoinMarketCap Prices',
        line=dict(
            color='rgb(107, 76, 154)',
            width=4
        )
    )
    dt = time.strftime("%m-%d-%y  %I %M %S %p")
    html = '.html'
    htmlname = str(dt) + html
    data = [bintrace, bittrace, krakentrace, exmotrace, cointrace]
    layout = dict(title='Current Price of Ripple',
                  yaxis=dict(title='Price'))
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename=htmlname)


class excel:
    dt = time.strftime("%m-%d-%y  %I %M %S %p")
    csvexs = '.csv'
    filename = dt + csvexs
    df = pd.DataFrame(np.column_stack([binanceprice, bitstampprice, krakenprice, exmoprice, coinmarketcapprice])
                      , columns=["Binance", "Bitstamp", "Kraken", "Exmo", "CMC"])
    df.to_csv(filename, index=False)


binanceInstance()
ethInstance()
bitstampInstance()
krakenInstance()
exmoInstance()
cmcInstance()
try:
    rundata()
except:
    graph()
    excel()
    print('An error occurred')
    binanceBrowser.quit()
    ethBrowser.quit()
    bitstampBrowser.quit()
    krakenBrowser.quit()
    exmoBrowser.quit()
    cmcBrowser.quit()

graph()
excel()
