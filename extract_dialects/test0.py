#!/user/bin/env python
# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer

def gen_Ngram(words,N):

    ngram = []

    for i in range(len(words)):
        cw = ""

        if i >= N-1:
            for j in reversed(range(N)):
                cw += words[i-j] + "//"
        else:
            continue
        cw = cw.rstrip("//")
        ngram.append(cw)

    return ngram

def mw1(txt):
    txt = txt.replace(" ", "").replace("　", "").replace("\t", "")
    t = Tokenizer()
    tokens = t.tokenize(txt)
    s = []

    for token in tokens:
        if token.part_of_speech.split(',')[1] == '数':
            token.surface = '0'
        s.append(token.surface)
    return s

if __name__ == '__main__':
    for line in open('test3', 'r'):
        s = mw1(line)
        ngram = gen_Ngram(s, 2)

        for i in range(len(ngram)):
                print(ngram[i])

