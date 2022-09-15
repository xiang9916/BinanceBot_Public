from BinanceClient import Client
from BinanceIndicators import VWAP
from BinanceTools import candles_decimal, proxy

import datetime
import numpy as np
import threading
import time
from decimal import *
from guppy import hpy; guppy_hpy=hpy() # guppy3
from math import floor

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_EVEN
proxy()
Client = Client()

def arbitrage():
    print('套利提示')
    spot_price_list = Client.getTickerPrice()
    spot_prices= {}
    for item in spot_price_list:
        spot_prices[item['symbol']] = item['price']
    res = arbitrageD(spot_prices)
    res.update(arbitrageF(spot_prices))
    sorted_res = {}
    for i in sorted(res):
        sorted_res[i] = res[i]
    
    last_asset = None
    for i in sorted_res:
        label = i.split('_')
        if label[0] != last_asset:
            print(last_asset := label[0])
        
        if label[1] == 'PERP':
            if label[2] == 'D':
                print('\033[0;33m标的 {}\t\t\t\t资金费率 {}%\t\t\t做多 APR {:+}%\033[0m'.format(*sorted_res[i]))
            elif label[2] == 'F':
                print('\033[0;36m标的 {}\t\t\t\t资金费率 {}%\t\t\t做多 APR {:+}%\033[0m'.format(*sorted_res[i]))
        else:
            if label[2] == 'D':
                print('\033[0;33m标的 {}\t到期日 {}\t贴水 {}%\tTheta {}\t做多 APR {:+}%\033[0m'.format(*sorted_res[i]))
            elif label[2] == 'F':
                print('\033[0;36m标的 {}\t到期日 {}\t贴水 {}%\tTheta {}\t做多 APR {:+}%\033[0m'.format(*sorted_res[i]))
    print()
    return


def arbitrageD(spot_prices):
    # print('币本位套利提示')
    all_symbols = sorted(Client.getDExchangeInfo()['symbols'], key= lambda symbol: symbol['symbol'])
    symbols = []
    for s in all_symbols:
        if s['baseAsset'] in assets:
            symbols.append(s)

    futures_price_list = Client.getDTickerPrice()
    premium_index_list = Client.getDPremiumIndex()
    futures_prices = {}
    premium_indexs = {}
    for item in futures_price_list:
        futures_prices[item['symbol']] = item['price']
    for item in premium_index_list:
        premium_indexs[item['symbol']] = item['lastFundingRate']
    
    res = {}
    for s in symbols:
        if s['symbol'].endswith('_PERP'):
            funding_rate = Decimal(premium_indexs[s['symbol']])
            # print('标的 {}\t\t\t\t资金费率 {}%\t\t\t做多 APR {}%'.format(s['pair'], funding_rate*100, round(funding_rate*3*360*100, 2)))
            res['{}_{}_D_{}'.format(s['baseAsset'], 'PERP', s['quoteAsset'])] = (s['pair'], funding_rate*100, round(-funding_rate*3*360*100, 2))
        else:
            spot_price = Decimal(spot_prices[s['pair']+'T'])
            futures_price = Decimal(futures_prices[s['symbol']])
            date = datetime.datetime(int('20'+s['symbol'][-6:-4]), int(s['symbol'][-4:-2]), int(s['symbol'][-2:]))
            theta = (date - datetime.datetime.today()).days
            backwardation = spot_price - futures_price
            # print('标的 {}\t到期日 {}\t升水 {}%\tTheta {}\t做多 APR {}%'.format(s['pair'], date.strftime('%Y/%m/%d'), contango/spot_price*100, theta, round((contango/spot_price)/theta*360*100, 2)))
            res['{}_{}_D_{}'.format(s['baseAsset'], s['symbol'][-6:], s['quoteAsset'])] = (s['pair'], date.strftime('%Y/%m/%d'), backwardation/spot_price*100, theta, round((backwardation/spot_price)/theta*360*100, 2))
    # print()
    return res


