from BinanceClient import Client
from BinanceIndicators import VWAP
from BinanceTools import candles_decimal, proxy

import matplotlib.pyplot as plt
from decimal import *

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_EVEN
proxy()
Client = Client()

if __name__ == '__main__':
    # 在 Binance 币本位合约上持有加密货币
    # funding rate >= 0.01% 时做空 PERP 合约，<= 0.00% 时平仓
    # funding rate < 0.01% 时做多 PERP 合约，>= 0.00% 时平仓
    # 使用次季的交割合约对冲，直到平仓或交割前1天
    pass
klines = Client.getDKlines(symbol='ETHUSD_PERP', interval='8h', limit=1000)
funding_rates = Client.getDFundingRate(symbol='ETHUSD_PERP', limit=600)

assets = [100]
deliveryFee = 0.0005 * 2
profit = 0
fee = 0
status = 'bear' # long bear short
for date in range(600):
    if date == 0: continue
    asset = assets[-1]
    if status == 'bear':
        '''
        if float(funding_rates[date]['fundingRate']) < -0.0001 and float(funding_rates[date-1]['fundingRate']) < -0.0001:
            status = 'long'
            fee += asset * (deliveryFee)
            asset *= 1-deliveryFee
        '''
        if float(funding_rates[date]['fundingRate']) >= 0.0001 and float(funding_rates[date-1]['fundingRate']) >= 0.0001:
            status = 'short'
            fee += asset * (deliveryFee)
            asset *= 1-deliveryFee
    elif status == 'short':
        '''
        if float(funding_rates[date]['fundingRate']) < -0.0001 and float(funding_rates[date-1]['fundingRate']) < -0.0001:
            status = 'long'
            fee += asset * (deliveryFee*2)
            asset *= 1-deliveryFee*2
        '''
        if float(funding_rates[date]['fundingRate']) < -0.0001:
            status = 'bear'
            fee += asset * (deliveryFee)
            asset *= 1-deliveryFee
        '''
        elif status == 'long':
            if float(funding_rates[date]['fundingRate']) >= 0.0001 and float(funding_rates[date-1]['fundingRate']) >= 0.0001:
                status = 'short'
                fee += asset * (deliveryFee*2)
                asset *= 1-deliveryFee*2
            elif float(funding_rates[date]['fundingRate']) >= 0.0001:
                status = 'bear'
                fee += asset * (deliveryFee)
                asset *= 1-deliveryFee
        '''



    if status == 'bear':
        asset += 0
    elif status == 'long':
        # print(profit)
        profit += - float(funding_rates[date]['fundingRate']) * asset
        asset += - float(funding_rates[date]['fundingRate']) * asset
    elif status == 'short':
        # print(profit)
        profit += float(funding_rates[date]['fundingRate']) * asset
        asset += float(funding_rates[date]['fundingRate']) * asset
    assets.append(asset)
plt.plot(list(range(600)), assets)
plt.show()
print(profit, fee)

funding_rates_data = list(map(lambda x: float(x['fundingRate']), funding_rates))
print(funding_rates_data)
plt.plot(list(range(600)), funding_rates_data)
plt.show()
