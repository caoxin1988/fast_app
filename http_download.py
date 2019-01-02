import hashlib
import os
import requests
import datetime
import time
import zipfile
import gzip
import shutil

import common

sign = 'ecd3fed47446c971'

class DownloadGZ:
    GZ_FILE = 'out.gz'

    @classmethod
    def download_gz(cls, date : str):
        #file_url = "http://qv.tv.funshion.com/millet/datapost/rom/data/start20181108.gz?sign=268188b1325cb6f1210f32f6b581e52a"
        local_file = common.CSV_DIR + cls.__get_app_start_file_name(date)

        if os.path.exists(local_file) and os.path.getsize(local_file) != 0:
            return

        source_file = common.HIVE_DIR + cls.__get_download_app_file_name(date)
        if os.path.exists(source_file):
            print('#### copy : ', source_file)
            shutil.copy(source_file, cls.GZ_FILE)
        else:
            print('#### start downloading: ', cls.__get_app_start_file_name(date))

            file_url = 'http://qv.tv.funshion.com/millet/datapost/rom/data/' + \
                cls.__get_download_app_file_name(date) + '?sign=' + cls.__getSign(date)
            r = requests.get(file_url, stream=True)

            with open(cls.GZ_FILE, 'wb') as out:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        out.write(chunk)

        cls.__extract_gz_file(date)

    @classmethod
    def __get_app_start_file_name(cls, date : str):
        return date + common.APP_CSV_SUFFIX

    @classmethod
    def __get_download_app_file_name(cls, date : str):
        fileName = 'start' + date + '.gz'
        return fileName

    @classmethod
    def __getSign(cls, date : str):
        source = cls.__get_download_app_file_name(date) + sign
        md5 = hashlib.md5(source.encode(encoding='UTF-8')).hexdigest()
        return md5

    @classmethod
    def __extract_gz_file(cls, date : str):

        g_file = gzip.GzipFile(cls.GZ_FILE)

        open(common.CSV_DIR + cls.__get_app_start_file_name(date), 'wb+').write(g_file.read())
        g_file.close()

        if os.path.exists(cls.GZ_FILE):
            os.remove(cls.GZ_FILE)

##=====================================

class DownlaodZip:
    ZIP_FILE = 'out.zip'

    @classmethod
    def download_zip(cls, date:str):

        file_url = 'http://qv.tv.funshion.com/millet/datapost/rom/data/' + cls.__get_download_user_file_name(date) + '?sign=' + cls.__getSign(date)

        local_file = common.CSV_DIR + cls.__get_user_file_name(date)

        if os.path.exists(local_file) and os.path.getsize(local_file) != 0:
            return

        print('#### start downloading: ', cls.__get_user_file_name(date))
        r = requests.get(file_url, stream=True)
        with open(cls.ZIP_FILE, "wb") as out:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    out.write(chunk)

        cls.__extractZipFile(date)

    @classmethod
    def __get_user_file_name(cls, date:str):
        return date + common.USER_CSV_SUFFIX

    @classmethod
    def __get_download_user_file_name(cls, date:str):
        return 'appbootstrap' + date + '.zip'

    @classmethod
    def __getSign(cls, date : str):
        source = cls.__get_download_user_file_name(date) + sign
        md5 = hashlib.md5(source.encode(encoding='UTF-8')).hexdigest()
        return md5

    @classmethod
    def __extractZipFile(cls, date:str):
        with zipfile.ZipFile(os.path.join(os.getcwd(), cls.ZIP_FILE)) as zf, \
                open(common.CSV_DIR + cls.__get_user_file_name(date), 'wb') as f:
            for file in zf.infolist():
                shutil.copyfileobj(zf.open(file.filename), f)


        if os.path.exists(cls.ZIP_FILE):
            os.remove(cls.ZIP_FILE)

if __name__ == '__main__':
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    # DownloadGZ.download_gz(date.strftime('%Y%m%d'))
    DownlaodZip.download_zip('20190101')

else:
    if not os.path.exists('csv_files/'):
        print('#### mkdir csv_files')
        os.mkdir('csv_files')
