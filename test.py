"""
# -*- coding: utf-8 -*-
# @Time    : 3/4/19 1:39 PM
# @Author  : Cao,Xin
# @Email   : caoxin1988s@gmail.com
# @File    : test.py.py

"""

from LogisticRegression.data_precessing import DataProcessing
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score


# {'18:89:A0:03:60:4D', '18:89:A0:03:5F:F4', '8C:6D:50:79:88:7A'}

if __name__ == '__main__':
    data_processing = DataProcessing(days=30, bulk=7)

    data = data_processing.transform_data('18:89:A0:03:60:4D')

    df = pd.DataFrame(data)
    print(df)
    assert isinstance(df, pd.DataFrame)

    X = df.loc[:, :2].values
    y = df.loc[:, 3].values

    logistic_classifier = LogisticRegression()
    logistic_classifier.fit(X, y)

    y_predict = logistic_classifier.predict(X)

    accuracy = accuracy_score(y, y_predict)
    precision = precision_score(y, y_predict)
    recall = recall_score(y, y_predict)
    print(accuracy, precision, recall)

    print(y_predict)
    print(logistic_classifier.predict_proba(X))
