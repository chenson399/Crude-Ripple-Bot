from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pylab as plt
import matplotlib.animation as animation
import numpy as np


binanceprice = []

binanceBrowser = webdriver.Chrome()
ethBrowser = webdriver.Chrome()


class binanceInstance:
    binanceBrowser.get('https://www.binance.com/login.html')
    loginemail = binanceBrowser.find_element_by_xpath('//*[@id="email"]')
    loginemail.click()
    loginemail.send_keys('chenson399@gmail.com')
    loginpass = binanceBrowser.find_element_by_xpath('//*[@id="pwd"]')
    loginpass.click()
    loginpass.send_keys('Mellophonia17')
    time.sleep(1)
    submit = binanceBrowser.find_element_by_xpath('//*[@id="login-btn"]')
    submit.click()
    time.sleep(10)
    binanceBrowser.get('https://www.binance.com/trade.html?symbol=TRX_ETH')


class ethInstance:
    ethBrowser.get("https://coinmarketcap.com/currencies/ethereum/")


global k
global i
k = 0
i = 0

largestprice = 0
smallestprice = 1
x = binanceBrowser.find_element_by_css_selector('body > div.main > div > div.kline-para > ul > li:nth-child(4) > strong')
low = x.text
y = binanceBrowser.find_element_by_css_selector('body > div.main > div > div.kline-para > ul > li:nth-child(3) > strong')
high = y.text

class binanceData:
    def binance(self):
        global largestprice
        global smallestprice
        global binprice
        content = binanceBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        binprice = soup.find("strong", {"ng-class":
                                            "{'green':currentProduct.close>trades[1].price,"
                                            "'magenta':currentProduct.close<trades[1].price}"}).text
        if binprice == low:
            smallestprice = binprice
            b.buy()
        if binprice == high:
            largestprice = binprice
            b.sell()

        content = ethBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        ethprice = soup.find("span", {"class": "text-large2"}).text
        ethprice = ethprice.strip('$')
        price1 = float(binprice) * float(ethprice)
        price1 = round(price1, 6)
        binanceprice.insert(k, price1)
        xar.insert(k, i)

    def buy(self):
        buyBox = binanceBrowser.find_element_by_xpath('//*[@id="buyQuanity"]')
        buyBox.click()
        buyBox.send_keys("1")
        buy = binanceBrowser.find_element_by_xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[2]/div[2]/div[3]/div[2]/div[1]/form/div[3]/input')
        buy.click()
        buyBox.clear()
        print("This is the smallest price", smallestprice)

    def sell(self):
        sellBox = binanceBrowser.find_element_by_xpath('//*[@id="sellQuanity"]')
        sellBox.click()
        sellBox.send_keys("1")
        sell = binanceBrowser.find_element_by_xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[2]/div[2]/div[3]/div[2]/div[2]/form/div[3]/input')
        sell.click()
        sellBox.clear()
        print("This is largest Price", largestprice)



fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

xar = []


class graph:
    def animate(self):
        x = np.array(xar)
        y = np.array(binanceprice)
        ax1.clear()
        ax1.plot(x, y)

b = binanceData()
c = graph()
ani = animation.FuncAnimation(fig, graph.animate)
try:
    while True:
        b.binance()
        c.animate()
        plt.show(block=False)
        plt.pause(1)
        k += 1
        i += 1

except KeyboardInterrupt:
    binanceBrowser.quit()
    ethBrowser.quit()

