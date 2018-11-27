import hashlib
import os
import requests
import time
import zipfile
import gzip

sign = 'ecd3fed47446c971'

GZ_FILE = 'out.gz'
ZIP_FILE = 'out.zip'

def download_gz():
    #file_url = "http://qv.tv.funshion.com/millet/datapost/rom/data/start20181108.gz?sign=268188b1325cb6f1210f32f6b581e52a"
    if os.path.exists('csv_files/' + get_app_start_file_name()):
        return

    print('#### start downloading: ', get_app_start_file_name())

    file_url = 'http://qv.tv.funshion.com/millet/datapost/rom/data/' + get_download_app_file_name() + '?sign=' + getSign()
    r = requests.get(file_url, stream=True)

    with open(GZ_FILE, 'wb') as out:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                out.write(chunk)

    extract_gz_file()

def get_app_start_file_name():
    today = time.strftime('%Y%m%d', time.localtime())
    yesterday = int(today) -1
    return str(yesterday) + '-app.csv'

def get_download_app_file_name():
    today = time.strftime('%Y%m%d', time.localtime())
    yesterday = int(today) -1
    fileName = 'start' + str(yesterday) + '.gz'
    return fileName

def getSign():
    source = get_download_app_file_name() + sign
    md5 = hashlib.md5(source.encode(encoding='UTF-8')).hexdigest()
    return md5

def extract_gz_file():

    g_file = gzip.GzipFile(GZ_FILE)

    open('csv_files/' + get_app_start_file_name(), 'wb+').write(g_file.read())
    g_file.close()

    if os.path.exists(GZ_FILE):
        os.remove(GZ_FILE)

##=====================================

def downloadZip():

    file_url = 'http://qv.tv.funshion.com/millet/datapost/rom/data/' + getFileName() + '?sign=' + getSign()
    r = requests.get(file_url, stream=True)
    with open(ZIP_FILE, "wb") as out:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                out.write(chunk)

    extractZipFile()

def getPreFileName():
    today = time.strftime('%Y%m%d', time.localtime())
    yesterday = int(today) -1
    return 'appbootstrap' + str(yesterday) + '.zip'

def getFileName():
    today = time.strftime('%Y%m%d', time.localtime())
    yesterday = int(today) -1
    fileName = 'out' + str(yesterday) + '.zip'
    return fileName

def extractZipFile():
    zf = zipfile.ZipFile(os.path.join(os.getcwd(), ZIP_FILE))
    for file in zf.namelist():
        zf.extract(file, 'out/' + getPreFileName())
    zf.close()

    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)

if __name__ == '__main__':
    download_gz()
