def VWAP(decimal_candles):
    res = []
    for k in decimal_candles:
        res.append(k[7]/k[5])
    return res

"""
#@version = 1
study("Gold",overlay=True)
length = input(defval=28, title="length", type="int")
mult = input(4.0, type="float", title="StdDev")

vma = vwma(close, length)
plot(vma, "VWMA", color="#FFFFFF")

t_upper = highest(close, length)
t_lower = lowest(close, length)
plot(t_upper, "Turtle Upper", color="#7F3F3F")
plot(t_lower, "Turtle Lower", color="#3F7F3F")

dev = mult * stdev(close, length)
volume_rate = min(1, sma(volume, length) / volume)
b_upper = t_upper + dev * volume_rate
b_lower = t_lower - dev * volume_rate
p1 = plot(b_upper, "Upper", color="#FF3F3F")
p2 = plot(b_lower, "Lower", color="#3FFF3F")
"""