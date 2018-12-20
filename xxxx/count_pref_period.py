#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import glob
import csv
from collections import OrderedDict

honkaigi = []
files = glob.glob('./../47honkaigi_20170913/*.csv')
for file in files:
    honkaigi.append(file)

prefs = OrderedDict()
for pref in honkaigi:
    line_num = 0
    period_num = 0
    with open(pref) as f:
        reader = csv.reader(f)
        for row in reader:
            # str(period_num) + '/' + str(line_num)
            line_num += 1
            if '。' in row[13]:
                period_num += 1
        period_ratio = period_num / line_num
        prefs[pref] = str(period_num) + ' / ' + str(line_num) + ' --' + str(period_ratio)
        line_num = 0
        period_num = 0

# for key, item in sorted(prefs.items(), key=lambda x: x[1]):
#    print("{0} / {1}".format(key, item))

for key, item in prefs.items():
    print("{0} / {1}".format(key, item))
