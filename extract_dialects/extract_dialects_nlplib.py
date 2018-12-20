#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import csv
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


NGRAM_DELIMITER = '//'


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


def gen_Ngram(text, N):
    words = mw1(text)
    ngram = []
    for i in range(len(words)):
        cw = ""
        if i >= N - 1:
            for j in reversed(range(N)):
                cw += words[i - j] + "//"
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


def split_gram(text, N):
    words = mw1(text)
    ngram = []
    for i in range(len(words)):
        cw = ""
        if i >= N - 1:
            for j in reversed(range(N)):
                cw += words[i - j]
        else:
            continue
        ngram.append(cw)
    return ngram


# - - - - - - - - - - - - - - - - - - - - - - 漢字置換するやつ

import re

# regex = u'[ぁ-んァ-ン]'
regex = u'[ぁ-ん]'
src = u"日本語を置換しちゃうゾイゾイ"
dst = re.sub(regex, "/", src)


def make_words_ex_kanzi(text, t):
    sub_list = []
    for token in t.tokenize(text):
        hiragana = re.sub(regex, "hiragana", token.surface)
        if 'hiragana' not in hiragana:
            token.surface = '[x]'
        sub_list.append(token.surface)
    return sub_list


def make_words_ex_kanzi2(text, t):
    sub_list = []
    for token in t.tokenize(text):
        hiragana = re.sub(regex, '', token.surface)
        if len(hiragana) != 0:
            token.surface = '[x]'
        sub_list.append(token.surface)
    return sub_list

def make_chars_ex_kanzi(text, t):
    str = ''
    for token in t.tokenize(text):
        hiragana = re.sub(regex, "hiragana", token.surface)
        if 'hiragana' not in hiragana:
            token.surface = 'x'
        str += token.surface
    return str


def make_chars_ex_kanzi2(text, t):
    str = ''
    for token in t.tokenize(text):
        hiragana = re.sub(regex, '', token.surface)
        if len(hiragana) != 0:
            token.surface = 'x'
        str += token.surface
    return str


def make_char_ngram_ex_kanzi(text, t, n):
    str = ''
    for token in t.tokenize(text):
        hiragana = re.sub(regex, "hiragana", token.surface)
        if 'hiragana' not in hiragana:
            token.surface = 'x'
        str += token.surface
    results = []
    if len(str) >= n:
        for i in range(len(str) - n + 1):
            results.append(str[i:i + n])

    return results


def make_char_ngram_ex_kanzi2(text, t, n):
    str = ''
    for token in t.tokenize(text):
        hiragana = re.sub(regex, '', token.surface)
        if len(hiragana) != 0:
            token.surface = 'x'
        str += token.surface
    results = []
    if len(str) >= n:
        for i in range(len(str) - n + 1):
            results.append(str[i:i + n])
    return results


import unicodedata


def maesyori(text):
    return unicodedata.normalize('NFKC', text.strip().replace(" ", "").replace("\t", "").replace("　", ""))


if __name__ == '__main__':
    text = 'それぞれの評判だけじゃなしに実数を拾うても、何で滋賀県がみんなからいうてあかんのかなと'
    words = make_words_ex_kanzi(text, Tokenizer())

    split_sentence = []
    sub = ''
    print(words)
    str = ''
    for w in words:
        str += w

    print(str)


    for w in words:
        if w != '[x]':
            sub += w
        else:
            if len(sub) != 0:
                split_sentence.append(sub)
            sub = ''

    print(split_sentence)