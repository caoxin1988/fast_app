# common function for algothrims

from Apps import Apps

CSV_DIR = './csv_files/'
APP_CSV_SUFFIX = '-app.csv'
USER_CSV_SUFFIX = '-start.csv'

RESULT_DIR = './result/'
RESULT_CSV_SUFFIX = '-result.csv'
TARGET_NUM = 2

SQL_SERVER = '172.17.7.26'
SQL_DB = 'rom_charts'

MONGO_DB = 'fast_app'

def remove_duplicates_of_app(apps: Apps):
    app_df = apps.get_dataframe()
    app_df = app_df[['sid', 'app_name', 'mac']].drop_duplicates()[['app_name', 'mac']]
    app_df = app_df.groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
    app_df = app_df.reset_index()

    return app_df