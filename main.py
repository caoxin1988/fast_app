import pandas as pd
from pandas import Series
import time
import datetime
import re

data_frame = None

#  convert timestamp to human time
def convert_time(t : int):
    return datetime.datetime.fromtimestamp(t)


def read_csv_file():
    data_frame = pd.read_csv('./query_result_month.csv')
    tmp = [None] * len(data_frame.columns)
    for i in range(0, len(data_frame.columns)-1):
        tmp[i] = data_frame.columns[i][10:]

    data_frame.columns = Series(tmp)
    print(data_frame.columns)

    macaddr_set = set()
    for item in data_frame['mac']:
        pattern = re.compile(r'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}')
        res = re.match(pattern, str(item))
        if res is not None:
            macaddr_set.add(item.lower())

def main():
    read_csv_file()

if __name__ == '__main__':
    main()

# test = data_frame[data_frame.app_name.str.startswith('com.ktcp.video')][['stm', 'mac', 'app_name']]
# print(test)
