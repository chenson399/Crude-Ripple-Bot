from selenium import webdriver
from bs4 import BeautifulSoup
import time

binanceBrowser = webdriver.Chrome()

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
    time.sleep(2)


global highthresh
global lowthresh
lowthresh = 0
highthresh = 0

class math:
    def highandlow(self):
        x = binanceBrowser.find_element_by_css_selector(
            'body > div.main > div > div.kline-para > ul > li:nth-child(4) > strong')
        low = x.text
        y = binanceBrowser.find_element_by_css_selector(
            'body > div.main > div > div.kline-para > ul > li:nth-child(3) > strong')
        high = y.text
        midavg = (float(high) + float(low)) / 2
        highthresh = (float(high) + midavg) / 2
        lowthresh = (midavg + float(low)) / 2


class binanceData:
    def binance(self):
        global binprice

        content = binanceBrowser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        binprice = soup.find("strong", {"ng-class":
                                            "{'green':currentProduct.close>trades[1].price,"
                                            "'magenta':currentProduct.close<trades[1].price}"}).text

    def buy(self):

        k = 1
        buyBox = binanceBrowser.find_element_by_xpath('//*[@id="buyQuanity"]')
        buyBox.click()
        buyBox.send_keys("1")
        buy = binanceBrowser.find_element_by_xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[2]/div[2]/div[3]/div[2]/div[1]/form/div[3]/input')
        buy.click()
        buyBox.clear()
        print('Ive bought this many TRX:', k)
        k += 1

    def sell(self):
        k = 1
        sellBox = binanceBrowser.find_element_by_xpath('//*[@id="sellQuanity"]')
        sellBox.click()
        sellBox.send_keys("1")
        sell = binanceBrowser.find_element_by_xpath(
            '//*[@id="ng-app"]/body/div[4]/div/div[2]/div[2]/div[3]/div[2]/div[2]/form/div[3]/input')
        sell.click()
        sellBox.clear()
        print("Ive sold this many TRX", k)
        k += 1


b = binanceData()
m = math()
lastprice = 0
while True:
    m.highandlow()
    b.binance()
    #This works to check if the price has moved or not
    if binprice != lastprice:
        print(lastprice)
        lastprice = binprice
        #dont buy if price has went up
        if (float(binprice)) <= lowthresh:
            print('low')
            if binprice < lastprice:
                b.buy()
            elif binprice > lastprice:
                print('The price went up')
                b.binance()
        #Dont sell if price has went down
        if (float(binprice)) >= highthresh:
            print('high')
            if binprice > lastprice:
                b.sell()
            elif binprice <lastprice:
                print('The price went down!')
                b.binance()
    elif binprice == lastprice:
        print('Price is same')
        time.sleep(2)
        b.binance()

