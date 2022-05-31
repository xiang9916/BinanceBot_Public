from BinanceClient import Client
from BinanceIndicators import VWAP
from BinanceTools import candles_decimal, proxy

import threading
import time
from decimal import *
from math import floor

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_EVEN
proxy()
Client = Client()

class PostOrder(threading.Thread):
    def __init__(self, API, params):
        threading.Thread.__init__(self)
        self.API = API
        self.params = params

    def run(self):
        self.post()
    
    def post(self):
        if self.API == 'BASE': Client.postOrder(**self.params)
        if self.API == 'D':    Client.postDOrder(**self.params)
        if self.API == 'F':    Client.postFOrder(**self.params)
        return

def hedge_order(symbols=('Long', 'Short'), side=('BUY', 'SELL'), API=('D','D'), quantity=0):
    if quantity < 0:
        side = (side[1], side[0])
        quantity *= -1

    for i in range(quantity):
        params1 = {'symbol': symbols[0], 'side': side[0], 'type': 'MARKET','quantity': 1}
        thread1 = PostOrder(API[0], params1)
        params2 = {'symbol': symbols[1], 'side': side[1], 'type': 'MARKET','quantity': 1}
        thread2 = PostOrder(API[1], params2)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        print('end-{}'.format(i))
        time.sleep(2)


if __name__ == '__main__':
    hedge_order(
        symbols=('ETHUSD_220624', 'ETHUSD_PERP'),
        side=('BUY', 'SELL'),
        API=('D', 'D'),
        quantity=10
    )