import pandas as pd
import matplotlib.pyplot as plt 

import config.common as common
from utils.http_download import DownloadGZ


class Apps(object):
    def __init__(self, date : str):
        file_name = common.CSV_DIR + date + common.APP_CSV_SUFFIX
        DownloadGZ.download_gz(date)

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
        return set(self.data_frame.mac.drop_duplicates().values)

    def get_dataframe(self):
        return self.data_frame


if __name__ == '__main__':
    app = Apps('20190101')
    print(app.get_dataframe().head())

