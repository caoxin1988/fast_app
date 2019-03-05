"""
# -*- coding: utf-8 -*-
# @Time    : 3/4/19 4:48 PM
# @Author  : Cao,Xin
# @Email   : caoxin1988s@gmail.com
# @File    : app_daily_info.py

"""

from mongoengine import connect, Document, StringField, IntField, \
            ListField, EmbeddedDocument, EmbeddedDocumentField


class AppInfo(EmbeddedDocument):
    app_name = StringField(max_length=100, required=True)
    app_open_time = IntField()


class UserInfo(Document):
    date = StringField(max_length=10, required=True)
    mac_addr = StringField(max_length=20, required=True)
    app_info = ListField(EmbeddedDocumentField(AppInfo))


def connect_mongo(dbname, host):
    connect(db=dbname, host=host)


if __name__ == '__main__':
    pass

    # connect(db='app_usage_info', host='localhost')
    #
    # app_info = AppInfo(app_name='tencent', app_open_time=0)
    # app_info1 = AppInfo(app_name='aiqiyi', app_open_time=3)
    #
    # UserInfo(date='20190228', mac_addr='abc', app_info=[app_info, app_info1]).save()
    #
    # UserInfo(date='20190303', mac_addr='efg', app_info=[app_info, app_info1]).save()

    results = UserInfo.objects
    print(len(results))
    print(results[0])

    print([result.date for result in results])
    # print(result.user_info.app_info.app_open_time)

else:
    # connect(db='app_usage_info', host='localhost')
    pass
