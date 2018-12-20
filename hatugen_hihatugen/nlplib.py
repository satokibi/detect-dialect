#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import re
import unicodedata
from janome.tokenizer import Tokenizer


def make_char_ngram(text, n):
    results = []
    if len(text) >= n:
        text = replace_text(text)
        for i in range(len(text) - n + 1):
            results.append(text[i:i + n])
    return results


def replace_text(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    str = ""
    for token in tokens:
        part_of_speech = token.part_of_speech.split(",")
        if part_of_speech[0] == '名詞':
            if part_of_speech[1] == "数":
                token.surface = '0'
            elif part_of_speech[2] == "人名":
                token.surface = '名前'
            elif part_of_speech[1] == '固有名詞':
                token.surface = '固名'
        str += token.surface
    return str

def noun(text):
    results = []
    t = Tokenizer()
    tokens = t.tokenize(text)
    for token in tokens:
        part_of_speech = token.part_of_speech.split(",")
        if "名詞" == part_of_speech[0]:
            if "数" == part_of_speech[1]:
                results.append('[数字]')
            elif "固有名詞" == part_of_speech[1]:
                results.append('[固有名詞]')
            else:
                results.append(token.surface)
    return results


WORD_DELIMITER = '##'
NGRAM_DELIMITER = '///'


def make_words(text, t):
    sub_list = []
    for token in t.tokenize(text):
        part_of_speech = token.part_of_speech.split(',')
        if part_of_speech[0] == '名詞':
            if part_of_speech[1] == "数":
                token.surface = '0'
            elif part_of_speech[2] == "人名":
                token.surface = '名前'
            elif part_of_speech[1] == '固有名詞':
                token.surface = '固名'
        sub_list.append(token.surface)
        # sub_list.append(token.part_of_speech.split(',')[0] + WORD_DELIMITER + token.surface)
    return sub_list


def make_word_n_gram(words, N):
    ngram = []
    if len(words) < N:
        cw = ""
        for i in range(len(words)):
            cw += words[i] + NGRAM_DELIMITER
        for i in range(N - len(words)):
            cw += 'xxx' + NGRAM_DELIMITER
        cw = cw.rstrip(NGRAM_DELIMITER)
        ngram.append(cw)
        return ngram

    for i in range(len(words)):
        cw = ""
        if i >= N - 1:
            for j in reversed(range(N)):
                cw += words[i - j] + NGRAM_DELIMITER
        else:
            continue
        cw = cw.rstrip(NGRAM_DELIMITER)
        ngram.append(cw)
    return ngram


def make_words_ex_noun(text, t):
    sub_list = []
    for token in t.tokenize(text):
        part_of_speech = token.part_of_speech.split(',')
        if part_of_speech[0] == '名詞':
            if part_of_speech[1] == "数":
                token.surface = '0'
            elif part_of_speech[2] == "人名":
                token.surface = '名前'
            elif part_of_speech[1] == '固有名詞':
                token.surface = '固名'
            else:
                p = re.compile("[!-/:-@[-`{-~]")
                symbol_list = re.findall(p, token.surface)
                if len(symbol_list) == 0:
                    token.surface = part_of_speech[1]
                else:
                    part_of_speech[0] = '記号'
        sub_list.append(part_of_speech[0] + WORD_DELIMITER + token.surface)
    return sub_list


def text_preprocessing(text):
    """
    テキストの前処理
     - 空白の削除
     - 読点の削除
     - 大文字数字　→　小文字数字
    """
    return unicodedata.normalize('NFKC',
                                 text.strip().replace(" ", "").replace("\t", "").replace("　", "").replace("。", ""))


def shorten_renzoku_char(text):
    """
        テキストの前処理
         - 連続する文字(記号)を短くする
            → 4こ以上の記号を4個までにする
        """
    return re.sub(re.compile("(.)\\1{3,}"), r'\1\1\1\1', text)


def hyouka(predict_labels, test_labels, test_texts):
    # 予 / 答
    tp = 0  # 1 / 1
    fp = 0  # 0 / 0
    tn = 0  # 1 / 0
    fn = 0  # 0 / 1
    for i in range(len(predict_labels)):
        if test_labels[i] == 1:
            if predict_labels[i] == test_labels[i]:
                tp += 1
            else:
                fn += 1
                print("予想:" + str(predict_labels[i]) + " / 答え:" + str(test_labels[i]) + " / text:" + str(test_texts[i]))
        if test_labels[i] == 0:
            if predict_labels[i] == test_labels[i]:
                tn += 1
            else:
                fp += 1
                print("予想:" + str(predict_labels[i]) + " / 答え:" + str(test_labels[i]) + " / text:" + str(test_texts[i]))

    accuracy = 0
    precision = 0
    recall = 0

    if tp == 0 or tn == 0 or fp == 0 or fn == 0:
        print(" - Accuracy  :  (" + str(tp + tn) + "/" + str(tp + tn + fp + fn) + ")")
        print(" - Precision :  (" + str(tp) + "/" + str(tp + fp) + ")")
        print(" - Recall    :  (" + str(tp) + "/" + str(tp + fn) + ")")

    else:
        accuracy = round(((tp + tn) / (tp + tn + fp + fn) * 100), 2)
        precision = round((tp / (tp + fp) * 100), 2)
        recall = round((tp / (tp + fn) * 100), 2)

        print("TP:{0}, TN:{1}, FP:{2}, FN:{3}".format(tp, tn, fp, fn))
        print(" - Accuracy  : " + str(accuracy) +
              "% (" + str(tp + tn) + "/" + str(tp + tn + fp + fn) + ")")
        print(" - Precision : " + str(precision) +
              "% (" + str(tp) + "/" + str(tp + fp) + ")")
        print(" - Recall    : " + str(recall) +
              "% (" + str(tp) + "/" + str(tp + fn) + ")")

    return [accuracy, precision, recall]


# グラフ化に必要なものの準備
import matplotlib
import matplotlib.pyplot as plt

# データの扱いに必要なライブラリ
import pandas as pd
import numpy as np
import datetime as dt


def make_graph(result, str):
    plt.style.use('ggplot')
    font = {'family': 'meiryo'}
    matplotlib.rc('font', **font)

    labels = ["c1", "c2", "c3", "w1", "w2", "w3", "en1", "en2", "en3"]

    df = pd.DataFrame(result, columns=['accuracy', 'precision', 'recall'], index=labels)
    df.plot.bar(alpha=0.6, figsize=(12, 5), width=0.2, align='center')
    plt.title(str, size=14)
    plt.ylim(ymax=100, ymin=80)

    plt.show()


def hinsi_count(text):
    t = Tokenizer()
    p = re.compile("[!-/:-@[-`{-~]")
    hinsi = []
    for i in range(15):
        hinsi.append(0)
    for token in t.tokenize(text):
        part_of_speech = token.part_of_speech.split(',')

        symbol_list = re.findall(p, token.surface)
        if len(symbol_list) != 0:
            part_of_speech[0] = '記号'

        if part_of_speech[0] == '連体詞':
            hinsi[0] += 1
        elif part_of_speech[0] == '接頭詞':
            hinsi[1] += 1
        elif part_of_speech[0] == '名詞':
            hinsi[2] += 1
        elif part_of_speech[0] == '動詞':
            hinsi[3] += 1
        elif part_of_speech[0] == '形容詞':
            hinsi[4] += 1
        elif part_of_speech[0] == '副詞':
            hinsi[5] += 1
        elif part_of_speech[0] == '接続詞':
            hinsi[6] += 1
        elif part_of_speech[0] == '助詞':
            hinsi[7] += 1
        elif part_of_speech[0] == '助動詞':
            hinsi[8] += 1
        elif part_of_speech[0] == '感動詞':
            hinsi[9] += 1
        elif part_of_speech[0] == '記号':
            hinsi[10] += 1
        elif part_of_speech[0] == 'フィラー':
            hinsi[11] += 1
        elif part_of_speech[0] == 'その他':
            hinsi[12] += 1
        elif part_of_speech[0] == '未知語':
            hinsi[13] += 1

        # 形態素数
        hinsi[14] += 1

    return hinsi
