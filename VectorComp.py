import math
import os
import pandas as pd
import random


class Vector(object):

    def __init__(self):
        self.data = {}
        self.contents = set([])
        self.total_words = 0
        self.matches = 0

    def initialize(self, filename1, filename2):
        file1 = open(filename1,'r')
        for line in file1:
            self.data[line[:-1]] = 0
            self.contents.add(line[:-1])
        file2 = open(filename2,'r')
        for line in file2:
            self.data[line[:-1]] = 0
            self.contents.add(line[:-1])

    def add_word(self, word):
        self.total_words += 1
        if word.upper() in self.contents:
            self.data[word.upper()] += 1
            self.matches += 1


    def get_adjusted(self):
        vec_copy = {}
        for key, value in self.data.items():
            if self.total_words != 0:
                vec_copy[key] = value / self.total_words
            else:
                vec_copy[key] = 0

        return vec_copy

    def get_angle(self, secondary_vec):
        adj_1 = self.get_adjusted()
        adj_2 = secondary_vec.get_adjusted()
        dot_product = 0
        magnitude_1 = 0
        magnitude_2 = 0
        for key in adj_1.keys():
            dot_product += adj_1[key] * adj_2[key]
            magnitude_1 += adj_1[key] ** 2
            magnitude_2 += adj_2[key] ** 2

        magnitude_1 = math.sqrt(magnitude_1)
        magnitude_2 = math.sqrt(magnitude_2)

        if magnitude_2 * magnitude_1 == 0:
            print('Error: one or both vectors are empty')
            return 1000
        else:

            return math.acos(dot_product /(magnitude_1 * magnitude_2))

def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', ' ')

    return data

def test(learn_proportion=0.6):
    price_data = pd.read_csv('spy_historical.csv')
    price_data['gain'] = (price_data['Close'] - price_data['Open']) / price_data['Open']
    price_data = price_data[['Date', 'gain']]
    price_data['date_copy'] = price_data['Date']
    price_data_dates = list(price_data['Date'])
    price_data.set_index('date_copy', inplace=True)
    learn_data = []
    test_data = []
    for i, date in enumerate(price_data_dates):
        if random.random() <= learn_proportion:
            learn_data.append(i)
        else:
            test_data.append(i)

    positive_vec = Vector()
    negative_vec = Vector()
    positive_vec.initialize('McDonaldWords/positive.txt','McDonaldWords/negative.txt')
    negative_vec.initialize('McDonaldWords/positive.txt','McDonaldWords/negative.txt')
    counter = 0
    num_learn = len(learn_data)
    for i in learn_data:
        if i <= 1:
            continue
        date = price_data.iloc[i - 1]['Date']
        counter += 1
        if counter % 100 == 0:
            print(round (100 * (counter/ num_learn)),'percent done learning')
        year, month, day = date.split('-')
        filename = 'newspaperdata/{}/{}_{}/nyt_business.txt'.format(year, month, day)
        days_text = read_file(filename)
        if price_data.iloc[i]['gain'] >= 0:
            positive = True
        else:
            positive = False
        for word in days_text.split():
            if positive:
                positive_vec.add_word(word)
            else:
                negative_vec.add_word(word)


    correct_days = 0
    total_days = 0
    total_matches = 0
    for i in test_data:
        if i <= 1:
            continue
        date = price_data.iloc[i - 1]['Date']
        total_days += 1
        year, month, day = date.split('-')

        filename = 'newspaperdata/{}/{}_{}/nyt_business.txt'.format(year, month, day)
        days_text = read_file(filename)
        day_vec = Vector()
        day_vec.initialize('McDonaldWords/positive.txt','McDonaldWords/negative.txt')
        for word in days_text.split():
            day_vec.add_word(word)
        neg_angle = day_vec.get_angle(negative_vec)
        pos_angle = day_vec.get_angle(positive_vec)
        if pos_angle < neg_angle:
            predicted_gain = True
        else:
            predicted_gain = False
        if price_data.iloc[i]['gain'] >= 0:
            actual_gain = True
        else:
            actual_gain = False
        if predicted_gain == actual_gain:
            correct_days += 1
        total_matches += day_vec.matches
    print('avg word hits per day: ',total_matches/total_days)
    print('correctly predicted direction on {} percent of days'.format(100 * (correct_days / total_days)))
    return correct_days / total_days

