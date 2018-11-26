# set target apps for target users with LRU

import pandas as pd
from pandas import Series
import datetime
import os

import common
from MySQL import MySQL
from Mongodb import Mongodb
from Apps import Apps

day_num = 0
mysql = None
mongodb = None

def set_days(num : int):
    global day_num
    day_num = num

'''operations for mysql'''
def init_mysql():
    global mysql
    mysql = MySQL(host = common.SQL_SERVER, user = 'rom', pwd = '123456', db = common.SQL_DB)

def close_mysql():
    global mysql
    mysql.close()

'''operations for mongodb'''
def init_mongodb(server : str):
    global mongodb
    mongodb =  Mongodb(db_name = common.MONGO_DB, server_ip = server)

def delete_all_data(collec : str):
    mongodb.delete_all(collec)

def close_mongodb():
    mongodb.close()

'''algothrims for  '''
def calculate_target_name_with_LRU(date_p : str, date_t : str, write_mongo : bool = False,
                    write_mysql : bool = False):

    app_file_p = common.CSV_DIR + date_p + common.APP_CSV_SUFFIX
    app_file_t = common.CSV_DIR + date_t + common.APP_CSV_SUFFIX

    if not os.path.exists(app_file_p) or not os.path.exists(app_file_t):
        file_name = app_file_p if os.path.exists(app_file_t) else app_file_t
        print('%s does not exist, please check, exit', file_name)
        return

    # data from former day
    apps = Apps(app_file_p)

    app_df = common.remove_duplicates_of_app(apps)
    app_df = app_df[['mac', 'app_name']]
    print('1', app_df.shape)

    # merge the data from former day
#     date_f = datetime.date(int(date_p[:4]), int(date_p[4:6]), int(date_p[6:])) - datetime.timedelta(days = 1)
#     apps = Apps(CSV_DIR + date_f.strftime('%Y%m%d') + APP_CSV_SUFFIX)
#     app_df_f = remove_duplicates_of_app(apps)
#     app_df_f = app_df_f[['mac', 'app_name']]
#     print(app_df_f.shape)

#     app_df = pd.concat([app_df, app_df_f], ignore_index = True)
#     print(app_df.shape)

#     app_df.drop_duplicates(inplace = True)
#     print(app_df.shape)

    # data for target day
    apps = Apps(app_file_t)
    app_df1 = apps.get_dataframe()
    app_df1 = app_df1[['mac', 'app_name']].groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
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
        mongodb.insert_element_to_collection('predict_ratio', result_dict)

if __name__ == '__main__':
    init_mongodb()
    calculate_target_name_with_LRU('20181119', '20181120')
    # app_start_info_dict = {'date': '20181118 Sun', 'app_start_times': 434575, 'user_count_apps': 127219, 'app_counts': 1999}
    # mongodb.insert_element_to_collection('apps_info', app_start_info_dict)
    close_mongodb()