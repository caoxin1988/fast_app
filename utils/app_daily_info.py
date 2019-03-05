"""
# -*- coding: utf-8 -*-
# @Time    : 3/5/19 9:47 AM
# @Author  : Cao,Xin
# @Email   : caoxin1988s@gmail.com
# @File    : app_daily_info.py.py

"""
from model.mongoDB.user_app_info import UserInfo, AppInfo, \
                UserInfo, connect_mongo
from collections import defaultdict


class AppDailyInfo:
    """
    read and write daily third app infos into mongoDB
    """
    def __init__(self, dbname, host):
        connect_mongo(dbname, host)

    def get_app_usage_info(self, date: str):
        """
        get app usage info of target date
        :param
            date: date str
        :return:
            dict: key: mac_addr; value: dict: key -> app name
                                              value -> app open counts
        """

        user_app_graph = defaultdict(dict)

        results = UserInfo.objects(date=date)

        if len(results) != 0:
            for user_info in results:
                mac_addr = user_info.mac_addr
                for app_info in user_info.app_info:
                    app_name, app_count = app_info.app_name, app_info.app_open_time
                    user_app_graph[mac_addr][app_name] = app_count
        else:
            return None

        return user_app_graph

    def write_app_usage_info(self, date: str, usage_data: dict):
        """
        write app usage info of target date into mongodb
        :param:
            date: date str
            usage_data: dict: key: mac_addr; value: dict: key -> app name
                                                          value -> app open counts
        :return:
            True : for write datebase success
        """
        if self.__check_is_saved(date):
            return True
        else:   # save data into mongodb here

            for mac_addr in usage_data:
                app_names = usage_data[mac_addr]

                app_info_list = [AppInfo(app_name, app_names[app_name]) for app_name in app_names]
                UserInfo(date=date, mac_addr=mac_addr, app_info=app_info_list).save()

            return True

    def __check_is_saved(self, date: str):
        results = UserInfo.objects(date=date)

        return len(results) != 0


'''
class AppInfo(EmbeddedDocument):
    app_name = StringField(max_length=100, required=True)
    app_open_time = IntField()


class UserInfo(Document):
    date = StringField(max_length=10, required=True)
    mac_addr = StringField(max_length=20, required=True)
    app_info = ListField(EmbeddedDocumentField(AppInfo))
'''