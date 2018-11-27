import pandas as pd
import matplotlib.pyplot as plt 
from pandas import Series

class AppResult(object):
    def __init__(self, file_name : str):
        print('====== read : ', file_name, 'start ======')
        data_frame = pd.read_csv(file_name, names=['mac', 'app_name'])

        self.data_frame = data_frame
        print('====== read : ', file_name, 'end ======')
        print('\n')

    def get_dataframe(self):
        return self.data_frame
