"""
# -*- coding: utf-8 -*-
# @Time    : 3/6/19 1:17 PM
# @Author  : Cao,Xin
# @Email   : caoxin1988s@gmail.com
# @File    : data_precessing.py

"""

import datetime
from collections import defaultdict, Counter
import pandas as pd

from utils.Apps import Apps
import config.common as common

mac_addr_sets = {'18:89:A0:03:60:4D', '18:89:A0:03:5F:F4', '8C:6D:50:79:88:7A'}

class DataProcessing:
    """
    preocess data with csv files
    """
    def __init__(self, days, bulk):
        """
        :param
            days: the data of days to get
            bulk: organize days with bulk
        """
        self.days = days
        self.bulk = bulk

    def __get_app_data_by_user(self):
        """
        get app usage data by mac addr within some days from today
        :param
            days: day numbers we want to read csv files
            mac: mac addr of target user

        :return:
            dict: key: mac_addr; value: dict: key -> app name
                                              value -> list of app open times
        """
        days = self.days

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

        # print(user_app_graph)
        return user_app_graph

    def __get_latest_cnt(self, l):
        cnt = 0

        for i in range(len(l)-1, -1, -1):
            if l[i] == 0 and cnt != 0:
                return cnt
            else:
                cnt += l[i]

        return cnt

    def transform_data(self, mac_addr):
        """
        transform data with bulks

        :return:
            matrix X: features matrix[seq: whole_cnt, latest_continues_cnt, cnt_of_yestersay, label]
        """
        bulk = self.bulk
        days = self.days

        user_app_graph = self.__get_app_data_by_user()
        features_label = []

        # why (days-1)? : data of yesterday can only be label
        for end_index in range(bulk-1, days-1):
            start_index = end_index + 1 - bulk
            apps_dict = user_app_graph[mac_addr]
            print(apps_dict, )

            for app_name in apps_dict:
                count_list = apps_dict[app_name]
                whole_cnt = sum(count_list[start_index:end_index+1])
                latest_continues_cnt = self.__get_latest_cnt(count_list)
                cnt_of_yesterday = count_list[end_index]
                label = 1 if count_list[end_index+1] > 0 else 0
                features_label.append([whole_cnt, latest_continues_cnt, cnt_of_yesterday, label])

        print(features_label)

        return features_label


if __name__ == '__main__':
    data_processing = DataProcessing(10, 4)

    data_processing.transform_data('18:89:A0:03:60:4D')
