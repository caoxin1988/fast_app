import pandas as pd
import numpy as np
import pymongo
import matplotlib.pyplot as plt

class Mongodb(object):
    def __init__(self, db_name : str, server_ip : str = 'localhost'):
        self.client = pymongo.MongoClient(server_ip, 27017)
        self.db = self.client[db_name]

    def close(self):
        self.client.close()

    def delete_all(self, collection : str):
        collec = self.db[collection]
        collec.delete_many({})

    def get_collection_dataframe(self, collection : str):
        collec = self.db[collection]
        df = pd.DataFrame(list(collec.find()))

        return df

    def insert_element_to_collection(self, collection : str, element : dict):
        collec = self.db[collection]
        collec.insert_one(element)


if __name__ == '__main__':
    # for test use but not import use
    mongodb = Mongodb('fast_app')

    df = mongodb.get_collection_dataframe('apps_info').drop(columns='_id').set_index('date')
    print(df)
    df.plot()
    # plt.xticks([1, 2, 3, 4, 5, 6, 7] ,df.index.tolist(), rotation = 70)
    plt.xticks(np.arange(len(df)), df.index.tolist(), rotation = 70)
    plt.show()