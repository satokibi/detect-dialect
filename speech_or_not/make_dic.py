#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import csv
import glob
from gensim import corpora
from nlplib import *


def make_dic_char(files, NGRAM):
    charas = []
    for pref in files:
        with open(pref) as f:
            reader = csv.reader(f)
            for row in reader:
                text = text_preprocessing(row[13])
                if (len(text) != 0):
                    char_ngram = make_char_ngram(text, NGRAM)
                if len(char_ngram) != 0:
                    charas.append(char_ngram)

    dictionary = corpora.Dictionary(charas)
    # 出現回数x回以下, y割以上のものを削除(少なすぎる、多すぎるものを消す)
    dictionary.filter_extremes(no_below=4, no_above=0.5)
    dictionary.save_as_text('./dictionary20171207/dic_char_' + str(NGRAM) + 'gram.txt')


def make_dic_word(files, NGRAM):
    dic_list = []
    t = Tokenizer()

    for pref in files:
        with open(pref) as f:
            reader = csv.reader(f)
            for row in reader:
                text = text_preprocessing(row[13])
                text = shorten_renzoku_char(text)
                if len(text) != 0:
                    word_ngram = make_word_n_gram(make_words(text, t), NGRAM)
                if len(word_ngram) != 0:
                    dic_list.append(word_ngram)

    dictionary = corpora.Dictionary(dic_list)
    # 出現回数x回以下, y割以上のものを削除(少なすぎる、多すぎるものを消す)
    dictionary.filter_extremes(no_below=2, no_above=0.5)
    dictionary.save_as_text('./dictionary20171207/dic_word_{0}gram.txt'.format(NGRAM))


def make_dic_word_ex_noun(files, NGRAM):
    dic_list = []
    t = Tokenizer()

    for pref in files:
        with open(pref) as f:
            reader = csv.reader(f)
            for row in reader:
                text = text_preprocessing(row[13])
                text = shorten_renzoku_char(text)
                if len(text) != 0:
                    word_ngram = make_word_n_gram(make_words_ex_noun(text, t), NGRAM)
                if len(word_ngram) != 0:
                    dic_list.append(word_ngram)

    dictionary = corpora.Dictionary(dic_list)  # 出現回数x回以下, y割以上のものを削除(少なすぎる、多すぎるものを消す)
    dictionary.filter_extremes(no_below=2, no_above=0.5)
    dictionary.save_as_text('./dictionary20171207/dic_word_ex_noun_{0}gram.txt'.format(NGRAM))



# gensim で特徴語辞書を作る
if __name__ == '__main__':
    honkaigi = glob.glob('./../47honkaigi_latest_conference/*.csv')

    for NGRAM in range(1, 4):
        print(NGRAM)
        make_dic_char(honkaigi, NGRAM)
        make_dic_word(honkaigi, NGRAM)
        make_dic_word_ex_noun(honkaigi, NGRAM)
