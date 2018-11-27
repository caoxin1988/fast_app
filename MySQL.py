import pymysql

class MySQL(object):
    def __init__(self, host : str, user : str, pwd : str, db : str):
        self.db = pymysql.connect(host, user, pwd, db, charset='utf8')

    def close(self):
        self.db.close()

    def clear_fast_app(self):
        cur = self.db.cursor(cursor = pymysql.cursors.DictCursor)

        cur.execute('delete from fast_app')
        self.db.commit()
        cur.close()

    def search_fast_app(self, mac : str):
        cur = self.db.cursor(cursor = pymysql.cursors.DictCursor)

        sql = 'select * from fast_app where mac = %s'
        count = cur.execute(sql, mac)

        data = cur.fetchall()
        print(data)

        cur.close()

    def update_target_app(self, mac : str, data : str):
        cur = self.db.cursor(cursor = pymysql.cursors.DictCursor)
        # search first
        sql = 'select * from fast_app where mac = %s'
        count = cur.execute(sql, mac)
        if count == 0:
            cur.execute('insert into fast_app(mac, content) VALUES(%s, %s)', (mac, data))
        else:
            cur.execute('update fast_app set content = %s where mac = %s', (data, mac))
        
        self.db.commit()
        cur.close()
        

if __name__ == '__main__':
    mysql = MySQL(host = '172.17.7.26', user = 'rom', pwd = '123456', db = 'rom_charts')
    # mysql.search_fast_app('abc')

    mysql.update_target_app('abc', 'xyz')
    mysql.update_target_app('lmn', 'xyz11')

    mysql.clear_fast_app()

    mysql.close()
