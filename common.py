# common function for algothrims
import os

CSV_DIR = './csv_files/'
APP_CSV_SUFFIX = '-app.csv'
USER_CSV_SUFFIX = '-start.csv'

RESULT_DIR = './result/'
RESULT_CSV_SUFFIX = '-result.csv'
TARGET_NUM = 2

TARGET_RESULT_DIR = './fast_app_result/'
TARGET_RESULT_SPLIT_DIR = TARGET_RESULT_DIR + 'split/'
TARGET_RESULT_FILE = TARGET_RESULT_DIR + 'target_result'
TARGET_RESULT_SPLIT_FILE = TARGET_RESULT_SPLIT_DIR + 'target_result-'
TARGET_RESULT_FILE_SUFFIX = '.txt'

TARGET_FILE_MAX_SIZE = 1000 * 1024
# POST_URL = 'http://172.17.5.73:8080/api/v1/rom-data'
POST_URL = 'http://172.17.12.130:8580/master-admin/api/v1/rom-data'
# GET_URL = 'http://172.17.5.73:8080/api/v1/clear/rom-data'
GET_URL = 'http://172.17.12.130:8580/master-admin/api/v1/clear/rom-data'
AUTH_SUFFIX = 'file-setting-log-upload'

HIVE_DIR = './hive_run_data/'

SQL_SERVER = '172.17.7.26'
SQL_DB = 'rom_charts'

MONGO_DB = 'fast_app'

if __name__ == '__main__':
    pass
else:
    if not os.path.exists('result'):
        print('#### mkdir result')
        os.mkdir('result')