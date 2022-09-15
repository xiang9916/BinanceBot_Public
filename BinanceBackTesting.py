from BinanceClient import Client
from BinanceIndicators import VWAP
from BinanceTools import candles_decimal, proxy

import matplotlib.pyplot as plt
import numpy as np
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
klines = Client.getDKlines(symbol='BNBUSD_PERP', interval='8h', limit=1000)
funding_rates = Client.getDFundingRate(symbol='BNBUSD_PERP', limit=600)

assets = [100]
deliveryFee = 0.0001 * 2
profit = 0
fee = 0
status = 'bear' # long bear short
trades = 0
for date in range(600):
    if date == 0: continue
    asset = assets[-1]
    if status == 'bear':

        if float(funding_rates[date]['fundingRate']) < -0.0000 and float(funding_rates[date-1]['fundingRate']) < -0.0000:
            status = 'long'
            fee += asset * (deliveryFee)
            asset *= 1-deliveryFee
            trades += 1
        
        if float(funding_rates[date]['fundingRate']) > 0.0000 and float(funding_rates[date-1]['fundingRate']) > 0.0000:
            status = 'short'
            fee += asset * (deliveryFee)
            asset *= 1-deliveryFee
            trades += 1
    
    elif status == 'short':
        
        if float(funding_rates[date]['fundingRate']) < -0.0000 and float(funding_rates[date-1]['fundingRate']) < -0.0000:
            status = 'long'
            fee += asset * (deliveryFee*2)
            asset *= 1-deliveryFee*2
            trades += 2
        
        if float(funding_rates[date]['fundingRate']) < -0.0000:
            status = 'bear'
            fee += asset * (deliveryFee)
            asset *= 1-deliveryFee
            trades += 1
        
    elif status == 'long':

        if float(funding_rates[date]['fundingRate']) > 0.0000 and float(funding_rates[date-1]['fundingRate']) > 0.0000:
            status = 'short'
            fee += asset * (deliveryFee*2)
            asset *= 1-deliveryFee*2
            trades += 2
        
        elif float(funding_rates[date]['fundingRate']) > 0.0000:
            status = 'bear'
            fee += asset * (deliveryFee)
            asset *= 1-deliveryFee
            trades += 1
        



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
# print(funding_rates_data)
plt.plot(list(range(600)), funding_rates_data)
plt.show()

print(assets)
profits = [0]
for i in range(1, len(assets)):
    profits.append(assets[i]-assets[i-1])

assets_day = []
profits_day = [0]
for i in range(len(assets)):
    if i%3 == 0:
        assets_day.append(assets[i])
for i in range(1, len(assets_day)):
    profits_day.append(assets_day[i]-assets_day[i-1])
    


def sharpe_rate(lst):
    lst = np.array(lst)
    n = len(lst)
    period = 600
    rf = 2
    print(erp_rf := lst.sum() / n - rf / period)
    print(sigmap := lst.std())
    print(sigmap * np.sqrt(period))
    Sharpe = erp_rf / sigmap * np.sqrt(period)
    return Sharpe

def MaxDrawdown(lst):
    lst = np.array(lst)
    maxdrawdown = [0]
    for i in range(1, len(lst)):
        maxdrawdown.append((lst[:i].max() - lst[i]) / lst[:i].max())
    return max(maxdrawdown)

print(sharpe_rate(profits))
print(MaxDrawdown(assets))
print()
print(sharpe_rate(profits_day))
print(MaxDrawdown(assets_day))

print(trades)