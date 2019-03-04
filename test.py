import datetime
import common
import shutil
import csv
import pandas as pd

from AppResult import AppResult
from User import User
from Apps import Apps

result_file = common.RESULT_DIR + '20181224' + common.RESULT_CSV_SUFFIX
result = AppResult(result_file)

result_df = result.get_dataframe()

result_user = result_df.mac.drop_duplicates().values

##  ========================  ##

def get_open_tv_user_set(days : int = 0):
    user_set = set()

    date_t = datetime.datetime.today() - datetime.timedelta(days=3)
    print(date_t.strftime('%Y%m%d'))

    for i in range(days, -1, -1):
        date_f = date_t - datetime.timedelta(days=i)
        print('date : ', date_f)
        user = User(date_f.strftime('%Y%m%d'))
        user_set |= user.get_user_mac_set()

    return user_set

user_set = get_open_tv_user_set(5)
result_user_set = set(result_user)

print(len(user_set))
print(len(result_user_set))

target_user = result_user_set - user_set
print(len(target_user))


app = Apps('20190101')
app_user = app.get_user_mac_set()

print(len(target_user & app_user))


def generate_new_target(user_set: set, result_df: pd.DataFrame):
    result_file = common.RESULT_DIR + '20181231' + common.RESULT_CSV_SUFFIX
    df = AppResult(result_file).get_dataframe()
    set1 = set(df.mac.drop_duplicates().values) - user_set
    df = df[df.mac.isin(set1)]
    print('1', len(df))
    print('1', len(df.mac.drop_duplicates()))


    result_df = result_df[result_df.mac.isin(user_set)]
    print('2', len(result_df))
    print('2', len(result_df.mac.drop_duplicates()))

    df = pd.concat([df, result_df])
    print('3', len(df))
    print('3', len(df.mac.drop_duplicates()))

    df.to_csv('test.csv', index=False)


generate_new_target(target_user, result_df)
