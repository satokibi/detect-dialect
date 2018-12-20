#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import os
import csv
import glob
from datetime import date

honkaigi = []
files = glob.glob('./../47honkaigi_20170913/*.csv')
for file in files:
    honkaigi.append(file)

# 各県 平成1年1月1日で初期化
latest_conferece_date_list = {}
oldest_conferece_date_list = {}
for pref in honkaigi:
    # latest_conferece_date_list[pref] = date(1, 1, 1)
    oldest_conferece_date_list[pref] = date(9999, 1, 1)

# 各県最新の日時の抽出
for pref in honkaigi:
    line = 0
    with open(pref) as f:
        reader = csv.reader(f)
        for row in reader:
            line += 1
            try:
                conference_date = date(int(row[4]), int(row[5]), int(row[6]))
            except:
                # なぜか沖縄県の2行だけ日付が0/0/0になっている
                print("{0} : {1}".format(pref, row))
                print(line)
            # if conference_date > latest_conferece_date_list[pref]:
            if conference_date < oldest_conferece_date_list[pref]:
                oldest_conferece_date_list[pref] = conference_date
                # latest_conferece_date_list[pref] = conference_date

for key, item in latest_conferece_date_list.items():
    print('{0} / {1}'.format(key, item))

for key, item in oldest_conferece_date_list.items():
    print('{0} / {1}'.format(key, item))


# フォルダの作成
try:
    os.mkdir('47honkaigi_oldest_conference')
except:
    print('already exists')

# 最新の議会のみをcsvファイルで出力
for pref in honkaigi:
    pref_name = pref.split('/')[-1]
    pref_name = pref_name.split('.')[-2]
    with open('./47honkaigi_oldest_conference/' + pref_name + '_' + str(
            #latest_conferece_date_list[pref].isoformat()) + '.csv', 'w') as write_file:
            oldest_conferece_date_list[pref].isoformat()) + '.csv', 'w') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        with open(pref) as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    conference_date = date(int(row[4]), int(row[5]), int(row[6]))
                except:
                    continue
                #if conference_date == latest_conferece_date_list[pref]:
                if conference_date == oldest_conferece_date_list[pref]:
                    writer.writerow(row)

