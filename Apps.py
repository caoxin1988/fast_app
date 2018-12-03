import pandas as pd
import matplotlib.pyplot as plt 
from pandas import Series

from Draw import Draw
import common
import http_download

class Apps(object):
    def __init__(self, date : str):
        file_name = common.CSV_DIR + date + common.APP_CSV_SUFFIX
        http_download.download_gz(date)

        print('====== read : ', file_name, 'start ======')
        data_frame = pd.read_csv(file_name, sep = '\t',
                                usecols=[0, 3, 13, 16], names=['stm', 'sid', 'app_name', 'mac'])
        data_frame.dropna(how = 'any', inplace = True)
        data_frame.mac = data_frame.mac.apply(lambda x : x.upper())
        # print(data_frame.shape)
        data_frame = data_frame[data_frame.mac.str.startswith('28:76:CD') | data_frame.mac.str.startswith('8C:6D:50') | data_frame.mac.str.startswith('18:89:A0')]
        data_frame.stm = pd.to_datetime(data_frame.stm + 28800, unit='s')

        data_frame = data_frame[(data_frame.app_name != 'tv.fun.marketshow') & 
                                (data_frame.app_name != 'com.funshion.poweroffdialog') &
                                (data_frame.app_name != 'com.cvte.tv.media') &
                                (data_frame.app_name != 'com.funshion.tvwifidisplay') &
                                (data_frame.app_name != 'com.toptech.localmm')]

        # print(data_frame.shape)
        self.draw = Draw()
        self.data_frame = data_frame

        # d = dict()
        # d['user_num'] = self.user_counts = data_frame.mac.value_counts().count()
        # d['app_start_times'] = self.app_open_times = data_frame.app_name.count()
        # d['average'] = d['app_start_times'] / d['user_num']
        # print('user and app num : ', d)

        self.app_numbers = data_frame.app_name.drop_duplicates().count()
        # print('app numbers : ', self.app_numbers)
        print('====== read : ', file_name, 'end ======')
        print('\n')

    def get_user_mac_set(self):
        return set(self.data_frame.mac.drop_duplicates().values.tolist())

    def get_dataframe(self):
        return self.data_frame

    def draw_app_names_pie(self):
        apps = self.data_frame.app_name.value_counts()
        # draw picture
        self.draw.draw_app_names_pie(apps, self.data_frame.app_name.count())

    def draw_app_by_person(self):
        users = self.data_frame.mac.value_counts()
        # draw picture
        self.draw.draw_app_open_times_pie_by_person(users, 'times')

        df = self.data_frame[['mac', 'app_name']].drop_duplicates()
        user_cnt = df.mac.value_counts()
        # how many apps opened per person
        self.draw.draw_app_open_times_pie_by_person(user_cnt, 'count')

    def app_graph_by_name(self, mac : str, app_name : str):
        print('%s users has opened %s' % (self.data_frame[self.data_frame.app_name == app_name].mac.value_counts().count(), app_name))

        df = self.data_frame[self.data_frame.mac == mac]
        print(df[df.app_name == app_name].head())
        print(df[df.app_name == app_name].shape)

        sessions = self.data_frame[(self.data_frame.mac == mac)].sid.drop_duplicates().count()
        print('user : %s has opened %s for %s times in %s different sessions' % \
                (mac, app_name, len(df[df.app_name == app_name]), sessions))

        apps = df.app_name.drop_duplicates()
        d = dict()
        for app in apps.values:
            cnt = len(df[df.app_name == app])
            d[app] = [cnt, sessions]
            print('user : %s has opened %s for %s times in %s different sessions' % \
                    (mac, app, cnt, sessions))

        pd.DataFrame(d, index = ['times', 'sessions']).T.plot(kind='bar')
        plt.show()

    def show_apps_by_highlight_user(self):
        df = self.data_frame[['mac', 'app_name']].drop_duplicates()
        user_cnt = df.mac.value_counts()
        users = self.data_frame.mac.value_counts()

        df= self.data_frame[['mac', 'app_name']]
        set1 = set(user_cnt[(user_cnt >= 1) & (user_cnt < 6)].index.tolist())
        set2 = set(users[users >= 10].index.tolist())
        highlight_user = set1 & set2
        print(len(set1), len(set2), len(highlight_user))
        df = df[df.mac.isin(highlight_user)]
        tmp = df.app_name.value_counts()
        highlight_app = set(tmp.head(20).index.tolist())
        print(tmp.shape)

        print(tmp.head(20))
        # draw picture
        self.draw.draw_bar(tmp.head(20), 'barh')
        
        # highlight users and highlight apps
        # for i in range(10):
        #     mac = highlight_user.pop()
        #     app_name = highlight_app.pop()
        #     print('===> ', mac, app_name)
        #     app_graph_by_name(mac, app_name)
