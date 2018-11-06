import pandas as pd
import numpy as np
from pandas import Series
import time
import datetime
import re
import matplotlib.pyplot as plt

from Draw import Draw

data_frame = None

def read_csv_file():
    global data_frame

    data_frame = pd.read_csv('./query_result.csv', sep = '\t',
                                usecols=[0, 3, 13, 16], names=['stm', 'sid', 'app_name', 'mac'])
    data_frame.stm = pd.to_datetime(data_frame.stm + 28800, unit='s')
    # print(data_frame.head())
    print(data_frame.shape)

    data_frame = data_frame[(data_frame.app_name != 'tv.fun.marketshow') & 
                            (data_frame.app_name != 'com.funshion.poweroffidalog') &
                            (data_frame.app_name != 'com.cvte.tv.media') &
                            (data_frame.app_name != 'com.toptech.localmm')]

    print(data_frame.shape)

def get_user_and_apps_num():
    d = dict()
    d['user_num'] = data_frame.mac.value_counts().count()
    d['app_start_times'] = data_frame.app_name.count()
    d['average'] = d['app_start_times'] / d['user_num']

    return d

def merge_stm_and_sid(df : pd.DataFrame):
    d = dict()
    for i in df.index:
        stm = df.loc[i, 'stm']
        sid = df.loc[i, 'sid']

        if sid in d.keys():
            df.loc[i, 'sid'] = d[sid]
        else:
            df.loc[i, 'sid'] = stm
            d[sid] = stm

    df.drop(columns = 'stm', inplace = True)
    

def main():
    draw = Draw()
    read_csv_file()

    # apps = data_frame.app_name.value_counts()
    # draw.draw_app_names_pie(apps, data_frame.app_name.count())

    # d = get_user_and_apps_num()
    # draw.draw_bar(d)

    users = data_frame.mac.value_counts()
    user = users.index[0]
    # draw.draw_app_open_times_pie_by_person(users, 'times')

    df = data_frame[['mac', 'app_name']].drop_duplicates()
    user_cnt = df.mac.value_counts()
    # draw.draw_app_open_times_pie_by_person(user_cnt, 'count')

    df = data_frame[['mac', 'app_name']]
    df = df[df.mac.isin(user_cnt[(user_cnt >= 1) & (user_cnt < 6)].index.tolist())]
    tmp = df.app_name.value_counts()
    print(tmp.shape)
    print(tmp[tmp > 100])

if __name__ == '__main__':
    main()

