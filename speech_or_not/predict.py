#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

from machine_learning import answer_date_to_vec
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from nlplib import *

def predict(NGRAM, files, dic, func, model):
    vecs, labels, texts = answer_date_to_vec(files, dic=dic, n=NGRAM, func=func)
    # トレーニングデータとテストデータに分割
    # 全体の30%をテストデータにする
    train_vecs, test_vecs, train_labels, test_labels, train_text, test_texts = train_test_split(vecs, labels, texts,
                                                                                                test_size=0.3,
                                                                                                random_state=123)

    estimator = joblib.load(model)
    predict_labels = estimator.predict(test_vecs)
    print(" - - - - -" + func + str(NGRAM) + " - - - - -")

    test_text0 = 0
    test_text1 = 0
    train_text0 = 0
    train_text1 = 0
    test_num = 0
    train_num = 0
    for num in test_labels:
        test_num += 1
        if num == 0:
            test_text0 += 1
        if num == 1:
            test_text1 += 1

    for num in train_labels:
        train_num += 1
        if num == 0:
            train_text0 += 1
        if num == 1:
            train_text1 += 1

    print("label_num" + str(test_num))
    print("test_0_num" + str(test_text0))
    print("test_1_num" + str(test_text1))

    print("train_num" + str(train_num))
    print("train_0_num" + str(train_text0))
    print("train_1_num" + str(train_text1))

    return hyouka(predict_labels, test_labels, test_texts)


if __name__ == '__main__':

    # ラベル付きデータ - - - - -
    fukuoka = "./47honkaigi_answer_txt/Pref40_fukuoka_0027-02-24_answer.txt"
    saga = "./47honkaigi_answer_txt/Pref41_saga_0027-03-06_answer.txt"
    nagasaki = "./47honkaigi_answer_txt/Pref42_nagasaki_nayose0904_0027-03-18_answer.txt"
    kumamoto = "./47honkaigi_answer_txt/Pref43_kumamoto_nayose0704_0027-03-13_answer.txt"
    oita = "./47honkaigi_answer_txt/Pref44_oita_nayose0704_0027-03-17_answer.txt"
    miyazaki = "./47honkaigi_answer_txt/Pref45_miyazaki_nayose0704_0027-03-13_answer.txt"
    kagoshima = "./47honkaigi_answer_txt/Pref46_kagoshima_0027-03-20_answer.txt"
    okinawa = "./47honkaigi_answer_txt/Pref47_okinawa_nayose0704_0027-03-27_answer.txt"

    kyusyu = [fukuoka, saga, nagasaki, kumamoto, oita, miyazaki, kagoshima, okinawa]
    pref3 = [okinawa, kagoshima, miyazaki]
    files = []

    # dictionary ,model- - - - -
    dic_char = './dictionary20171207/dic_char_{0}gram.txt'
    dic_char_ex_noun = './dictionary20171207/dic_char_ex_noun_{0}gram.txt'
    dic_hinsi = './dictionary20171207/dic_hinsi_{0}gram.txt'
    dic_word = './dictionary20171207/dic_word_{0}gram.txt'
    dic_word_ex_noun = './dictionary20171207/dic_word_ex_noun_{0}gram.txt'

    model_char = './learning_models20171207/char_{0}gram_saga.pkl.cmp'
    model_char_ex_noun = './learning_models20171207/char_ex_noun_{0}gram_saga.pkl.cmp'
    model_hinsi = './learning_models20171207/hinsi_{0}gram_saga.pkl.cmp'
    model_word = './learning_models20171207/word_{0}gram_saga.pkl.cmp'
    model_word_ex_noun = './learning_models20171207/word_ex_noun_{0}gram_saga.pkl.cmp'

    for NGRAM in range(1, 4):
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        #$predict(NGRAM, [saga], dic_char.format(NGRAM), 'char', model_char.format(NGRAM))
        predict(NGRAM, [saga], dic_word.format(NGRAM), 'word', model_word.format(NGRAM))
        #predict(NGRAM, [saga], dic_word_ex_noun.format(NGRAM), 'word_ex_noun', model_word_ex_noun.format(NGRAM))
