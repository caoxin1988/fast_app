import pandas as pd
import numpy as np
from pandas import Series
import sys
import datetime
import json
import argparse

from User import User
from Apps import Apps
import http_download
import common
import algo_lru

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

def get_package_json(names : Series):
    l = []
    for name in names:
        d = {'package_name' : name}
        # d = {'package_name' : name, 'start_time' : ''}
        l.append(d)

    res = {'packagelist' : l}
    return res

def update_target_app_database(mysql):
    date = datetime.date.today() - datetime.timedelta(days = 2)
    app_file = common.CSV_DIR + date.strftime('%Y%m%d') + common.APP_CSV_SUFFIX

    apps = Apps(app_file)
    app_df = apps.get_dataframe()
    app_df = app_df[['mac', 'app_name']].groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
    app_df = app_df.reset_index()

    i = 0
    for mac_addr in app_df.mac.tolist():
        df = app_df[app_df.mac == mac_addr].nlargest(2, 'app_cnt')

        res = get_package_json(df.app_name)
        i += 1
        print(i)
        # print(res)
        # print(json.dumps(res))

#     mysql.update_target_app('28:76:CD:01:02:B1', json.dumps(res))
#     mysql.update_target_app('28:76:CD:00:00:53', json.dumps(res))

# date : the date run this script
def from_date(date : datetime.date, days : int = 0):
    date_from = date - datetime.timedelta(days = 2)
    date_today = datetime.date.today()

    while date_from + datetime.timedelta(days = 2) <= date_today - datetime.timedelta(days = days):
        yield (date_from, date_from + datetime.timedelta(days=1))

        date_from = date_from + datetime.timedelta(days=1)

def main(date : datetime.date, write_mongo : bool, mongo_server : str):

    if write_mongo:
        algo_lru.init_mongodb(mongo_server)

    for (date_p, date_t) in from_date(date):
        algo_lru.calculate_target_name_with_LRU(date_p.strftime('%Y%m%d'), date_t.strftime('%Y%m%d'),
                write_mongo= write_mongo)

    if write_mongo:
        algo_lru.close_mongodb()


if __name__ == '__main__':
    ## download csv files from http_server
    http_download.download_gz()

    '''
    usage:
      python fast_app.py --write_mongo=True --mongo_server=localhost --date_start=20181119
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--write_mongo', type = bool, default = False)
    parser.add_argument('--date_start', type = str, default = None)
    parser.add_argument('--mongo_server', type = str, default = 'localhost')
    args = parser.parse_args()

    write_mongo = args.write_mongo
    mongo_server = args.mongo_server

    if args.date_start:
        date_int = int(args.date_start)
        date = datetime.date(date_int // 10000, date_int % 10000 // 100, date_int % 100)
    else:
        date = datetime.date.today()

    main(date, write_mongo = write_mongo, mongo_server = mongo_server)