import pandas as pd
import numpy as np
from pandas import Series
import time
import os
import datetime

from User import User
from Apps import Apps

'''
def get_miss_user_number(apps : Apps, user : User):
    # users in daily.csv but not in app_starts.csv
    all_app_user_set = apps.get_user_mac_set()
    all_tv_user_set = user.get_user_mac_set()
    print('miss user numbers: ', len(all_app_user_set & all_tv_user_set))
'''

def cal_every_app_and_all_users(apps: Apps, user : User):
    print('cal_every_app_and_all_users : ')
    print('\n')
    app_df = apps.get_dataframe()
    app_df = app_df[['sid', 'app_name', 'mac']].drop_duplicates()[['app_name', 'mac']]
    app_df = app_df.groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
    app_df = app_df.reset_index()
    print(app_df.shape)
    print('=========\n')

    user_df = user.get_user_dataframe()
    # merge app open dataframe and user open tv dataframe
    app_user_df = pd.merge(user_df, app_df, on = 'mac', how = 'outer')
    # delete the users who has app open record[app_cnt] but no tv open record[open_cnt]
    app_user_df.dropna(subset=['open_cnt'], inplace=True)
    app_user_df.app_cnt = app_user_df.app_cnt.fillna(0)
    app_user_df.open_cnt = app_user_df.open_cnt.astype('int')
    app_user_df.app_cnt = app_user_df.app_cnt.astype('int')
    print(app_user_df.head())

    # s = app_df.apply(lambda x : x.app_cnt / x.open_count, axis = 1)
    # print(s.describe())
    # app_df.insert(3, 'open_ratio', s)
    # print(app_df.head(20))
    return app_user_df


def main():

    apps = Apps('./csv_files/20181117-app.csv')
    start_user = User('./csv_files/20181117-start.csv')

    df = cal_every_app_and_all_users(apps, start_user)


if __name__ == '__main__':
    main()

