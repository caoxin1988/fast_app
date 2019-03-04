import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt
from http_download import DownlaodZip
import common

class User(object):

    def __init__(self, date : str):
        file_name = common.CSV_DIR + date + common.USER_CSV_SUFFIX
        DownlaodZip.download_zip(date)

        print('====== read : ', file_name, 'start ======')
        df = pd.read_csv(file_name, sep = '\t' , usecols = [1, 2],
                                        names = ['mac', 'open_cnt'])
        df.dropna(how = 'any', inplace = True)

        df = df[df.mac.str.startswith('2876CD') | df.mac.str.startswith('8C6D50') | df.mac.str.startswith('1889A0')]
        df = df.groupby('mac').open_cnt.sum().reset_index()
        df.mac = df.mac.apply(lambda x : ':'.join([x[:2], x[2:4], x[4:6], x[6:8], x[8:10], x[10:]]))
        print(df.head())
        print('user numbers : ', df.mac.count())
        print('start tv times : ', df.open_cnt.sum())
        self.data_frame = df
        print('====== read : ', file_name, ' end ======')
        print('\n')

    def user_open_times(self):
        print(self.data_frame.open_cnt.describe())
        d = dict()
        d['[1000 : ]'] = self.data_frame.open_cnt[self.data_frame.open_cnt >= 1000].count()
        d['[500 : 1000]'] = self.data_frame.open_cnt[(self.data_frame.open_cnt >= 500) & (self.data_frame.open_cnt < 1000)].count()
        d['[100 : 500]'] = self.data_frame.open_cnt[(self.data_frame.open_cnt >= 100) & (self.data_frame.open_cnt < 500)].count()
        d['[ : 100]'] = self.data_frame.open_cnt[self.data_frame.open_cnt < 100].count()
        print(d)
        Series(d, name= '').plot(kind='pie', autopct = '%.2f')
        plt.title('user start tv ratio')
        plt.show()

    def get_user_dataframe(self):
        return self.data_frame

    def get_user_mac_set(self):
        return set(self.data_frame.mac.values)

if __name__ == '__main__':
    user = User('20190101')