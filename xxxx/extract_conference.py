#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import csv
import sys
import glob
from datetime import date

honkaigi = glob.glob('./../47honkaigi_20170913/*.csv')

file = './../47honkaigi_20170913/Pref25_shiga_kuten_div2_0905.csv'
date1 = date(27, 2, 27)

# 各県最新の日時の抽出
for pref in honkaigi:
    line = 0
    if pref == file:
        with open(pref) as f:
            reader = csv.reader(f)
            for row in reader:
                line += 1
                try:
                    conference_date = date(int(row[4]), int(row[5]), int(row[6]))
                    if conference_date == date1:
                        if '。' in row[13]:
                            print(row[13])
                except:
                    # なぜか沖縄県の2行だけ日付が0/0/0になっている
                    print("{0} : {1}".format(pref, row))
                    print(line)
                    #            if conference_date > latest_conferece_date_list[pref]:
                    #                latest_conferece_date_list[pref] = conference_date

"""
# フォルダの作成
try:
    os.mkdir('47honkaigi_latest_conference')
except:
    print('already exists')

# 最新の議会のみをcsvファイルで出力
for pref in honkaigi:
    pref_name = pref.split('/')[1]
    pref_name = pref_name.split('.')[0]
    with open('./47honkaigi_latest_conference/' + pref_name + '_' + str(
            latest_conferece_date_list[pref].isoformat()) + '.csv', 'w') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        with open(pref) as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    conference_date = date(int(row[4]), int(row[5]), int(row[6]))
                except:
                    continue
                if conference_date == latest_conferece_date_list[pref]:
                    writer.writerow(row)
"""
