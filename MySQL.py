import pymysql

class MySQL(object):
    def __init__(self, host : str, user : str, pwd : str, db : str):
        self.db = pymysql.connect(host, user, pwd, db, charset='utf8')

    def close(self):
        self.db.close()

    def clear_fast_app(self):
        cur = self.db.cursor()

        cur.execute('truncate fast_app')
        cur.close()

    def search_fast_app(self, mac : str):
        cur = self.db.cursor(cursor = pymysql.cursors.DictCursor)

        sql = 'select * from fast_app where mac = %s'
        count = cur.execute(sql, mac)

        data = cur.fetchall()
        print(data)

        cur.close()

    def update_target_app(self, **dictargs):
        mac = None
        data = None
        db_list = None

        for item in dictargs.keys():
            if item == 'mac':
                mac = dictargs['mac']
            elif item == 'data':
                data = dictargs['data']
            elif item == 'db_list':
                db_list = dictargs['db_list']

        if not db_list and (not mac or not data):
            print('return')
            return

        cur = self.db.cursor()
        if db_list:
            cur.executemany('insert into fast_app(mac, content) VALUES(%s, %s);', db_list)
        
        if mac and data:
            cur.execute('insert into fast_app(mac, content) VALUES(%s, %s)', (mac, data))
        
        self.db.commit()
        cur.close()
        

if __name__ == '__main__':
    mysql = MySQL(host = '172.17.7.26', user = 'rom', pwd = '123456', db = 'rom_charts')
    # mysql.search_fast_app('abc')

    # mysql.update_target_app('abc', 'xyz')

    # mysql.clear_fast_app()
    mysql.update_target_app(db_list = [('abc', 'xyz')])
    # mysql.clear_fast_app()

    mysql.close()

