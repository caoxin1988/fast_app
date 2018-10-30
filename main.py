import pandas as pd
from pandas import Series
import time
import datetime

#  convert timestamp to human time
def convert_time(t : int):
    return datetime.datetime.fromtimestamp(t)



data_frame = pd.read_csv('./3rd_app_data.csv')
# a = data_frame[data_frame['app_start.stm'].str.starswith('154')]
tmp = [None] * len(data_frame.columns)
for i in range(0, len(data_frame.columns)-1):
    tmp[i] = data_frame.columns[i][10:]

data_frame.columns = Series(tmp)

test = data_frame[data_frame.stm > 1540744146][['stm', 'app_name']]
print(test)


print(convert_time(1540878669))
