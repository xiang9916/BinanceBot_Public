from BinanceClient import Client
from BinanceIndicators import VWAP
from BinanceTools import candles_decimal, proxy

import threading
import time
from decimal import *
from math import floor

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_EVEN
# proxy()
Client = Client()

qty = 12
tier = 2

while 1:
    if Client.getTickerPrice(symbol='BUSDUSDT')['price'] == '1.00000000':
        print(Client.getTickerPrice(symbol='BUSDUSDT'))
        Client.deleteOpenOrders(symbol='BUSDUSDT')
        break

OrderIDs = [0] * (2 * tier)
Orderstatus = [0] * (2 * tier)
for i in range(1, tier+1):
    OrderIDs[tier-i] = Client.postOrder(symbol='BUSDUSDT', side='BUY', type='LIMIT', timeInForce='GTC', quantity=qty, price=1-i*0.0001)["orderId"]
for i in range(1, tier+1):
    OrderIDs[tier+i-1] = Client.postOrder(symbol='BUSDUSDT', side='SELL', type='LIMIT', timeInForce='GTC', quantity=qty, price=1+i*0.0001)["orderId"]
Orderstatus = ([1] * tier) + ([-1] * tier)

while 1:
    for i in range(2 * tier):
        res = Client.getOrder(symbol='BUSDUSDT', orderId=str(OrderIDs[i])) # FILLED
        if res["status"] == 'FILLED':
            if res['side'] == 'BUY':
                p = float(res['price']) + 0.0001
                OrderIDs[i] = Client.postOrderClient.postOrder(symbol='BUSDUSDT', side='SELL', type='LIMIT', timeInForce='GTC', quantity=qty, price=p)["orderId"]
            elif res['side'] == 'SELL':
                p = float(res['price']) - 0.0001
                OrderIDs[i] = Client.postOrderClient.postOrder(symbol='BUSDUSDT', side='BUY', type='LIMIT', timeInForce='GTC', quantity=qty, price=p)["orderId"]
            
            