import pandas as pd
import numpy as np
from pandas import Series
import time
import datetime
import re
import matplotlib.pyplot as plt

from User import User
from Apps import Apps

'''
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
'''

def get_miss_user_number(apps : Apps, user : User):
    # users in daily.csv but not in app_starts.csv
    all_app_user_set = apps.get_user_mac_set()
    all_tv_user_set = user.get_user_mac_set()
    print('miss user numbers: ', len(all_app_user_set & all_tv_user_set))

# 计算打开app用户数量和所有开机用户数量关系
def cal_apps_and_all_users(apps: Apps, user : User):
    print('cal_apps_and_all_users')
    # get_miss_user_number(apps, user)
    app_df = apps.get_dataframe()
    app_df = app_df[['app_name', 'mac']].groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
    app_df = app_df.reset_index().set_index('mac')
    print(app_df.shape)

    user_df = user.get_user_dataframe()

    # print(user_df.shape)
    app_df.insert(2, 'open_count', Series(user_df.cnt.values, index=user_df.mac))
    app_df.dropna(how='any', inplace=True)
    app_df.open_count = app_df.open_count.astype('int')
    print(app_df.open_count.describe())
    print(app_df.app_cnt.describe())

    print(app_df.head(5))

    s = app_df.apply(lambda x : x.app_cnt / x.open_count, axis = 1)
    print(s.describe())

def cal_every_app_and_all_users(apps: Apps, user : User):
    print('cal_every_app_and_all_users')
    app_df = apps.get_dataframe()
    app_df = app_df[['sid', 'app_name', 'mac']].drop_duplicates()[['app_name', 'mac']]
    app_df = app_df.groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
    app_df = app_df.reset_index().set_index('mac')

    user_df = user.get_user_dataframe()
    app_df.insert(2, 'open_count', Series(user_df.cnt.values, index=user_df.mac))
    app_df.dropna(how='any', inplace=True)
    app_df.open_count = app_df.open_count.astype('int')
    print(app_df.open_count.describe())
    print(app_df.app_cnt.describe())
    print(app_df.shape)

    s = app_df.apply(lambda x : x.app_cnt / x.open_count, axis = 1)
    print(s.describe())
    app_df.insert(3, 'open_ratio', s)
    print(app_df.head(20))


def main():

    # apps = Apps('./query_result.csv')
    user_10 = User('./daily.csv')

    user_11 = User('./11th/daily_11.csv')
    app_11 = Apps('./11th/3rd_app_11.csv')

    # user.user_open_times()

    # get_miss_user_number(apps, user)

    # apps.draw_app_names_pie()
    # apps.draw_app_by_person()
    # apps.show_apps_by_highlight_user()

    # cal_apps_and_all_users(app_11, user_11)
    cal_every_app_and_all_users(app_11, user_11)


if __name__ == '__main__':
    main()

