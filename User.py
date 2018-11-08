import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt

class User(object):

    def __init__(self):
        df = pd.read_csv('./daily.csv', sep = '\t' , usecols = [1, 2],
                                        names = ['mac', 'cnt'])
        df.dropna(how = 'any', inplace = True)

        df = df[df.mac.str.startswith('2876CD') | df.mac.str.startswith('8C6D50') | df.mac.str.startswith('1889A0')]
        df = df.groupby('mac').cnt.sum().reset_index()
        df.mac = df.mac.apply(lambda x : ':'.join([x[:2], x[2:4], x[4:6], x[6:8], x[8:10], x[10:]]))
        print(df.head())
        print(df.mac.describe())
        self.data_frame = df

    def user_open_times(self):
        print(self.data_frame.cnt.describe())
        d = dict()
        d['[1000 : ]'] = self.data_frame.cnt[self.data_frame.cnt >= 1000].count()
        d['[500 : 1000]'] = self.data_frame.cnt[(self.data_frame.cnt >= 500) & (self.data_frame.cnt < 1000)].count()
        d['[100 : 500]'] = self.data_frame.cnt[(self.data_frame.cnt >= 100) & (self.data_frame.cnt < 500)].count()
        d['[ : 100]'] = self.data_frame.cnt[self.data_frame.cnt < 100].count()
        print(d)
        Series(d, name= '').plot(kind='pie', autopct = '%.2f')
        plt.title('user start tv ratio')
        plt.show()

    def calculate_app_start_ratio(self, s : Series):
        pass

    def get_user_mac_set(self):
        return set(self.data_frame.mac.values.tolist())

# user = User()
        