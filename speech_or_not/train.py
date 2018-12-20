#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

from machine_learning import answer_date_to_vec
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

def make_model(NGRAM, files, dic, func, save_file_name):
    vecs, labels, texts = answer_date_to_vec(files, dic=dic, n=NGRAM, func=func)
    train_vecs, test_vecs, train_labels, test_labels = train_test_split(vecs, labels, test_size=0.3, random_state=123)

    estimator = MultinomialNB()
    estimator.fit(train_vecs, train_labels)
    joblib.dump(estimator, save_file_name, compress=True)


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
    pref3 = [saga, fukuoka, oita]

    # dictionary ,savefilename- - - - -
    dic_char = './dictionary20171207/dic_char_{0}gram.txt'
    dic_word = './dictionary20171207/dic_word_{0}gram.txt'
    dic_word_ex_noun = './dictionary20171207/dic_word_ex_noun_{0}gram.txt'

    sf_name_char = './learning_models20171207/char_{0}gram_kyusyu.pkl.cmp'
    sf_name_word = './learning_models20171207/word_{0}gram_kyusyu.pkl.cmp'
    sf_name_word_ex_noun = './learning_models20171207/word_ex_noun_{0}gram_kyusyu.pkl.cmp'

    for NGRAM in range(1, 4):
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print(NGRAM)
        make_model(NGRAM, kyusyu, dic_char.format(NGRAM), 'char', sf_name_char.format(NGRAM))
        make_model(NGRAM, kyusyu, dic_word.format(NGRAM), 'word', sf_name_word.format(NGRAM))
        make_model(NGRAM, kyusyu, dic_word_ex_noun.format(NGRAM), 'word_ex_noun', sf_name_word_ex_noun.format(NGRAM))
