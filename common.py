# common function for algothrims
import os

CSV_DIR = './csv_files/'
APP_CSV_SUFFIX = '-app.csv'
USER_CSV_SUFFIX = '-start.csv'

RESULT_DIR = './result/'
RESULT_CSV_SUFFIX = '-result.csv'
TARGET_NUM = 2

SQL_SERVER = '172.17.7.26'
SQL_DB = 'rom_charts'

MONGO_DB = 'fast_app'

if __name__ == '__main__':
    pass
else:
    if not os.path.exists('result'):
        print('#### mkdir result')
        os.mkdir('result')