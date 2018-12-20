#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer


def count_answer(file):
    # データの行
    line_num = sum(1 for line in open(file))
    text0 = 0
    text1 = 0
    text2 = 0
    # おかしな行
    miss_line_num = 0

    t = Tokenizer()

    keitaiso_num0 = 0
    meisi_num0 = 0
    jodousi_num0 = 0

    keitaiso_num1 = 0
    meisi_num1 = 0
    jodousi_num1 = 0

    with open(file) as f:
        for line in f:
            text_and_answer = line.split('\t')

            if len(text_and_answer) == 2:
                answer = text_and_answer[1].rstrip()
                tokens = t.tokenize(text_and_answer[0].strip().replace(" ", "").replace("　", ""))
                if answer == '0':
                    for token in tokens:
                        part_of_speech = token.part_of_speech.split(',')
                        if part_of_speech[0] == '名詞':
                            meisi_num0 += 1
                        elif part_of_speech[0] == '助動詞':
                            jodousi_num0 += 1
                        keitaiso_num0 += 1
                    # print("{0} / keitaiso:{1}, meisi:{2}, jodousi:{3}".format(text_and_answer[0],keitaiso_num0,meisi_num0,jodousi_num0))
                    text0 += 1
                elif answer == '1':
                    for token in tokens:
                        ppp = token.part_of_speech.split(',')
                        if ppp[0] == '名詞':
                            meisi_num1 += 1
                        elif ppp[0] == '助動詞':
                            jodousi_num1 += 1
                        keitaiso_num1 += 1
                        # print("{0} / keitaiso:{1}, meisi:{2}, jodousi:{3}".format(text_and_answer[0], keitaiso_num1,
                        # meisi_num1, jodousi_num1))
                    text1 += 1
                elif answer == '2':
                    text2 += 1


            else:
                miss_line_num += 1
        print(file)
        print("行数" + str(line_num))
        print("発言テキスト" + str(text1))
        print("非発言テキスト" + str(text0))
        print("その他" + str(text2))
        print("失敗？" + str(miss_line_num))

        print("0 // keitaiso:{0}, meisi:{1}, jodousi:{2}".format(keitaiso_num0, meisi_num0, jodousi_num0))
        print("1 // keitaiso:{0}, meisi:{1}, jodousi:{2}".format(keitaiso_num1, meisi_num1, jodousi_num1))


def count_keitaiso(file):
    # データの行
    line_num = sum(1 for line in open(file))
    text0 = 0
    text1 = 0
    text2 = 0
    # おかしな行
    miss_line_num = 0

    t = Tokenizer()

    keitaiso_num0 = 0
    keitaiso_num1 = 0
    hinsi0 = {}
    hinsi1 = {}

    with open(file) as f:
        for line in f:
            text_and_answer = line.split('\t')

            if len(text_and_answer) == 2:
                answer = text_and_answer[1].rstrip()
                tokens = t.tokenize(text_and_answer[0].strip().replace(" ", "").replace("　", ""))

                if answer == '0':
                    for token in tokens:
                        part_of_speech = token.part_of_speech.split(',')
                        hinsi0[part_of_speech[0]] = hinsi0.get(part_of_speech[0], 0) + 1
                        keitaiso_num0 += 1
                    text0 += 1
                elif answer == '1':
                    for token in tokens:
                        part_of_speech = token.part_of_speech.split(',')
                        if not token.surface == '、':
                            hinsi1[part_of_speech[0]] = hinsi1.get(part_of_speech[0], 0) + 1

                        keitaiso_num1 += 1
                    text1 += 1
                elif answer == '2':
                    text2 += 1

            else:
                miss_line_num += 1
        print(file)
        print("行数" + str(line_num))
        print("発言テキスト" + str(text1))
        print("非発言テキスト" + str(text0))
        print("その他" + str(text2))
        print("失敗？" + str(miss_line_num))

        print("0 : {0}".format(hinsi0))
        print("0 keitaiso ave:{0}".format((keitaiso_num0 / text0)))
        for hinsi in hinsi0:
            hinsi0[hinsi] = hinsi0.get(hinsi) / keitaiso_num0
        print("0 ave:{0}".format(hinsi0))


        print("1 : {0}".format(hinsi1))
        print("1 keitaiso ave:{0}".format((keitaiso_num1 / text1)))
        for hinsi in hinsi1:
            hinsi1[hinsi] = hinsi1.get(hinsi) / keitaiso_num1
        print("1 ave:{0}".format(hinsi1))

        HINSI = ['フィラー', '副詞', '助詞', '動詞', '名詞', '形容詞', '感動詞', '接続詞', '接頭詞', '記号', '連体詞']
        for h in HINSI:
            print('{0}/{1}:{2}'.format(0, h, hinsi0.get(h, 0)))
            print('{0}/{1}:{2}'.format(1, h, hinsi1.get(h, 0)))



import glob

if __name__ == '__main__':
    answer_dates = []
    files = glob.glob('/Users/yuya/PycharmProjects/soturon/speech_or_not/47honkaigi_answer_txt/*.txt')
    for file in files:
        answer_dates.append(file)

    for pref in answer_dates:
        print(" - - - - - - - - - ")
        print(pref)
        count_keitaiso(pref)
