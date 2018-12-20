#!/usr/bin/enb python3
# -*- coding: utf-8 -*-


def char_count(file):
    # データの行
    line_num = sum(1 for line in open(file))
    text0_num = 0
    text0_max = 0
    text0_min = 100
    text0_min_text = "";

    text1_num = 0
    text1_max = 0
    text1_min = 100

    text2_num = 0
    text2_max = 0
    text2_min = 100


    koeta100num = 0

    # おかしな行
    miss_line_num = 0

    with open(file) as f:
        for line in f:
            text_and_answer = line.split('\t')
            if len(text_and_answer) == 2:
                answer = int(text_and_answer[1].rstrip())
                char_num = len(text_and_answer[0].strip().replace("　","").replace(" ","").replace("\t",""))
                if(char_num > 100):
                    koeta100num += 1

                if answer == 0:
                    text0_num += 1
                    text0_max, text0_min = hikaku(text0_max, text0_min, char_num)
                elif answer == 1:
                    text1_num += 1
                    text1_max, text1_min = hikaku(text1_max, text1_min, char_num)
                elif answer == 2:
                    text2_num += 1
                    text2_max, text2_min = hikaku(text2_max, text2_min, char_num)
            else:
                miss_line_num += 1

        print(file)
        print("行数" + str(line_num))
        print("発言テキスト" + str(text1_num))
        print("max: {0}, min: {1}".format(text1_max,text1_min))
        print("非発言テキスト" + str(text0_num))
        print("max: {0}, min: {1}".format(text0_max, text0_min))
        print("その他" + str(text2_num))
        print("max: {0}, min: {1}".format(text2_max, text2_min))
        print("失敗？" + str(miss_line_num))

        print("over 100: " + str(koeta100num))


def hikaku(max, min, num):
    rmax = max
    rmin = min
    if (max < num):
        rmax = num
    if (min > num):
        rmin = num
    return rmax, rmin


import glob

if __name__ == '__main__':
    answer_dates = []
    files = glob.glob('/Users/yuya/PycharmProjects/soturon/speech_or_not/47honkaigi_answer_txt/*.txt')
    for file in files:
        answer_dates.append(file)

    for pref in answer_dates:
        char_count(pref)
