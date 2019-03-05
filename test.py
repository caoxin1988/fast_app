"""
# -*- coding: utf-8 -*-
# @Time    : 3/4/19 1:39 PM
# @Author  : Cao,Xin
# @Email   : caoxin1988s@gmail.com
# @File    : test.py.py

"""

import datetime
from collections import defaultdict, Counter
import pandas as pd

from utils.Apps import Apps
import config.common as common

mac_addr_sets = {'18:89:A0:03:60:4D', '18:89:A0:03:5F:F4', '8C:6D:50:79:88:7A'}


def get_app_data_by_user(days):
    """
    get app usage data by mac addr within some days from today
    :param
        days: day numbers we want to read csv files
        mac: mac addr of target user\

    :return:
        dict: key: mac_addr; value: dict: key -> app name
                                          value -> list of app open times
    """
    def app_graph():
        return defaultdict(lambda: [0] * days)

    user_app_graph = defaultdict(app_graph)

    today_date = datetime.datetime.today()

    for day in range(days, 0, -1):
        date_str = (today_date - datetime.timedelta(days=day)).strftime(common.DATE_FORMAT)
        df = Apps(date_str).get_dataframe()
        assert isinstance(df, pd.DataFrame)

        df = df.groupby('mac').apply(lambda x: Counter(x.app_name))

        for mac in df.index:
            if mac not in mac_addr_sets:
                continue

            for app_name in df[mac]:
                user_app_graph[mac][app_name][days - day] = df[mac][app_name]

    print(user_app_graph)


if __name__ == '__main__':

    days = 20

    get_app_data_by_user(days)
