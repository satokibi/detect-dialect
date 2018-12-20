#!/usr/bin/enb python3
# -*- coding: utf-8 -*-


test_file = "/Users/yuya/PycharmProjects/soturon/speech_or_not/47honkaigi_answer_txt/Pref41_saga_0027-03-06_answer.txt"

line_num = 0
text0_num = 0
text1_num = 0
text2_num = 0
tokui_num = 0

import glob
honkaigi = []
files = glob.glob('/Users/yuya/PycharmProjects/soturon/47honkaigi_lc_txt/47honkaigi_lc_hatugen/*')

for pref in files:
    with open(pref) as f:
        for line in f:
            line_num += 1
            if 'のほう' in line:
                tokui_num += 1
                print(line)



print(line_num)
print(tokui_num)