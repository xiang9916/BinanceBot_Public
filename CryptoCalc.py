import re

from decimal import *
from math import *
from numpy import *

ans = 0
precision = 8
checker = re.compile(r'\d,\d')

while 1:
    str = input()

    while 1:
        m = checker.search(str)
        if m:
            mm = m.group()
            str = str.replace(mm,mm.replace(',',''))
        else:
            break
    
    if str == '': break
    exec("ans="+str)
    if type(ans) == float:
        print((round(ans, precision)))
    else:
        print(ans)