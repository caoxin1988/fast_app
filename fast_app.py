import pandas as pd
import numpy as np
from pandas import Series
import sys
import datetime
import json
import argparse

from User import User
from Apps import Apps
import common
import algo_lru
import http_download

'''
def get_miss_user_number(apps : Apps, user : User):
    # users in daily.csv but not in app_starts.csv
    all_app_user_set = apps.get_user_mac_set()
    all_tv_user_set = user.get_user_mac_set()
    print('miss user numbers: ', len(all_app_user_set & all_tv_user_set))
'''

def merge_apps_and_users(apps: Apps, user : User):
    app_df = common.remove_duplicates_of_app(apps)

    print('merge_apps_and_users : ')
    print('=========\n')

    user_df = user.get_user_dataframe()
    # merge app open dataframe and user open tv dataframe
    app_user_df = pd.merge(user_df, app_df, on = 'mac', how = 'outer')
    # delete the users who has app open record[app_cnt] but no tv open record[open_cnt]
    app_user_df.dropna(subset=['open_cnt'], inplace=True)
    app_user_df.app_cnt = app_user_df.app_cnt.fillna(0)
    app_user_df.app_name = app_user_df.app_name.fillna('no')
    app_user_df.open_cnt = app_user_df.open_cnt.astype('int')
    app_user_df.app_cnt = app_user_df.app_cnt.astype('int')
    print(app_user_df.head())

    return app_user_df

# date : the date run this script
def from_date(date : datetime.date, days : int = 0):
    date_from = date - datetime.timedelta(days = 2)
    date_today = datetime.date.today()

    while date_from + datetime.timedelta(days = 2) <= date_today - datetime.timedelta(days = days):
        yield (date_from, date_from + datetime.timedelta(days=1))

        date_from = date_from + datetime.timedelta(days=1)

def main(date : datetime.date, write_mongo : bool, mongo_server : str,
        update_result : bool, write_mysql : bool, day_num : int):

    if write_mongo:
        algo_lru.init_mongodb(mongo_server)

    for (date_p, date_t) in from_date(date):

        algo_lru.calculate_target_name_with_LRU_with_days(date_p.strftime('%Y%m%d'), date_t.strftime('%Y%m%d'),
                write_mongo= write_mongo, update_result = update_result, day_num = day_num)

    if write_mongo:
        algo_lru.close_mongodb()

    # update mysql database
    if write_mysql:
        date = (datetime.datetime.today() - datetime.timedelta(days = 1)).strftime('%Y%m%d')
        algo_lru.update_mysql(date)

def str2bool(s : str):
    if s.lower() == 'true':
        return True
    else:
        return False

if __name__ == '__main__':

    '''
    usage:
      python fast_app.py --date_start=20181119 --write_mongo=True 
        --mongo_server=172.17.7.26 --update_result=False
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--write_mongo', type = str, default = 'False')
    parser.add_argument('--date_start', type = str, default = None)
    parser.add_argument('--mongo_server', type = str, default = 'localhost')
    parser.add_argument('--update_result', type = str, default = 'True')
    parser.add_argument('--write_mysql', type = str, default = 'False')
    parser.add_argument('--days', type = int, default = 0)
    args = parser.parse_args()

    write_mongo = str2bool(args.write_mongo)
    mongo_server = args.mongo_server
    update_result = str2bool(args.update_result)
    day_num = args.days

    write_mysql = str2bool(args.write_mysql)

    if args.date_start:
        date_int = int(args.date_start)
        date = datetime.date(date_int // 10000, date_int % 10000 // 100, date_int % 100)
    else:
        date = datetime.date.today()

    main(date, write_mongo = write_mongo, mongo_server = mongo_server,
        update_result = update_result, write_mysql = write_mysql, day_num = day_num)