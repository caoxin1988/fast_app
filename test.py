import pandas as pd
import datetime
import sys

import common
from Apps import Apps
from AppResult import AppResult


def get_apps_with_days(date : datetime.datetime, day_num : int = 1) -> pd.DataFrame:
    df_app = None

    for num in range(day_num-1, -1, -1):
        date_target = date - datetime.timedelta(days=num)

        df_app1 = Apps(date_target.strftime('%Y%m%d')).get_dataframe()
        df_app1 = df_app1[['mac', 'app_name']].drop_duplicates()
        assert isinstance(df_app1, pd.DataFrame)

        df_app = pd.concat([df_app, df_app1]).drop_duplicates()

    return df_app

if __name__ == '__main__':
    print('#### today is :', datetime.datetime.today().strftime('%Y%m%d'), '\n'*2)

    yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')

    # get app start info of yesterday
    apps = Apps(yesterday)
    df_app = apps.get_dataframe()[['mac', 'app_name']].groupby('mac').agg({'app_name':'value_counts'}).rename(columns={'app_name':'app_cnt'})
    assert isinstance(df_app, pd.DataFrame)
    df_app.reset_index(inplace=True)

    total_of_today = df_app.app_cnt.sum()
    print('#### total of today: ', total_of_today)

    df = get_apps_with_days(datetime.datetime.today() - datetime.timedelta(days=2), day_num=14)


    df = pd.merge(df_app, df, on=['mac', 'app_name'])
    assert isinstance(df, pd.DataFrame)
    df = df.groupby(['mac', 'app_name']).agg({'app_cnt':'sum'})

    start = datetime.datetime.now()
    sum = 0
    for mac in df.index.levels[0]:
        df_sub = df.loc[mac]
        if len(df_sub) > 2:         # just for saving time
            df_sub = df_sub.sort_values(by='app_cnt', ascending=False)[:2]

        for app in df_sub.index:
            sum += df_sub.loc[app, 'app_cnt']

    print(sum, total_of_today)
    print(round(sum / total_of_today, 3))
    print('end : ', datetime.datetime.now() - start)