def arbitrageF(spot_prices):
    # print('U本位套利提示')
    all_symbols = sorted(Client.getFExchangeInfo()['symbols'], key= lambda symbol: symbol['symbol'])
    symbols = []
    for s in all_symbols:
        if s['baseAsset'] in assets:
            symbols.append(s)

    futures_price_list = Client.getFTickerPrice()
    premium_index_list = Client.getFPremiumIndex()
    futures_prices = {}
    premium_indexs = {}
    for item in futures_price_list:
        futures_prices[item['symbol']] = item['price']
    for item in premium_index_list:
        premium_indexs[item['symbol']] = item['lastFundingRate']

    res = {}
    for s in symbols:
        if s['symbol'].endswith('USDT') or s['symbol'].endswith('BUSD'):
            funding_rate = Decimal(premium_indexs[s['symbol']])
            # print('标的 {}\t\t\t\t资金费率 {}%\t\t\t做多 APR {}%'.format(s['pair'], funding_rate*100, round(-funding_rate*3*360*100, 2)))
            res['{}_{}_F_{}'.format(s['baseAsset'], 'PERP', s['quoteAsset'])] = (s['pair'], funding_rate*100, round(-funding_rate*3*360*100, 2))
        else:
            spot_price = Decimal(spot_prices[s['pair']])
            futures_price = Decimal(futures_prices[s['symbol']])
            date = datetime.datetime(int('20'+s['symbol'][-6:-4]), int(s['symbol'][-4:-2]), int(s['symbol'][-2:]))
            theta = (date - datetime.datetime.today()).days
            backwardation = spot_price - futures_price
            # print('标的 {}\t到期日 {}\t贴水 {}%\tTheta {}\t做多 APR {}%'.format(s['pair'], date.strftime('%Y/%m/%d'), backwardation/spot_price*100, theta, round((backwardation/spot_price)/theta*360*100, 2)))
            res['{}_{}_F_{}'.format(s['baseAsset'], s['symbol'][-6:], s['quoteAsset'])] = (s['pair'], date.strftime('%Y/%m/%d'), backwardation/spot_price*100, theta, round((backwardation/spot_price)/theta*360*100, 2))
    # print()
    return res


def purchase_history(history):
    def distribute_times(year, month):
        current_datetime = datetime.datetime.now()
        year_delta = current_datetime.year - year
        month_delta = current_datetime.month - month
        return int(4 * year_delta) + floor(month_delta / 3)

    assets = {i: history[i][0] for i in history}
    for i in assets:
        times = distribute_times(history[i][2], history[i][3])
        for _ in range(times):
            origin = assets[i]
            assets[i] = round(Decimal(int(assets[i] * (1 + (Decimal(1 + history[i][1]) ** Decimal(1/360) - 1) * 90) * 100000000) / 100000000), 8)
        expect = round(Decimal(int(assets[i] * (1 + (Decimal(1 + history[i][1]) ** Decimal(1/360) - 1) * 90) * 100000000) / 100000000), 8)
        print('{}\t上季度收益\t{}\t下季度收益\t+ {} = {}'.format(i, assets[i]-origin, expect-assets[i], expect))
    print()
    return assets


def report():
    assets_candles = weighted_candels(assets=assets, limit=720)

    # 报告现价和涨跌幅
    print('截至 {} 加密市场行情'.format(time.strftime("%Y/%m/%d-%H:%M:%S",time.localtime(int(assets_candles['BTC'][-1][0]/1000)))))
    print("Currency\t收盘价格\t\t\t平均成交价格\t\tBuy/Sell")
    for asset in assets:
        print('{}:\t\t{} USD ({:+}%)\t{} USD {}\t{}/{} {}'.format(
            asset,
            assets_candles[asset][-1][1],
            round((assets_candles[asset][-1][1]/assets_candles[asset][-2][1]-1)*100, 2),
            VWAP(assets_candles[asset][-2:-1])[0],
            '↑' if assets_candles[asset][-1][1] > assets_candles[asset][-2][7]/assets_candles[asset][-2][5] else '↓',
            round(assets_candles[asset][-2][9] / assets_candles[asset][-2][5] * 100, 2),
            round((assets_candles[asset][-2][5]-assets_candles[asset][-2][9]) / assets_candles[asset][-2][5] * 100, 2),
            '↓' if assets_candles[asset][-2][5] > assets_candles[asset][-2][9]*2 else '↑'
        ))
    print()

    # 基本面信息
    print('截至 {} 基本面信息'.format(time.strftime("%Y/%m/%d-%H:%M:%S",time.localtime(int(assets_candles['BTC'][-1][0]/1000)))))
    print('Currency\tP/E\tP/E(360)')
    for asset in assets:
        if len(assets_candles[asset]) >= 720:
            print('{}:\t\t{}\t{}'.format(
                asset,
                round(assets_candles[asset][-1][1] / (assets_candles[asset][-1][1]-assets_candles[asset][-361][1]), 2),
                round(np.mean(list(map(lambda x: x[1], assets_candles[asset][-360:]))) / (np.mean(list(map(lambda x: x[1], assets_candles[asset][-360:])))-np.mean(list(map(lambda x: x[1], assets_candles[asset][-720:-361])))), 2)
            ))
        else:
            print('{}:\t\t数据只有 {}/720 天，无法提供基本面信息'.format(
                asset,
                len(assets_candles[asset])
            ))
    print()

    # 报告每份 Portfolio 价值
    print('截至 {} 每份价值'.format(time.strftime("%Y/%m/%d-%H:%M:%S",time.localtime(int(assets_candles['BTC'][-1][0]/1000)))))
    total_balance = Decimal(0)
    balances = {}
    total_balance_yesterday = Decimal(0)
    balances_yesterday = {}
    for asset in assets:
        total_balance += assets_candles[asset][-1][1] * assets[asset]
        total_balance_yesterday += assets_candles[asset][-2][1] * assets[asset]
        balances[asset] = assets_candles[asset][-1][1] * assets[asset]
        balances_yesterday[asset] = assets_candles[asset][-2][1] * assets[asset]

    print('Total:\t{} USD ({:+}%)'.format(
        total_balance,
        round((total_balance/total_balance_yesterday-1)*100, 2)
    ))
    for asset in assets:
        print('{}:\t{} USD ({:+}%)\t[{}% ({:+}%)]'.format(
            asset,
            balances[asset],
            round((balances[asset]/balances_yesterday[asset]-1)*100, 2),
            round((balances[asset]/total_balance)*100, 2),
            round((balances[asset]/total_balance-balances_yesterday[asset]/total_balance_yesterday)*100, 2)
        ))
    print()


