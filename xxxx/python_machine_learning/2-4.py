#!/usr/bin/enb python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from lib2 import AdalineGD
import matplotlib.pyplot as plt


df = pd.read_csv('https://archive.ics.uci.edu/ml/'
                 'machine-learning-databases/iris/iris.data', header=None)
df.tail()

# 1-100行目の目的変数の抽出
y = df.iloc[0:100, 4].values
# Iris-setosaを-1, Iris-setosaを1に変換
y = np.where(y == 'Iris-setosa', -1, 1)
# 1-100行目の1, 3列目の抽出
X = df.iloc[0:100, [0, 2]].values

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
adal = AdalineGD(n_iter=10, eta=0.01).fit(X, y)

ax[0].plot(range(1, len(adal.cost_) + 1), np.log10(adal.cost_), marker='o')

ax[0].set_xlabel('Epochs')
ax[0].set_ylabel('log(Sum-squared-error)')

ax[0].set_title('Adaline - Learning rate 0.01')

ada2 = AdalineGD(n_iter=10, eta= 0.0001).fit(X,y)

ax[1].plot(range(1,len(ada2.cost_)+1), ada2.cost_,marker='o')

ax[1].set_xlabel('Epochs')
ax[1].set_ylabel('Sum-squared-error')

ax[1].set_title('Adaline - Learning rate 0.0001')

plt.show()