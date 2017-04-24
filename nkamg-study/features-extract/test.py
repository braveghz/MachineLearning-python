import numpy as np
import pandas as pd
import sys, getopt, time
from numpy import *

data = {'state':['Ohino','Ohino','Ohino','Nevada','Nevada','aaaa'],
        'year':[2000,2001,2002,2001,2002,2000],
        'pop':[1.5,1.7,3.6,2.4,2.9,1.0]}
df = pd.DataFrame(data)
'''
print df
   pop   state  year
0  1.5   Ohino  2000
1  1.7   Ohino  2001
2  3.6   Ohino  2002
3  2.4  Nevada  2001
4  2.9  Nevada  2002
5  1.0    aaaa  2000
'''
grouped=df.groupby('state')
print len(grouped) #3