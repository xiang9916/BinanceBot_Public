import hashlib
import hmac
import json
import time
import os
from decimal import *

def candles_decimal(candles):
    for i in range(len(candles)):
        for j in range(12):
            if j in [1, 2, 3, 4, 5, 7, 9, 10, 11]:
                candles[i][j] = Decimal(candles[i][j])
    return candles


def jsonprint(object):
    print(json.dumps(object, indent=4))


def rounder(num):
    if type(num) == type('0'):
        num = float(num)
    if num >= 100000:
        return int(num)
    elif num >= 10000:
        return round(num, 1)
    elif num >= 1000:
        return round(num, 2)
    elif num >= 100:
        return round(num, 3)
    elif num >= 10:
        return round(num, 4)
    elif num >= 1:
        return round(num, 5)
    else:
        return round(num, 6)


def proxy():
    try:
        os.environ["http_proxy"] = "http://127.0.0.1:10809"
        os.environ["https_proxy"] = "http://127.0.0.1:10809"
    except:
        print('http or https proxy failed, using direct connect')


def sign(param, SECRET_KEY):
    query_string = '&'.join([f'{k}={v}' for k, v in param.items()])
    return hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


def timeStamp():
    return int(time.time() * 1000)
