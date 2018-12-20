#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

from gensim import corpora, matutils
from nlplib import *


def answer_date_to_vec(files, dic, n=None, func='word'):
    dictionary = corpora.Dictionary.load_from_text(dic)

    vecs = []
    labels = []
    texts = []
    t = Tokenizer()

    for file in files:

        # データの行
        line_num = sum(1 for line in open(file))

        text0 = 0
        text1 = 0
        text2 = 0

        # おかしな行
        miss_line_num = 0

        with open(file) as f:
            current_line = 0
            for line in f:
                current_line += 1
                # プログラム経過　表示用
                # sys.stdout.write("\r {0} {1}/ {2}".format(file, current_line, line_num))
                # sys.stdout.flush()

                text_and_answer = line.split('\t')
                if len(text_and_answer) == 2:
                    text = text_and_answer[0]
                    answer = text_and_answer[1].strip()

                    if answer == '1':
                        text1 += 1
                    elif answer == '0':
                        text0 += 1
                    elif answer == '2':
                        text2 += 1
                        continue

                    text = text_preprocessing(text)
                    if (len(text) == 0):
                        print("char_num 0")
                        continue

                    # 学習したい形に合わせてtextを処理
                    if func == 'char':
                        processed_text = make_char_ngram(text, n)
                    elif func == 'word':
                        text = shorten_renzoku_char(text)
                        processed_text = make_word_n_gram(make_words(text, t), n)
                    elif func == 'word_ex_noun':
                        text = shorten_renzoku_char(text)
                        processed_text = make_word_n_gram(make_words_ex_noun(text, t), n)
                    else:
                        print('ないよ')
                        break

                    texts.append(text_and_answer[0])
                    tmp = dictionary.doc2bow(processed_text)
                    # vecs.append(list(matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0]) + test)
                    vecs.append(list(matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0]))
                    label = int(answer)
                    labels.append(label)
                else:
                    miss_line_num += 1

            print('file:{0} 行数:{1} 発言数:{2} 非発言数:{3} 発言/非発言:{4}'.format(file, line_num,
                                                                       text1, text0, text2))

    return vecs, labels, texts
