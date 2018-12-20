#!/usr/bin/enb python3
# -*- coding: utf-8 -*-


import math
import sys
import glob
from extract_dialects_nlplib import *


def load_model(file):
    language_model = {}
    with open(file) as file:
        for line in file:
            w_p = line.split()
            if len(w_p) == 2:
                language_model[w_p[0]] = float(w_p[1])
    return language_model


def select_model(func_name):
    models = []
    if func_name == 'normal':
        str = './language_models/hougen-hindo-{0}gram.txt'
    elif func_name == 'kanzi':
        str = './language_models/hougen_{0}gram_ex_kanzi.txt'
        # str = './language_models/dic_honkaigi_20170913_{0}gram.txt'
    elif func_name == 'kanzi2':
        str = './language_models/hougen_{0}gram_ex_kanzi2.txt'
    elif func_name == 'char':
        str = './language_models/hougen_char_{0}gram_ex_kanzi.txt'
    elif func_name == 'char2':
        str = './language_models/hougen_char_{0}gram_ex_kanzi2.txt'
    elif func_name == 'tanida':
        str = './language_models/dic_kyusyu_tanida_{0}gram.txt'

    for i in range(1, 5):
        # for i in range(1, 3):
        models.append(load_model(str.format(i)))
    return models


def select_calc(N, models, w, DELIMITER, kanzi):
    UNKNOWN_PROBABILITY = 0.05
    v = 3000000
    try:
        if N == 2:
            if w[0] == kanzi or w[1] == kanzi:
                return 0
            w_h2 = models[1].get(w[0] + DELIMITER + w[1], 0)
            w_h1 = models[0].get(w[0], 0)
            w_p2 = w_h2 / w_h1
            p = ((1 - UNKNOWN_PROBABILITY) * w_p2) + UNKNOWN_PROBABILITY / v
            return math.log2(p)
        if N == 3:
            if w[0] == kanzi or w[1] == kanzi or w[2] == kanzi:
                return 0
            w_h3 = models[2].get(w[0] + DELIMITER + w[1] + DELIMITER + w[2], 0)
            w_h2 = models[1].get(w[0] + DELIMITER + w[1], 0)
            w_p3 = w_h3 / w_h2
            p = ((1 - UNKNOWN_PROBABILITY) * w_p3) + UNKNOWN_PROBABILITY / v
            return math.log2(p)
        if N == 4:
            if w[0] == kanzi or w[1] == kanzi or w[2] == kanzi or w[3] == kanzi:
                return 0
            w_h4 = models[3].get(w[0] + DELIMITER + w[1] + DELIMITER + w[2] + DELIMITER + w[3], 0)
            w_h3 = models[2].get(w[0] + DELIMITER + w[1] + DELIMITER + w[2], 0)
            w_p4 = w_h4 / w_h3
            p = ((1 - UNKNOWN_PROBABILITY) * w_p4) + UNKNOWN_PROBABILITY / v
            return math.log2(p)
    except ZeroDivisionError:
        return math.log2(UNKNOWN_PROBABILITY / v)


def calc_probability(file, N, func_name='kanzi', file_type='txt'):
    models = select_model(func_name)
    with open(file) as f:
        reader = csv.reader(f)
        result = {}
        num = 0
        t = Tokenizer()
        if (file_type == 'csv'):
            file = reader
        elif (file_type == 'txt'):
            file = f
        for row in file:
            # 確認用
            sys.stdout.write("\r {0}".format(num))
            sys.stdout.flush()
            num += 1

            if (file_type == 'csv'):
                text = unicodedata.normalize('NFKC',
                                             row[13].strip().replace(" ", "").replace("\t", "").replace("　", ""))
            elif (file_type == 'txt'):
                text = unicodedata.normalize('NFKC',
                                             row.strip().replace(" ", "").replace("\t", "").replace("　", ""))

            kuten = text.split('、')
            gram = split_gram(text, 6)

            for ws in gram:
                if (func_name == 'kanzi'):
                    words = make_word_n_gram(make_words_ex_kanzi(ws, t), N)
                elif (func_name == 'kanzi2'):
                    words = make_word_n_gram(make_words_ex_kanzi2(ws, t), N)
                elif (func_name == 'char'):
                    words = make_char_ngram_ex_kanzi(ws, t, N)
                elif (func_name == 'char2'):
                    words = make_char_ngram_ex_kanzi2(ws, t, N)
                elif (func_name == 'normal'):
                    words = make_word_n_gram(make_words(ws, t), N)

                sentence_probability = 0
                for word in words:
                    if func_name == 'kanzi' or func_name == 'kanzi2' or func_name == 'normal':
                        w = word.split("//")
                        DELIMITER = '//'
                        kanzi = '[x]'
                    elif func_name == 'char' or func_name == 'char2':
                        w = word[:]
                        DELIMITER = ''
                        kanzi = 'x'

                    sentence_probability -= select_calc(N, models, w, DELIMITER, kanzi)

                save_text = ws + " \n// " + text
                result[save_text] = sentence_probability
        return result



