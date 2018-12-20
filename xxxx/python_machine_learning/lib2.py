#!/usr/bin/enb python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from numpy.random import seed
from matplotlib.colors import ListedColormap


class Perceptron(object):
    """ パーセプトロンの分類器

    パラメータ
    - - - - - - - - - -
    eta : float
        学習率 ( 0.0 より大きく 1.0 以下の値 )
    n_iter : int
        トレーニングデータのトレーニング回数

    属性
    - - - - - - - - - -
    w_ : 1次元配列
        適合後の重み
    errors_ : リスト
        各エポックでの誤分類数

    """

    def __init__(self, eta=0.01, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        """ トレーニングデータに適合させる

        パラメータ
        - - - - - - - - - -
        X : {配列のようなデータ構造}, shape = [n_samples, n_features]
            トレーニングデータ
            n_sampleはサンプルの個数, n_featureは特徴量の個数
        y : 配列のようなデータ構造, shape = [n_samples]
            目的変数

        戻り値
        - - - - - - - - - -
        self : object

        """
        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.n_iter):  # トレーニング回数分トレーニングデータを反復
            errors = 0
            for xi, target in zip(X, y):  # 各サンプルで重みを更新
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        """総入力を計算"""
        return np.dot(X, self.w_[1:] + self.w_[0])

    def predict(self, X):
        """1ステップ後のクラスラベルを返す"""
        return np.where(self.net_input(X) >= 0.0, 1, -1)


class AdalineGD(object):
    """ADAptive LInear NEuron分類器

    パラメータ
    - - - - - - - - - -
    eta : float
        学習率(0.0より大きく1.0以下の値)
    n_iter : int
        トレーニングデータのトレーニング回数

    属性
    - - - - - - - - - -
    w_ : 1次元配列
        適合後の重み
    errors_ : リスト
        各エポックでの誤分類数

    """

    def __init__(self, eta=0.01, n_iter=50):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        """トレーニングデータに適合させる

        パラメータ
        - - - - - - - - - -
        X : {配列のようなデータ構造}, shape = {n_samples, n_features}
            トレーニングデータ
            n_sampleはサンプルの個数, n_featureは特徴量の個数
        y : 配列のようなデータ構造, shape = [n_samples]
            目的変数

        戻り値
        - - - - - - - - - -
        self : object

        """
        self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for i in range(self.n_iter):  # トレーニング回数分トレーニングデータを反復
            output = self.net_input(X)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()

            cost = (errors ** 2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        """総入力を計算"""
        return np.dot(X, self.w_[1:] + self.w_[0])

    def actibation(self, X):
        """線形活性化関数の出力を計算"""
        return self.net_input(X)

    def predict(self, X):
        """1ステップ後のクラスラベルを返す"""
        return np.where(self.actibation(X) >= 0.0, 1, -1)


def plot_decision_regions(X, y, classifier, resolution=0.02):
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))

    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)

    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)

    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)


class AdalineSGD(object):
    """ADaptive LInear NEuron分類器

    パラメータ
    - - - - - - - - - -
    era : float
        学習率(0.0より大きく1.0以下の値)
    n_iter : int
        トレーニングデータのトレーニング回数

    属性
    - - - - - - - - - -
    w_ : １次元配列
        適合後の重み
    errors_ : リスト
        各エポックでの誤分類数
    shuffle : bool (デフォルト : true)
        循環を回避するために各エポックでトレーニングデータをシャッフル
    random_state : int (デフォルト : None)
        シャッフルに使用するランダムステートを設定し、重みを初期化

    """

    def __init__(self, eta=0.01, n_iter=10, shuffle=True, random_state=None):
        # 学習率の初期化
        self.eta = eta
        # トレーニング回数の初期化
        self.n_iter = n_iter
        # 重みの初期化フラグはFalseに設定
        self.w_initialized = False
        # 各エポックでトレーニングデータをシャッフルするかどうかのフラグを初期化
        self.shuffle = shuffle
        # 引数random_stateが指定された場合は乱数種を設定
        if random_state:
            seed(random_state)

    def fit(self, X, y):
        """トレーニングデータに適合させる

        パラメータ
        - - - - - - - - - -
        X : {配列のようなデータ構造}, shape = [n_smaples, n_features]
            トレーニングデータ
            n_sampleはサンプルの個数, n_featureは特徴量の個数
        y : 配列のようなデータ構造, shape = [n_samples]
            目的変数

        戻り値
        - - - - - - - - - -
        self : object

        """
        # 重みベクトルの生成
        self._initialize_weights(X.shape[1])
        # コストを格納するリストの生成
        self.cost_ = []
        # トレーニング回数分トレーニングデータを反復
        for i in range(self.n_iter):
            # 指定された場合はトレーニングデータをシャッフル
            if self.shuffle:
                X, y = self._shuffle(X, y)
            # 各サンプルのコストを格納するリストの生成
            cost = []
            # 各サンプルに対する計算
            for xi, target in zip(X, y):
                # 特徴量xiを目的変数yを用いた重みの更新とコストの計算
                cost.append(self._update_weights(xi, target))
            # サンプルの平均コストの計算
            avg_cost = sum(cost) / len(y)
            # 平均コストを格納
            self.cost_.append(avg_cost)
        return self

    def partial_fit(self, X, y):
        """重みを再初期化することなくトレーニングデータに適合させる"""
        # 初期化されていない場合は初期化を実行
        if not self.w_initialized:
            self._initialize_weights(X.shape[1])
        # 目的変数yの要素数が2以上の場合は
        # 各サンプルの特徴量xiと目的変数targetで重みを更新
        if y.ravel().shape[0] > 1:
            for xi, target in zip(X, y):
                self._update_weight(xi, target)
        # 目的変数yの要素数が1の場合は
        # サンプル全体の特徴量Xと目的変数yで重みを更新
        else:
            self._update_weights(X, y)
        return self

    def _shuffle(self, X, y):
        """トレーニングデータをシャッフル"""
        r = np.random.permutation(len(y))
        return X[r], y[r]

    def _initialize_weights(self, m):
        """重みを0ん￥に初期化"""
        self.w_ = np.zeros(1 + m)
        self.w_initialized = True

    def _update_weights(self, xi, target):
        """ADALINEの学習規則を用いて重みを更新"""
        # 活性化関数の出力を計算
        output = self.net_input(xi)
        # 誤差の計算
        error = (target - output)
        self.w_[1:] += self.eta * xi.dot(error)
        self.w_[0] += self.eta * error
        cost = 0.5 * error ** 2
        return cost

    def net_input(self, X):
        """総入力を計算"""
        return np.dot(X, self.w_[1:] + self.w_[0])

    def activation(self, X):
        """線形活性化関数の出力を計算する"""
        return self.net_input(X)

    def predict(self, X):
        """1ステップ後のクラスラベルを返す"""
        return np.where(self.activation(X) >= 0.0, 1, -1)
