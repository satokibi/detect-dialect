#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import csv
from speech_or_not import *

def select_func(line, func='', ):
    num = -1
    if func == 'period':
        if '。' in line:
            num = 1
        else:
            num = 0
    elif func == 'char':
        sn = Speech_or_not('char', 2)
        num = sn.predict([line])[0]
    else:
        print('please select func')

    return num


def make_speech_and_not_txt(file, func=''):
    f0 = open("./hihatugen/" + file.rsplit('.')[0].rsplit('/')[-1] + '_hihatugen.txt', 'w')
    f1 = open("./hatugen/" + file.rsplit('.')[0].rsplit('/')[-1] + '_hatugen.txt', 'w')
    with open(file) as f:
        for line in f:
            num = select_func(line, func)
            if num == 1:
                f1.write(line)
            elif num == 0:
                f0.write(line)
        f1.close()
        f0.close()


def make_speech_and_not_csv(file, func=''):
    f0 = open("./hihatugen/" + file.rsplit('.')[0].rsplit('/')[-1] + '_hihatugen.txt', 'w')
    f1 = open("./hatugen/" + file.rsplit('.')[0].rsplit('/')[-1] + '_hatugen.txt', 'w')
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            line = row[13]
            num = select_func(line, func)
            if num == 1:
                f1.write(line + '\n')
            elif num == 0:
                f0.write(line + '\n')
        f1.close()
        f0.close()


import glob

if __name__ == '__main__':
    honkaigi = glob.glob('/Users/yuya/PycharmProjects/soturon/47honkaigi_oldest_conference/*.csv')
    i = 0

    for file in honkaigi:
        i += 1
        if i == 47:
            make_speech_and_not_csv(file, func='char')
        else:
            make_speech_and_not_csv(file, func='period')
    """

    for file in honkaigi:
        print(file.rsplit('.')[0].rsplit('/')[-1] + '.txt')

    """
