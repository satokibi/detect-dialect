#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import glob
import csv
from datetime import date

honkaigi = glob.glob('./../47honkaigi_20170719/*.csv')

prefs = {}
for pref in honkaigi:
    line_num = 0
    period_num = 0
    before_date = date(1, 1, 1)
    pref_period = {}
    with open(pref) as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                current_date = date(int(row[4]), int(row[5]), int(row[6]))
                if before_date != current_date:
                    if line_num != 0:
                        period_ratio = period_num / line_num
                        pref_period[before_date] = period_ratio
                        # str(period_num) + '/' + str(line_num)
                    before_date = current_date
                    line_num = 0
                    period_num = 0
                line_num += 1
                if '。' in row[13]:
                    period_num += 1
            except:
                continue
        prefs[pref] = pref_period

print(prefs)

for pref in honkaigi:
    print('- - - - - - - - - -')
    print('{0}'.format(pref))
    for key, item in sorted(prefs[pref].items(), key=lambda x: x[1]):
        print("{0} / {1}".format(key, item))
