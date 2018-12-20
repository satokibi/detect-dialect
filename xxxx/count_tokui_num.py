#!/usr/bin/enb python3
# -*- coding: utf-8 -*-


test_file = "/Users/yuya/PycharmProjects/soturon/extract_dialects/Pref25_shiga.txt"

line_num = 0
text0_num = 0
text1_num = 0
text2_num = 0

with open(test_file) as f:
    for line in f:
        try:
            t_a = line.split()

            text = t_a[0]
            answer = t_a[1]
            line_num += 1

            if answer == '0':
                text0_num += 1
            if answer == '1':
                text1_num += 1
            if answer == '2':
                text2_num += 1
        except:
            print(line)

print("text0: " + str(text0_num))
print("text1: " + str(text1_num))
print("text2: " + str(text2_num))
