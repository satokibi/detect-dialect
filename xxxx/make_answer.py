#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import csv
import glob
"""
def a():
    honkaigi = []
    files = glob.glob('47honkaigi_latest_conference/*.csv')
    for file in files:
        honkaigi.append(file)

    # 最新の議会のみをcsvファイルで出力
    for pref in honkaigi:
        pref_name = pref.split('/')[1]
        pref_name = pref_name.split('.')[0]

        with open('./scikit-learn_gensim/47honkaigi_answer_csv/' + pref_name + '_answer.csv', 'w') as write_file:
            writer = csv.writer(write_file, lineterminator='\n')
            with open(pref) as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row[13]) == 0:
                        continue
                    if '。' in row[13]:
                        num = '1'
                    else:
                        num = '0'
                    row.append(num)
                    writer.writerow(row)

"""

if __name__ == '__main__':
    file = "/Users/yuya/PycharmProjects/soturon/47honkaigi_latest_conference/Pref42_nagasaki_nayose0904_0027-03-18.csv"
    with open(file) as read_file:
        reader = csv.reader(read_file)
        with open('answer.txt', 'w') as write_file:
            for row in reader:
                if len(row[13]) == 0:
                    continue
                if '。' in row[13]:
                    num = '1'
                else:
                    num = '0'
                write_file.write(row[13] + "\t")
                write_file.write(num + "\n")
