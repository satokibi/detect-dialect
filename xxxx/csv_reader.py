#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import csv
import glob

from janome.tokenizer import Tokenizer


def keitaiso(str):
    t = Tokenizer()
    tokens = t.tokenize(str)
    return tokens


honkaigi = glob.glob('./../47honkaigi_20170913/*.csv')

oita = '/Users/yuya/PycharmProjects/soturon/47honkaigi_20170913/Pref44_oita_nayose0704.csv'

for pref in honkaigi:
    hougen_num = 0
    with open(pref) as open_file:
        reader = csv.reader(open_file)
        t = Tokenizer()
        line_num = 0
        for row in reader:
            line_num += 1
            if 'けん' in row[13]:
                hougen_num += 1
                print("{0}/{1}/{2} : {3}".format(row[4], row[5], row[6], row[13]))

    print(pref)
    print("{0} / {1} - - - - - - - - - - - - - - - - - - -".format(hougen_num,line_num))
    print()

