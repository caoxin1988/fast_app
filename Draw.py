import matplotlib.pyplot as plt
import tkinter
from pandas import Series
import pandas as pd
import math

class Draw(object):
    def __init__(self):
        pass

    def draw_app_names_pie(self, apps : Series, count : int):
        if apps.count() > 19:
            tmp = apps[:19].append(Series({'others' : count - apps[:19].sum()}))
            tmp.name = ''
            tmp.plot.pie(autopct = '%.2f')
        else:
            apps.name = ''
            apps.plot.pie(autopct = '%.2f')
        
        plt.title('app open ratio(%)')
        plt.show()

        print('====' * 10, '\n')
        app_num = apps.count()
        app_times = apps.sum()
        app_max = apps.max()
        app_min = apps.min()
        print('app number: %s, app open times: %s, app max open times: %s, app min open times: %s' %
                (app_num, app_times, app_max, app_min))
        print('\n')

        max_len = len(str(app_max))
        d = dict()
        while max_len > 0:
            if max_len == len(str(app_max)):
                min = int(math.pow(10, max_len-1))
                max = int(app_max)
            else:
                min = int(math.pow(10, max_len-1))
                max = int(math.pow(10, max_len))

            d['[' + str(min) + ', ' + str(max) + ']'] = apps[(apps >= min) & (apps <= max)].count()
            max_len -= 1

        print(d)
        Series(d, name = '').plot(kind='pie', autopct = '%.2f')
        plt.title('app open times ratio')
        plt.show()


    def get_app_start_times_per_person(self, s : Series, r : str):
        user_count = s.count()
        user_max =s.max()
        user_min =s.min()

        print('user counts : ', user_count)
        if r == 'times':
            print('max user open times by user : ', user_max)
            print('min user open times by user : ', user_min)
        elif r == 'count':
            print('max user open counts by user : ', user_max)
            print('min user open counts by user : ', user_min)

        max_len = len(str(user_max))
        user_cnt = dict()

        while max_len > 0:
            if max_len == len(str(user_max)):
                min = int(math.pow(10, max_len-1))
                max = user_max
            else:
                min = int(math.pow(10, max_len-1))
                max = int(math.pow(10, max_len))

                if max_len == 1 and r == 'count':
                    user_cnt['[1, 3]'] = s[(s >= 1) & (s < 3)].count()
                    user_cnt['[3, 6]'] = s[(s >= 3) & (s < 6)].count()
                    user_cnt['[6, 10]'] = s[(s >= 6) & (s < 10)].count()

            if max_len == 1 and r == 'count':
                break
            else:
                user_cnt['[' + str(min) + ', ' + str(max) + ']'] = s[(s >= min) & (s <= max)].count()

            max_len -= 1

        return user_cnt


    def draw_app_open_times_pie_by_person(self, s : Series, r : str):
        user_cnt = self.get_app_start_times_per_person(s, r)
        print(user_cnt)
        Series(user_cnt, name = '').plot(kind='pie', autopct = '%.2f')
        if r == 'times':
            plt.title('app open times by person')
        elif r == 'count':
            plt.title('app open counts by person')
        plt.show()


    def draw_bar(self, d : dict):
        # d = {'user' : [100], 'app' : [20], 'average' : [5]}
        data_frame = pd.DataFrame(d, index=['cnt'])
        print(data_frame)

        data_frame.plot(kind='bar')
        plt.show()