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
def cal_apps_and_all_users():
    pass

def main():

    apps = Apps()
    user = User()

    # get_miss_user_number(apps, user)
    app_df = apps.get_dataframe()
    app_df = app_df[['app_name', 'mac']].groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
    app_df = app_df.reset_index().set_index('mac')
    print(app_df.shape)

    user_df = user.get_user_dataframe()

    # print(user_df.shape)
    app_df.insert(2, 'open_count', Series(user_df.cnt.values, index=user_df.mac))
    print(app_df.head())
    # print(app_df.shape)
    # print(app_df.open_count.describe())
    # app_df.dropna(how='any', inplace=True)
    # print(app_df.shape)
    # app_df[app_df.open_count < 1000].plot('open_count', 'app_cnt' ,kind='scatter')
    # plt.show()


if __name__ == '__main__':
    main()

