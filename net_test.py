import pandas as pd
import statsmodels.api as sm  
import sys


def test1(filename):
    print('TEST 1:')
    df = pd.read_csv(filename)
    x = df['predictedRatio']
    y = df['actualRatio']
    model = sm.OLS(y,x).fit()
    print(model.summary())


def test2(filename):
    print('TEST 2:')
    df = pd.read_csv(filename)
    false_positive = 0
    true_positive = 0
    false_negative = 0
    true_negative = 0
    total_data = 0

    PREDICTED_RATIO = 1
    ACTUAL_RATIO = 2
    for data in df.itertuples():
        total_data += 1
        if data[PREDICTED_RATIO] > 1:
            if data[ACTUAL_RATIO] > 1:
                true_positive += 1
            else:
                false_positive += 1
        elif data[PREDICTED_RATIO] < 1:
            if data[ACTUAL_RATIO] < 1:
                true_negative += 1
            else:
                false_negative += 1


    print('Results:')
    print('True Positive Rate:',true_positive / total_data)
    print('True Negative Rate:', true_negative / total_data)
    print('False Positive Rate:', false_positive / total_data)
    print('False Negative Rate:',false_negative / total_data)


if __name__ == '__main__':
    filename = sys.argv[1]
    test1(filename)
    test2(filename)
