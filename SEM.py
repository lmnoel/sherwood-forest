#Simple Equity Model (SEM)
#In Development by Logan Noel
import pandas as pd
import glob, os, re
import matplotlib.pyplot as plt
import numpy as np
import math


def load_data(path):
    dfs = []
    if not os.path.exists(path):
        return dfs
    filenames = glob.glob(path + '/*.csv')
    for filename in filenames:
        ticker = re.findall('/([A-Z.]*).csv', filename)[0]
        cols = ['date','time',ticker]
        df = pd.read_csv(filename,header=None)
        df.columns = ['date', 'time', ticker]
        dfs.append(df)
    return dfs

def lt(a, b):
    return a < b

def fxn(data, index, range_, minima, param = 1.2):
    vals = []
    
    if index - range_ < 0:
        lb = 0
    else:
        lb = index - range_
    if index + range_ > len(data):
        ub = len(data)
    else:
        ub = index + range_
    subset = data[lb:ub]
    sd = np.std(subset)
    if minima:
        return data[index] < np.mean(subset) - param * sd
    else:
        return data[index] > np.mean(subset) + param * sd


def gt(a, b):
    return a > b


def find_local_extrema(df, minima=True, range=10):
    extrema_i = []
    extrema_vals = []
    f_count = 0
    data = list(df['adj_close'])
    range_param = len(data) * (range / 100)
    for i, obs in enumerate(data):
        f_count += 1
        if fxn(data, i, 20, minima):
            extrema_i.append(i)
            f_count = 0
            extrema_vals.append(obs)

    return extrema_i, extrema_vals


def load_sample_data():
    df = pd.read_csv('gold.csv')
    return df

def plot_sample_data():
    data = load_sample_data()
    minima_i, min_vals = find_local_extrema(data, True, 10)
    fit_min = np.polyfit(minima_i, min_vals, 1)
    fit_min_fxn = np.poly1d(fit_min)
    maxima_i, max_vals = find_local_extrema(data, False, 10)
    fit_max = np.polyfit(maxima_i, max_vals, 1)
    fit_max_fxn = np.poly1d(fit_max)
    indeces = list(range(len(data)))
    plt.plot(indeces, list(data['adj_close']), color='black')
    plt.plot(indeces, fit_min_fxn(indeces),color='r')
    plt.plot(indeces, fit_max_fxn(indeces),color='g')
    plt.title("GLD Price Support/Resistance")
    plt.xlabel("Days")
    plt.ylabel("$")
    for item in minima_i:
        plt.axvline(x=item,color='r', alpha=0.25)
    for item in maxima_i:
        plt.axvline(x=item,color='g',alpha=0.25)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    plot_sample_data()