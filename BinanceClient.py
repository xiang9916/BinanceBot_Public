from BinanceKey import API_KEY, SECRET_KEY
from BinanceTools import *

import requests
import time
from urllib.parse import urljoin

requests.packages.urllib3.disable_warnings()

BASE_URL = 'https://api.binance.com'
FAPI_URL = 'https://fapi.binance.com'
DAPI_URL = 'https://dapi.binance.com'

headers = {
    'X-MBX-APIKEY': API_KEY
}

def add(dict, params_dict):
    for param_name in params_dict:
        if params_dict[param_name] is not None:
            dict[param_name] = params_dict[param_name]
    return dict


# 函数编写示例
'''
    #           【API 官方介绍】
    def 【名称】(self, 【参数】):
        while 1:
            PATH = 【路径】
            params = {
                【必要参数】
            }
            add(params, params_dict)

            params['timestamp'] = timeStamp() 【时间戳】
            params['signature'] = sign(params, SECRET_KEY) 【签名】
            url = urljoin(【API类型】, PATH)
            r = requests.【请求方式】(url, headers=headers, params=params)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print(【API 官方介绍】)
                jsonprint(【参数】)
                jsonprint(r.json())
                time.sleep(10)
'''


class Client:
    def __init__(self) -> None:
        return

    #   执行任意交互
    def do(self, command = "GET /sapi/v1/accountSnapshot (HMAC SHA256)", params = {"type": "SPOT", "timestamp": True}):
        commands = command.split(' ', 2)
        PATH = commands[1]
        api = PATH[1:].split('/')[0]

        if api == 'sapi' or api == 'api': URL = BASE_URL
        if api == 'dapi': URL = DAPI_URL

        while 1:
            PATH = commands[1]
            if params["timestamp"] == True: params["timestamp"] = timeStamp()
            if commands[2] == '(HMAC SHA256)': params['signature'] = sign(params, SECRET_KEY)
            url = urljoin(URL, PATH)

            if commands[0] == 'GET':    r = requests.get(url, headers=headers, params=params, verify=False)
            if commands[0] == 'POST':   r = requests.post(url, headers=headers, params=params)
            if commands[0] == 'DELETE': r = requests.delete(url, headers=headers, params=params)

            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('POST /dapi/v1/order (HMAC SHA256)')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #   现货/杠杆/币安宝/矿池
    #       行情接口
    #           获取服务器时间 GET /api/v3/time
    def getTime(self):
        while 1:
            PATH = '/api/v3/time'
            params = {}
            url = urljoin(BASE_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /api/v3/time')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           K线数据 GET /api/v3/klines
    def getKlines(self, symbol = 'ETHUSDT', interval = '', limit = 1000):
        while 1:
            PATH = '/api/v3/klines'
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            url = urljoin(BASE_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /api/v3/klines')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           当前平均价格 GET /api/v3/avgPrice
    def getAvgPrice(self, symbol = 'ETHUSDT'):
        while 1:
            PATH = '/api/v3/avgPrice'
            params = {
                'symbol': symbol
            }
            url = urljoin(BASE_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /api/v3/avgPrice')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           24hr价格变动情况 GET /api/v3/ticker/24hr
    def getTicker24hr(self, symbol = 'ETHUSDT'):
        while 1:
            PATH = '/api/v3/ticker/24hr'
            params = {
                'symbol': symbol
            }
            url = urljoin(BASE_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /api/v3/ticker/24hr')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           最新价格 GET /api/v3/ticker/price
    def getTickerPrice(self, symbol = None):
        while 1:
            PATH = '/api/v3/ticker/price'
            params = {}
            if not(symbol is None): params['symbol'] = symbol

            url = urljoin(BASE_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /api/v3/ticker/price')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

#       账户和交易接口
    #           下单 POST /api/v3/order (HMAC SHA256)
    def postOrder(self, symbol, side, type, positionSide=None, reduceOnly=None, quantity=None, price=None, newClientOrderId=None, stopPrice=None, activationPrice=None, callbackRate=None, timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None, recvWindow=None):
        while 1:
            PATH = '/api/v3/order'
            params = {
                'symbol': symbol,
                'side': side,
                'type': type
            }
            add(params, {'positionSide': positionSide, 'reduceOnly': reduceOnly, 'quantity': quantity, 'price': price, 'newClientOrderId': newClientOrderId, 'stopPrice': stopPrice, 'activationPrice': activationPrice, 'callbackRate': callbackRate, 'timeInForce': timeInForce, 'workingType': workingType, 'priceProtect': priceProtect, 'newOrderRespType': newOrderRespType, 'recvWindow': newOrderRespType})

            params['timestamp'] = timeStamp()
            params['signature'] = sign(params, SECRET_KEY)
            url = urljoin(BASE_URL, PATH)
            r = requests.post(url, headers=headers, params=params)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('POST /api/v3/order (HMAC SHA256)')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #   U本位合约接口
    #       行情接口
    #           获取交易规则和交易对 GET /fapi/v1/exchangeInfo
    def getFExchangeInfo(self):
        while 1:
            PATH = '/fapi/v1/exchangeInfo'
            params = {}
            url = urljoin(FAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /fapi/v1/exchangeInfo')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           最新标记价格和资金费率 GET /fapi/v1/premiumIndex
    def getFPremiumIndex(self, symbol = None):
        while 1:
            PATH = '/fapi/v1/premiumIndex'
            params = {}
            if not(symbol is None): params['symbol'] = symbol
            
            url = urljoin(FAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /fapi/v1/premiumIndex')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           最新价格 GET /fapi/v1/ticker/price
    def getFTickerPrice(self, symbol = None):
        while 1:
            PATH = '/fapi/v1/ticker/price'
            params = {}
            if not(symbol is None): params['symbol'] = symbol

            url = urljoin(FAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                if type(r.json) == list:
                    return sorted(r.json(), key=lambda symbol: symbol['symbol'])
                else:
                    return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /fapi/v1/ticker/price')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #       账户和交易接口
    #           下单 POST /fapi/v1/order (HMAC SHA256)
    def postFOrder(self, symbol, side, type, positionSide=None, reduceOnly=None, quantity=None, price=None, newClientOrderId=None, stopPrice=None, activationPrice=None, callbackRate=None, timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None, recvWindow=None):
        while 1:
            PATH = '/fapi/v1/order'
            params = {
                'symbol': symbol,
                'side': side,
                'type': type
            }
            add(params, {'positionSide': positionSide, 'reduceOnly': reduceOnly, 'quantity': quantity, 'price': price, 'newClientOrderId': newClientOrderId, 'stopPrice': stopPrice, 'activationPrice': activationPrice, 'callbackRate': callbackRate, 'timeInForce': timeInForce, 'workingType': workingType, 'priceProtect': priceProtect, 'newOrderRespType': newOrderRespType, 'recvWindow': newOrderRespType})

            params['timestamp'] = timeStamp()
            params['signature'] = sign(params, SECRET_KEY)
            url = urljoin(FAPI_URL, PATH)
            r = requests.post(url, headers=headers, params=params)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('POST /fapi/v1/order (HMAC SHA256)')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #   币本位合约接口
    #       行情接口
    #           获取服务器时间 GET /dapi/v1/time
    def getDTime(self):
        while 1:
            PATH = '/dapi/v1/time'
            params = {}
            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/time')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           获取交易规则和交易对 GET /dapi/v1/exchangeInfo
    def getDExchangeInfo(self):
        while 1:
            PATH = '/dapi/v1/exchangeInfo'
            params = {}
            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/exchangeInfo')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           最新现货指数价格和Mark Price GET /dapi/v1/premiumIndex
    def getDPremiumIndex(self, symbol = None):
        while 1:
            PATH = '/dapi/v1/premiumIndex'
            params = add({}, {'symbol': symbol})

            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/premiumIndex')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           查询永续合约资金费率历史 GET /dapi/v1/fundingRate
    def getDFundingRate(self, symbol, startTime = None, endTime = None, limit = 1000):
        while 1:
            PATH = '/dapi/v1/fundingRate'
            params = {
                'symbol': symbol
            }
            add(params, {'startTime': startTime, 'endTime': endTime, 'limit': limit})

            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/fundingRate')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           K线数据 GET /dapi/v1/klines
    def getDKlines(self, symbol, interval, startTime = None, endTime = None, limit = 1500):
        while 1:
            PATH = '/dapi/v1/klines'
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/klines')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           24hr价格变动情况 GET /dapi/v1/ticker/24hr
    def getDTicker24hr(self, symbol = 'ETHUSD_PERP'):
        while 1:
            PATH = '/dapi/v1/ticker/24hr'
            params = {
                'symbol': symbol
            }
            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/ticker/24hr')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           最新价格 GET /dapi/v1/ticker/price
    def getDTickerPrice(self, symbol = None):
        while 1:
            PATH = '/dapi/v1/ticker/price'
            params = {}
            if not(symbol is None): params['symbol'] = symbol

            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return sorted(r.json(), key=lambda symbol: symbol['symbol'])
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/ticker/price')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #       账户和交易接口
    #           下单 POST /dapi/v1/order (HMAC SHA256)
    def postDOrder(self, symbol, side, type, positionSide=None, reduceOnly=None, quantity=None, price=None, newClientOrderId=None, stopPrice=None, activationPrice=None, callbackRate=None, timeInForce=None, workingType=None, priceProtect=None, newOrderRespType=None, recvWindow=None):
        while 1:
            PATH = '/dapi/v1/order'
            params = {
                'symbol': symbol,
                'side': side,
                'type': type
            }
            add(params, {'positionSide': positionSide, 'reduceOnly': reduceOnly, 'quantity': quantity, 'price': price, 'newClientOrderId': newClientOrderId, 'stopPrice': stopPrice, 'activationPrice': activationPrice, 'callbackRate': callbackRate, 'timeInForce': timeInForce, 'workingType': workingType, 'priceProtect': priceProtect, 'newOrderRespType': newOrderRespType, 'recvWindow': newOrderRespType})

            params['timestamp'] = timeStamp()
            params['signature'] = sign(params, SECRET_KEY)
            url = urljoin(DAPI_URL, PATH)
            r = requests.post(url, headers=headers, params=params)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('POST /dapi/v1/order (HMAC SHA256)')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           查询订单 GET /dapi/v1/order (HMAC SHA256)
    def getDOrder(self, symbol = 'ETHUSD_PERP', orderId = None, origClientOrderId = None):
        while 1:
            PATH = '/dapi/v1/order'
            params = {
                'symbol': symbol
            }

            if not(orderId is None): params['orderId'] = orderId
            if not(origClientOrderId is None): params['origClientOrderId'] = origClientOrderId

            params['timestamp'] = timeStamp()
            params['recvWindow']= 10000
            params['signature'] = sign(params, SECRET_KEY)
            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/order (HMAC SHA256)')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           批量撤销订单 DELETE /dapi/v1/allOpenOrders (HMAC SHA256)
    def deleteAllOpenOrders(self, symbol = 'ETHUSD_PERP'):
        while 1:
            PATH = '/dapi/v1/allOpenOrders'
            params = {
                'symbol': symbol
            }
            params['timestamp'] = timeStamp()
            params['signature'] = sign(params, SECRET_KEY)
            url = urljoin(DAPI_URL, PATH)
            r = requests.delete(url, headers=headers, params=params)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('DELETE /dapi/v1/allOpenOrders (HMAC SHA256)')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           账户信息 GET /dapi/v1/account (HMAC SHA256)
    def getDAccount(self):
        while 1:
            PATH = '/dapi/v1/account'
            params = {}
            params['timestamp'] = timeStamp()
            params['signature'] = sign(params, SECRET_KEY)
            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/account (HMAC SHA256)')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)

    #           账户成交历史 GET /dapi/v1/userTrades (HMAC SHA256)
    def getDUserTrades(self, symbol = 'ETHUSD_PERP', limit = None):
        while 1:
            PATH = '/dapi/v1/userTrades'
            params = {
                'symbol': symbol
            }

            if not(limit is None): params['limit'] = limit

            params['timestamp'] = timeStamp()
            params['signature'] = sign(params, SECRET_KEY)
            url = urljoin(DAPI_URL, PATH)
            r = requests.get(url, headers=headers, params=params, verify=False)
            if r.status_code == 200:
                return r.json()
            else:
                print()
                print('ERROR', r)
                print('GET /dapi/v1/userTrades (HMAC SHA256)')
                jsonprint(params)
                jsonprint(r.json())
                time.sleep(10)