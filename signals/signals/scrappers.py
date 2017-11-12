import json
import requests
import xmltodict
from bs4 import BeautifulSoup
import time


from threading import Thread
from concurrent.futures import Future

def call_with_future(fn, future, args, kwargs):
    try:
        result = fn(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)

def threaded(fn):
    def wrapper(*args, **kwargs):
        future = Future()
        Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future
    return wrapper

class APISignals(object):

    MOEDA=""
    RESULTS={}
    SERVICES = {
        "vicentra": {
            "URL": "http://vicetra.com/android/technicalForex/getData.php?symbol=%s&indi=300&lang=en",
            "HEADERS": {
                "Host": "vicetra.com",
                "Connection": "Keep - Alive",
                "User - Agent": "Apache - HttpClient / UNAVAILABLE(java 1.4)"
            }
        },
        "clawshorns": {
            "URL": "http://api.clawshorns.com/signals?token=f984357eab59537962aab2cc190a7fe3&lang=pt",
            "HEADERS": {
                "Host": "api.clawshorns.com",
                "Connection": "Keep-Alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
                "Accept-Encoding": "gzip"
            }
        },
        "investingcom": {
            "URL": "https://ssltsw.forexprostools.com/index.php?timeframe=300&lang=1&forex=1,2,3,5,7,9,10&commodities=8830,8836,8831,8849,8833,8862,8832&indices=175,166,172,27,167,179,168&stocks=334,345,346,347,348,349,350&tabs=1,2,3,4&amp;forex=1,2,3,5,7,9,10&amp;commodities=8830,8836,8831,8849,8833,8862,8832&amp;indices=175,166,172,27,167,179,168&amp;stocks=334,345,346,347,348,349,350&amp;tabs=1,2,3,4%20&referer=https://ssltsw.forexprostools.com/?lang=1%20&selectedTabId=QBS_1",
            "HEADERS": {
                "Accept": "text/html, */*; q=0.01",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.8,pt;q=0.6",
                "Cookie": "geoC=BR"
            }
        }
    }

    def run(self):
        RESULTS = {}
        RESULTS["investingcom"]=self.investingcom().result()
        RESULTS["clawshorns"] = self.clawshorns().result()
        RESULTS["vicentra"] = self.vicentra().result()
        return RESULTS


    def process(self,signals,force=True):
        buy = 0
        sale = 0
        neutro = 0
        try:
            if signals["investingcom"]['movimento'] == 'Strong Buy' or (
                    signals["investingcom"]['movimento'] == 'Buy' and force):
                buy += 1
            elif signals["investingcom"]['movimento'] == 'Strong Sell' or (
                    signals["investingcom"]['movimento'] == 'Sell' and force):
                sale += 1
            else:
                neutro += 1
        except:
            pass

        try:
            if signals["clawshorns"]['movimento'] == 'Comprar' or (
                    signals["clawshorns"]['movimento'] == 'Comprar ativo' and force):
                buy += 1
            elif signals["clawshorns"]['movimento'] == 'Vender' or (
                    signals["clawshorns"]['movimento'] == 'Vender ativo' and force):
                sale += 1
            else:
                neutro += 1
        except:
            pass

        try:
            if signals["vicentra"]['movimento'] == 'Strong Buy' or (
                    signals["vicentra"]['movimento'] == 'Buy' and force):
                buy += 1
            elif signals["vicentra"]['movimento'] == 'Strong Sell' or (
                    signals["vicentra"]['movimento'] == 'Sell' and force):
                sale += 1
            else:
                neutro += 1
        except:
            pass

        buy = round((100/3)*buy,0)
        sale = round((100/3)*sale,0)
        neutro = round((100/3)*neutro,0)

        return signals,buy,sale,neutro

    def __init__(self,moeda):
        self.RESULTS = {}
        self.MOEDA = moeda

    @threaded
    def investingcom(self):
        '''
        :param moeda: EUR/USD | GBP/USD | USD/JPY | AUD/USD | USD/CAD | EUR/JPY | EUR/CHF
        :return:
        '''
        response = requests.get(self.SERVICES['investingcom']['URL'], headers=self.SERVICES['investingcom']['HEADERS'])
        soup = BeautifulSoup(response.text, 'html.parser')
        result = {}
        for tr in soup.findAll('tr'):
            if(tr.findAll("td")[2]["title"]==self.MOEDA):
                result["moeda"] = tr.findAll("td")[2]["title"]
                result["movimento"] = tr.findAll("td")[4].text
                result["valor"] = tr.findAll("td")[3].text
                break
        return result

    @threaded
    def clawshorns(self):
        '''

        :return:
        '''
        URL = self.SERVICES['clawshorns']['URL']
        HEADERS = self.SERVICES['clawshorns']['HEADERS']
        t = requests.get(URL, headers=HEADERS)
        res = xmltodict.parse(t.text)
        res = res['root']['items']['entry']
        res = [x for x in res if x['group_name'] == 'M5' and x['pair_'] == self.MOEDA]
        result = {}
        for i in res:
            result["moeda"] = i["pair_"]
            result["intervalo"] = i["group_name"].replace("M", "")
            result["movimento"] = i['recommendation_text']
            result["data"] = i["pair_"]
            result["ma10"] = i["ma10"]
            result["ma20"] = i["ma20"]
            result["ma50"] = i["ma50"]
            result["ma100"] = i["ma100"]
            result["macd"] = i["macd"]
            result["bbands"] = i["bbands"]
            result["ichimoku"] = i["ichimoku"]
            result["stochastic"] = i["stochastic"]
            result["williams"] = i["williams"]
            result["zigzag"] = i["zigzag"]
            break
        return result

    @threaded
    def vicentra(self):
        moeda = (self.MOEDA.replace("/","-")+("-technical")).lower()
        def getSymbol(moeda):
            # print(moeda)
            URL = self.SERVICES['vicentra']['URL'] % (moeda)
            HEADERS = self.SERVICES['vicentra']['HEADERS']
            t = requests.get(URL, headers=HEADERS)
            res = t.json()['data']
            result = {}
            result["moeda"] = self.MOEDA
            for i in res:
                try:
                    result[i['sembol']]={}
                    result[i['sembol']]["Movimento"] = i['iki']
                    result[i['sembol']]["Valor"] = i['bir']
                except KeyError:
                    result["movimento"] = i['durum']
                    result["Compra"] = i['buy']
                    result["Venda"] = i['sell']
                    result["Data"] = i["zaman"]
                    result["Preço"] = i["fiyat"]
            return result

        def getAll():
            URL = "http://vicetra.com/android/technicalForex/getData.php?list=300&lang=en"

            HEADERS = {
                "Host": "vicetra.com",
                "Connection": "Keep - Alive",
                "User - Agent": "Apache - HttpClient / UNAVAILABLE(java 1.4)"
            }
            t = requests.get(URL, headers=HEADERS)
            print("getAll: ")
            for i in t.json()['data']:
                print("==============================")
                print("Moeda", i['sembol'])
                print("Movimento", i['durum'])
                print("Data", i['zaman'])
                print("%", i['yuzde'])
                print("Preço", i['fiyat'])
                print("Diferença", i['fark'])
                print("Key", i['value'])
        return getSymbol(moeda)