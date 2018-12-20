#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

from gensim import corpora, matutils
from sklearn.externals import joblib
from nlplib import *


class Speech_or_not:
    def __init__(self, func, n):
        if func == 'char':
            self.estimator = joblib.load('./learning_models20171207/char_{0}gram_kyusyu.pkl.cmp'.format(n))
            self.dic = corpora.Dictionary.load_from_text('./dictionary20171207/dic_char_{0}gram.txt'.format(n))
        elif func == 'word':
            self.estimator = joblib.load('./learning_models20171207/word_{0}gram_kyusyu.pkl.cmp'.format(n))
            self.dic = corpora.Dictionary.load_from_text('./dictionary20171207/dic_word_{0}gram.txt'.format(n))
        elif func == 'word_en':
            self.estimator = joblib.load('./learning_models20171207/word_ex_noun_{0}gram_kyusyu.pkl.cmp'.format(n))
            self.dic = corpora.Dictionary.load_from_text('./dictionary20171207/dic_word_ex_noun_{0}gram.txt'.format(n))

        self.func = func
        self.n = n
        self.t = Tokenizer()

    def predict(self, texts):
        vecs = []
        for text in texts:
            text = text_preprocessing(text)
            # 学習したい形に合わせてtextを処理
            if self.func == 'char':
                processed_text = make_char_ngram(text, self.n)
            elif self.func == 'word':
                text = shorten_renzoku_char(text)
                processed_text = make_word_n_gram(make_words(text, self.t), self.n)
            elif self.func == 'word_en':
                text = shorten_renzoku_char(text)
                processed_text = make_word_n_gram(make_words_ex_noun(text, self.t), self.n)

            tmp = self.dic.doc2bow(processed_text)
            vecs.append(matutils.corpus2dense([tmp], num_terms=len(self.dic)).T[0])
        return self.estimator.predict(vecs)


if __name__ == '__main__':
    sn = Speech_or_not('word', 1)

    str = ''
    while str != 'quit':
        str = input()
        if len(str) > 0:
            print(sn.predict([str]), end='')
            print(" / " + str)
