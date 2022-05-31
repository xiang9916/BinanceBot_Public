def VWAP(decimal_candles):
    res = []
    for k in decimal_candles:
        res.append(k[7]/k[5])
    return res