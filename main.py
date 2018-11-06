import pandas as pd
import numpy as np
from pandas import Series
import time
import datetime
import re
import matplotlib.pyplot as plt

from Draw import Draw

data_frame = None
user_counts = 0
app_open_times = 0
app_numbers = 0

def read_csv_file():
    global data_frame

    data_frame = pd.read_csv('./query_result.csv', sep = '\t',
                                usecols=[0, 3, 13, 16], names=['stm', 'sid', 'app_name', 'mac'])
    data_frame.stm = pd.to_datetime(data_frame.stm + 28800, unit='s')
    # print(data_frame.head())
    # print(data_frame.shape)

    data_frame = data_frame[(data_frame.app_name != 'tv.fun.marketshow') & 
                            (data_frame.app_name != 'com.funshion.poweroffidalog') &
                            (data_frame.app_name != 'com.cvte.tv.media') &
                            (data_frame.app_name != 'com.toptech.localmm')]

    print(data_frame.shape)

def get_user_and_apps_num():
    global user_counts
    global app_open_times

    d = dict()
    d['user_num'] = user_counts = data_frame.mac.value_counts().count()
    d['app_start_times'] = app_open_times = data_frame.app_name.count()
    d['average'] = d['app_start_times'] / d['user_num']
    print('user and app num : ', d)


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

def app_graph_by_name(mac : str, app_name : str):
    print('%s users has opened %s' % (data_frame[data_frame.app_name == app_name].mac.value_counts().count(), app_name))

    df = data_frame[data_frame.mac == mac]
    print(df[df.app_name == app_name].head())
    print(df[df.app_name == app_name].shape)

    sessions = data_frame[(data_frame.mac == mac)].sid.drop_duplicates().count()
    print('user : %s has opened %s for %s times in %s different sessions' % \
            (mac, app_name, len(df[df.app_name == app_name]), sessions))

    apps = df.app_name.drop_duplicates()
    d = dict()
    for app in apps.values:
        cnt = len(df[df.app_name == app])
        d[app] = [cnt, sessions]
        print('user : %s has opened %s for %s times in %s different sessions' % \
                (mac, app, cnt, sessions))

    pd.DataFrame(d, index = ['times', 'sessions']).T.plot(kind='bar')
    plt.show()
    

def main():
    global app_numbers
    draw = Draw()
    read_csv_file()

    apps = data_frame.app_name.value_counts()
    app_numbers = apps.count()
    draw.draw_app_names_pie(apps, data_frame.app_name.count())

    get_user_and_apps_num()

    users = data_frame.mac.value_counts()
    draw.draw_app_open_times_pie_by_person(users, 'times')

    df = data_frame[['mac', 'app_name']].drop_duplicates()
    user_cnt = df.mac.value_counts()
    # how many apps opened per person
    draw.draw_app_open_times_pie_by_person(user_cnt, 'count')

    print(user_counts, app_numbers, app_open_times)

    # show the apps by the GOOD users
    df= data_frame[['mac', 'app_name']]
    set1 = set(user_cnt[(user_cnt >= 1) & (user_cnt < 6)].index.tolist())
    set2 = set(users[users >= 10].index.tolist())
    highlight_user = set1 & set2
    print(len(set1), len(set2), len(highlight_user))
    df = df[df.mac.isin(highlight_user)]
    tmp = df.app_name.value_counts()
    highlight_app = set(tmp.head(20).index.tolist())
    print(tmp.shape)
    print(tmp.head(20))
    draw.draw_bar(tmp.head(20), 'barh')
    
    # highlight users and highlight apps
    for i in range(5):
        mac = highlight_user.pop()
        app_name = highlight_app.pop()
        print('===> ', mac, app_name)
        app_graph_by_name(mac, app_name)



if __name__ == '__main__':
    main()

