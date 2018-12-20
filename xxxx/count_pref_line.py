#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import glob
import csv

honkaigi = glob.glob('./..//47honkaigi_lc_txt/47honkaigi_lc_hihatugen/*.txt')


sum = 0
print('pref_name\t\t/\tdate\t\t/\tline_num')
print('- - - - - - - - - - - - - - - - - - - - - - - -')
for pref in honkaigi:
    with open(pref) as f:
        i = 0
        for row in f:
            i += 1
        sum += i
        pref_name = '_'.join(pref.split('/')[3].split('_')[0:2])
        date = pref.split('_')[-1].split('.')[0]
        print('{0}\t/\t{1}\t/\t{2}'.format(pref_name, date, i))

print('- - - - - - - - - - - - - - - - - - - - - - - -')
print('average : {0}'.format(sum / len(honkaigi)))
print(sum)
