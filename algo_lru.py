# set target apps for target users with LRU

import pandas as pd
from pandas import Series
import datetime
import os
import csv
import json
import requests
import hashlib
import time

import common
from MySQL import MySQL
from Mongodb import Mongodb
from Apps import Apps
from AppResult import AppResult

mongodb = None

'''operations for mongodb'''
def init_mongodb(server : str):
    global mongodb
    mongodb =  Mongodb(db_name = common.MONGO_DB, server_ip = server)

def delete_all_data(collec : str):
    mongodb.delete_all(collec)

def close_mongodb():
    mongodb.close()

def merge_dataframe_with_days(df : pd.DataFrame, date : str, day_num : int = 0):
    app_df = df

    for i in range(day_num, 0, -1):
        date_f = datetime.date(int(date[:4]), int(date[4:6]), int(date[6:])) - datetime.timedelta(days = i)
        apps = Apps(date_f.strftime('%Y%m%d'))
        app_df_f = apps.get_dataframe()
        app_df_f = app_df_f[['mac', 'app_name']].groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})

        app_df = pd.concat([app_df, app_df_f])

        app_df = app_df.reset_index().groupby(['mac', 'app_name']).agg({'app_cnt':'sum'})

    return app_df

def write_result_file_with_days(df : pd.DataFrame, date : str, update_result : bool, days : int = 0):
    result_file = common.RESULT_DIR + date + common.RESULT_CSV_SUFFIX

    # merge dataframe with former days
    df = merge_dataframe_with_days(df, date, days)

    if not update_result:
        return

    start = datetime.datetime.now()

    result = []
    for mac_addr in df.index.levels[0]:
        df_sub = df.loc[mac_addr]
        if len(df_sub) > 2:
            df_sub = df_sub.sort_values(by = 'app_cnt', ascending = False)[:common.TARGET_NUM]

        for app_name in df_sub.index:
            res_sub = []
            res_sub.append(mac_addr)
            res_sub.append(app_name)

            result.append(res_sub)

    with open(result_file, 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)

    print('#### Runtime = ', datetime.datetime.now() - start)


'''algothrims for lru with days '''
def calculate_target_name_with_LRU_with_days(date_p : str, date_t : str, write_mongo : bool = False,
    update_result : bool = True, day_num : int = 0):

    result_file = common.RESULT_DIR + date_p + common.RESULT_CSV_SUFFIX
    app_df = None
    if os.path.exists(result_file):
        apps = AppResult(result_file)
        app_df = apps.get_dataframe()
    else:
        # data from former day
        apps = Apps(date_p)

        app_df = apps.get_dataframe()
        app_df = app_df[['mac', 'app_name']].groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
        write_result_file_with_days(df = app_df, date = date_p, update_result = update_result, days = day_num)

        apps = AppResult(result_file)
        app_df = apps.get_dataframe()

    # data for target day
    apps = Apps(date_t)
    app_df1 = apps.get_dataframe()
    app_df1 = app_df1[['mac', 'app_name']].groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
    # generate result for prediction
    write_result_file_with_days(df = app_df1, date = date_t, update_result = update_result, days = day_num)

    app_df1 = app_df1.reset_index()

    # merge two dataframe for the result
    df = pd.merge(app_df, app_df1, on = ['mac', 'app_name'])

    # get app and user datas
    app_start_times = int(app_df1.app_cnt.sum())
    user_count_apps = int(app_df1.mac.drop_duplicates().count())
    app_counts = int(app_df1.app_name.drop_duplicates().count())

    app_start_info_dict = {
            'date' : datetime.date(int(date_t[:4]), int(date_t[4:6]), int(date_t[6:])).strftime('%Y%m%d %a'),
            'app_start_times' : app_start_times,
            'user_count_apps' : user_count_apps,
            'app_counts' : app_counts }
    # app_start_info_dict = {'date': '20181118 Sun', 'app_start_times': 434575, 'user_count_apps': 127219, 'app_counts': 1999}
    print(app_start_info_dict)

    if write_mongo:
        print('#### start writing app_start_info_dict into mongoDB')
        mongodb.insert_element_to_collection('apps_info', app_start_info_dict)

    # get the target result
    app_open_times_ratio = round((df.app_cnt.sum() / app_df1.app_cnt.sum()), 2)
    target_user_ratio = round((df.mac.drop_duplicates().count() / app_df.mac.count()), 2)
    target_user_app_ratio = round((df.mac.count() / app_df.mac.count()), 2)

    result_dict = {
            'date' : datetime.date(int(date_t[:4]), int(date_t[4:6]), int(date_t[6:])).strftime('%Y%m%d %a'), 
            'app_open_times_ratio' : app_open_times_ratio,
            'target_user_ratio' : target_user_ratio,
            'target_user_app_ratio' : target_user_app_ratio }
    print(result_dict)

    if write_mongo:
        print('#### start writing result_dict into mongoDB')
        mongodb.insert_element_to_collection('predict_ratio', result_dict)


