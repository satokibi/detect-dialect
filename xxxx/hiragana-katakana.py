#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import re
regex = u'[ぁ-んァ-ン]'
src = u"日本語を置換しちゃうゾイゾイ"
dst = re.sub(regex, "/", src)

print (dst)