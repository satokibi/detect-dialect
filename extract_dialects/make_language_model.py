#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import glob
from extract_dialects_nlplib import *

honkaigi = glob.glob('/Users/yuya/PycharmProjects/soturon/extract_dialects/tanida_hikaku/*.txt')

regex = u'[ぁ-んァ-ン]'
src = u"漢字ひらがなカタカナabc"
dst = re.sub(regex, "/", src)

t = Tokenizer()

counts = {}

N = 2
for pref in honkaigi:
    print(pref)
    with open(pref) as file:
        # reader = csv.reader(file)
        for row in file:
            words = make_word_n_gram(make_words(maesyori(row), t), N)
            for word in words:
                counts[word] = counts.get(word, 0) + 1

f = open('dic_kyusyu_tanida_{0}gram.txt'.format(N), 'w')
for word, count in counts.items():
    probability = counts[word]
    f.write(word + "\t")
    f.write(str(probability) + "\n")
f.close()