def calc_probability_hyouka(file, N, func_name='kanzi'):
    models = select_model(func_name)

    with open(file) as f:
        result = {}
        num = 0
        t = Tokenizer()
        for row in f:
            text_answer = row.split()

            # 確認用
            sys.stdout.write("\r {0}".format(num))
            sys.stdout.flush()
            num += 1
            text = unicodedata.normalize('NFKC',
                                         text_answer[0].strip().replace(" ", "").replace("\t", "").replace("　", ""))

            kanzi = '[x]'
            if (func_name == 'kanzi'):
                words = make_words_ex_kanzi(text, t)
            elif (func_name == 'kanzi2'):
                words = make_words_ex_kanzi2(text, t)
            elif (func_name == 'char'):
                words = make_chars_ex_kanzi(text, t)
                kanzi = 'x'
            elif (func_name == 'char2'):
                words = make_chars_ex_kanzi2(text, t)
                kanzi = 'x'

            try:
                split_sentence = []
                sub = ''

                for w in words:
                    if w != kanzi:
                        sub += w
                    else:
                        if len(sub) != 0:
                            split_sentence.append(sub)
                        sub = ''
            except:
                split_sentence = [""]
                print("a")

            for sp in split_sentence:
                if (func_name == 'normal'):
                    words_ngram = gen_Ngram(row, N)
                if (func_name == 'kanzi'):
                    words_ngram = make_word_n_gram(make_words_ex_kanzi(sp, t), N)
                elif (func_name == 'kanzi2'):
                    words_ngram = make_word_n_gram(make_words_ex_kanzi2(sp, t), N)
                elif (func_name == 'char'):
                    words_ngram = make_char_ngram_ex_kanzi(sp, t, N)
                elif (func_name == 'char2'):
                    words_ngram = make_char_ngram_ex_kanzi2(sp, t, N)

                sentence_probability = 0
                for word in words_ngram:
                    if (func_name == 'normal' or func_name == 'kanzi' or func_name == 'kanzi2'):
                        DELIMITER = '//'
                        w = word.split("//")
                    elif (func_name == 'char' or func_name == 'char2'):
                        DELIMITER = ''
                        w = word[:]

                    sentence_probability -= select_calc(N, models, w, DELIMITER, kanzi)

                save_text = sp + " \n// " + text_answer[1] + "::" + text
                result[save_text] = sentence_probability
    return result


def calc_probability_sp(file, N=2,func_name='kanzi'):
    models = select_model(func_name)
    kanzi = "[x]"
    with open(file) as f:
        result = {}
        num = 0
        t = Tokenizer()
        for row in f:
            row = row.split()[0]
            # 確認用
            sys.stdout.write("\r {0}".format(num))
            sys.stdout.flush()
            num += 1
            text = unicodedata.normalize('NFKC',
                                         row.strip().replace(" ", "").replace("\t", "").replace("　", ""))

            words = make_words_ex_kanzi(text, t)
            sp = []
            for word in words:
                if word != kanzi:
                    sp.append(word)
                else:
                    sentence_probability = 0
                    words_ngram = make_word_n_gram(sp, N)
                    for word2 in words_ngram:
                        w = word2.split("//")
                        sentence_probability -= select_calc(N, models, w, '//', kanzi)
                    save_text = ''.join(sp) + " \n// " + text
                    result[save_text] = sentence_probability
                    sp.clear()
    return result


if __name__ == '__main__':
    test_file2 = "/Users/yuya/PycharmProjects/soturon/47honkaigi_lc_txt/47honkaigi_lc_hatugen/Pref44_oita_nayose0704_0027-03-17.txt.txt"
    test_file4 = './Pref25_shiga_270227.txt'
    test_hyouka = './Pref25_shiga.txt'

    # test_file5 = './Pref32_shimane_270225.txt'
    test_file6 = "test.txt"

    # result = calc_probability_hyouka(test_hyouka, 2, func_name='kanzi')
    # result = calc_probability(test_file4, 2, func_name='normal')

    # result = calc_probability_sp(test_hyouka, func_name='tanida')
    result = calc_probability_sp(test_hyouka, 2,func_name='kanzi')

    i = 0
    for k, v in sorted(result.items(), key=lambda x: x[1]):
        i += 1
        print(" - " + str(i) + "- - - - - - - - - - - - - - - - - - - -")
        print("{0} / {1}".format(v, k))