def get_package_json(names : list):
    l = []
    for name in names:
        d = {'package_name' : name}
        # d = {'package_name' : name, 'start_time' : ''}
        l.append(d)

    res = {'packagelist' : l}
    return res

def update_mysql(date : str):
    start = datetime.datetime.now()
    print('#### write date into mysql')

    result_file = common.RESULT_DIR + date + common.RESULT_CSV_SUFFIX
    if not os.path.exists(result_file):
        print('%s doesnot exist', result_file)
        return

    apps = AppResult(result_file)
    app_df = apps.get_dataframe().set_index('mac')

    db_list = []
    for mac in app_df.index.drop_duplicates():

        l = []
        df = app_df.loc[mac]
        if len(df) == 1:
            l.append(df.app_name)
        else:
            l = df.app_name.tolist()
        
        res = get_package_json(l)
        db_list.append((mac, json.dumps(res)))

    print('#### get data time: ', datetime.datetime.now() - start)
    mysql = MySQL(host = common.SQL_SERVER, user = 'rom', pwd = '123456', db = common.SQL_DB)
    mysql.clear_fast_app()
    mysql.update_target_app(db_list = db_list)
    mysql.close()

    print('#### update sql time: ', datetime.datetime.now() - start)

def upload_result_to_server():
    parameters = {}
    parameters['ctime'] = str(int(time.time()))
    source = parameters['ctime'] + common.AUTH_SUFFIX
    parameters['sign'] = hashlib.md5(source.encode(encoding='UTF-8')).hexdigest()
    ret = requests.get(url=common.GET_URL, params = parameters)
    print('get : ', ret)

    headers = {}
    for root, dirs, files in os.walk(common.TARGET_RESULT_SPLIT_DIR):
        for file in files:
            file_name = common.TARGET_RESULT_SPLIT_DIR + file
            files = dict()
            files['file'] = open(file_name, 'rb')

            headers['fn'] = file_name
            source = file_name + common.AUTH_SUFFIX
            headers['auth'] = hashlib.md5(source.encode(encoding='UTF-8')).hexdigest()
            ret = requests.post(url=common.POST_URL, headers = headers, files = files)
            print(ret)

def generate_target_file(date : str):
    start = datetime.datetime.now()
    print('#### write date into file')

    result_file = common.RESULT_DIR + date + common.RESULT_CSV_SUFFIX
    if not os.path.exists(result_file):
        print('%s doesnot exist', result_file)
        return

    apps = AppResult(result_file)
    app_df = apps.get_dataframe().set_index('mac')

    db_list = []
    for mac in app_df.index.drop_duplicates():

        l = []
        df = app_df.loc[mac]
        if len(df) == 1:
            l.append(df.app_name)
        else:
            l = df.app_name.tolist()

        res = get_package_json(l)
        db_list.append([mac, json.dumps(res)])

    print('#### get data time: ', datetime.datetime.now() - start)

    if not os.path.exists(common.TARGET_RESULT_DIR):
        os.mkdir(common.TARGET_RESULT_DIR)
        os.mkdir(common.TARGET_RESULT_SPLIT_DIR)
    else:
        for root, dirs, files in os.walk(common.TARGET_RESULT_SPLIT_DIR):
            for file in files:
                os.remove(common.TARGET_RESULT_SPLIT_DIR + file)

    target_file = common.TARGET_RESULT_FILE + common.TARGET_RESULT_FILE_SUFFIX
    with open(target_file, 'w', newline = '') as f:
        for line in db_list:
            f.write(line[0] + ',')
            f.write(line[1] + '\n')

    with open(target_file, 'r') as f:
        num = 0
        f_name = common.TARGET_RESULT_SPLIT_FILE + str(num) + common.TARGET_RESULT_FILE_SUFFIX
        tmp_f = open(f_name, 'w')

        for line in f.readlines():
            tmp_f.write(line)
            if os.path.getsize(f_name) > common.TARGET_FILE_MAX_SIZE:
                num += 1
                f_name = common.TARGET_RESULT_SPLIT_FILE + str(num) + common.TARGET_RESULT_FILE_SUFFIX
                tmp_f = open(f_name, 'w')

    print('#### generate file time: ', datetime.datetime.now() - start)


if __name__ == '__main__':
    init_mongodb('localhost')
    # calculate_target_name_with_LRU_with_days('20181126', '20181127', update_result=True, day_num =1)
    # generate_target_file('20181212')
    upload_result_to_server()
    close_mongodb()