#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer


def keitaiso(str):
    t = Tokenizer()
    tokens = t.tokenize(str)
    return tokens


"""
with open('/Users/yuya/PycharmProjects/soturon/speech_or_not/種類.txt')as f:
    for line in f:

        tokens = keitaiso(line.strip().replace(" ", "").replace("　", ""))
        for token in tokens:
            print(token)
        print('- - - - - - - - - - - - - - - - - - - - - - -')
"""

tokens = keitaiso("それぞれの評判だけじゃなしに実数を拾うても、何で滋賀県がみんなからいうてあかんのかなと".strip().replace(" ", "").replace("　", ""))
for token in tokens:
    print('- - - - - - - - - - - - - - - - - - - - - - -')
    print(token)
    print(token.surface)
    print(token.part_of_speech)
    part_of_speech = token.part_of_speech.split(',')
    print(part_of_speech)