class GetKlines(threading.Thread):
    def __init__(self, symbol, interval = '1d', limit = 1000):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.res = None

    def run(self):
        self.res = candles_decimal(Client.getKlines(symbol=self.symbol, interval=self.interval, limit=self.limit))

    
    def result(self):
        return self.res


class WeightedCandles(threading.Thread):
    def __init__(self, asset, interval = '1d', limit = 1000):
        threading.Thread.__init__(self)
        self.asset = asset
        self.interval = interval
        self.limit = limit
        self.res = None

    def run(self):
        stablecoins = ('USDT', 'USDC', 'BUSD')
        self.thread_list = []
        self.symbol_list = []
        self.candles_list = []
        for sc in stablecoins:
            if self.asset + sc in ['PAXGUSDC']:
                continue
            self.symbol = self.asset + sc
            self.symbol_list.append(self.symbol)
            self.thread_list.append(GetKlines(symbol=self.symbol, interval=self.interval, limit=self.limit))

        for t in self.thread_list: t.start()
        for t in self.thread_list: t.join()
        for t in self.thread_list: self.candles_list.append(t.result())

        self.res = self.candles_list

    def result(self):
        return self.res


def weighted_candels(assets, interval='1d', limit=2):
    thread_dict = {}
    assets_candles = {}
    for asset in assets: thread_dict[asset] = WeightedCandles(asset=asset, interval=interval, limit=limit)
    for t in thread_dict: thread_dict[t].start()
    for t in thread_dict: thread_dict[t].join()
    for t in thread_dict:
        candles_list = thread_dict[t].result()
        weighted_candles = []
        len_list = len(candles_list)
        real_limit = min(map(lambda x: len(x), candles_list))
        if real_limit >= 720:
            if max(map(lambda x: len(x), candles_list)) >= 720:
                candles_list = [i for i in candles_list if len(i)>=720]
        for j in range(real_limit):
            weighted_candles.append([])
            for k in range(11):
                if k in [0, 6]:
                    weighted_candles[-1].append(candles_list[0][j][k])
                elif k in [1, 2, 3, 4]:
                    sum = Decimal(0)
                    weight = Decimal(0)
                    for i in range(len_list):
                        sum += candles_list[i][j][k] * candles_list[i][j][5]
                        weight += candles_list[i][j][5]
                    weighted_candles[-1].append(sum/weight)
                else:
                    sum = Decimal(0)
                    for i in range(len_list):
                        sum += candles_list[i][j][k]
                    weighted_candles[-1].append(sum)
        assets_candles[t] = weighted_candles

    return assets_candles


if __name__ == '__main__':
    history = {
        'PAXG':[Decimal('0.01000000'), Decimal('1.00')/100, 2019, 10],

        'BTC': [Decimal('0.00210000'), Decimal('1.20')/100, 2018, 1],
        'ETH': [Decimal('0.02100000'), Decimal('1.50')/100, 2021, 4],
        'BNB': [Decimal('0.02000000'), Decimal('5.23')/100, 2021, 7],

        'ADA': [Decimal('4.50000000'), Decimal('1.00')/100, 2022, 4],
        'SOL': [Decimal('0.05000000'), Decimal('0.78')/100, 2022, 4],
    }
    assets = purchase_history(history)
    for asset in assets:
        print('{}\t{}'.format(asset, assets[asset]))
    print()
    
    arbitrage()
    report()
    # print(guppy_hpy.heap())
