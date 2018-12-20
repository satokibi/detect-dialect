#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import re
from janome.tokenizer import Tokenizer

regex = u'[ぁ-ん]'

def bun_bunkatu(text):
    sub_list = []
    for token in Tokenizer().tokenize(text):
        hiragana = re.sub(regex, "hiragana", token.surface)
        if 'hiragana' not in hiragana:
            token.surface = '[x]'
        sub_list.append(token.surface)
        split_sentence = []
        sub = ''
        for w in sub_list:
            if w != '[x]':
                sub += w
            else:
                if len(sub) != 0:
                    split_sentence.append(sub)
                sub = ''

    return split_sentence


"""
text = '当たり前の経営者としての理屈ではなかろうかと思うわけです。'
words = bun_bunkatu(text)

print(words)
→['当たり前の', 'としての', 'ではなかろうかと思うわけです']
"""