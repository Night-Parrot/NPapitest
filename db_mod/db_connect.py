import configparser
import datetime
import os
import sys
import re
import psycopg2
import psycopg2.extras
import uuid


from DBUtils.PooledDB import PooledDB


o_path = os.getcwd()
sys.path.append(o_path)
from common import my_log




logger = my_log.LogUtil().getLogger()


config = configparser.ConfigParser()
config.read('./config.ini')
host = config.get('db_connect', 'host')
port = config.get('db_connect', 'port')
username = config.get('db_connect', 'username')
password = config.get('db_connect', 'password')
database = config.get('db_connect', 'database')

class My_dbc(object):

    def __init__(self):
        self._pool = None


    def get_pool_conn(self):
        if not self._pool:
            self.init_pgsql_pool()
        return self._pool.connection()

    def init_pgsql_pool(self):
        try:
            logger.info('Begin to create {0} postgresql pool on：{1}.\n'.format(host, datetime.datetime.now()))
            pool = PooledDB(
                creator=psycopg2,  # 使用链接数据库的模块mincached
                maxconnections=50,  # 连接池允许的最大连接数，0和None表示不限制连接数
                mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached=10,  # 链接池中最多闲置的链接，0和None不限制
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
                setsession=[],  # 开始会话前执行的命令列表。
                host=host,
                port=port,
                user=username,
                password=password,
                database=database)
            self._pool = pool
            logger.info('SUCCESS: create postgresql success')
        except Exception as e:
            logger.error('ERROR: create postgresql pool failed')
            # self.close_db_cursor()
            logger.error('ERROR: create postgresql pool error caused by: ' + str(e))

    def pg_select_operator(self, sql):
        sqlinfo = {}
        reslist = []
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql)
            rs = cursor.fetchall()
        except Exception as e:
            logger.error('ERROR: execute  {0} causes error'.format(sql))
            logger.error('ERROR: load data from database error caused ：' + str(e))
            rs = []
        finally:
            cursor.close()
            conn.close()
        if len(rs) != 1:
            for num in range(len(rs)):
                sqlinfo = dict(sqlinfo, **rs[num])
                reslist.append(sqlinfo)
            return reslist
        if len(rs) == 0:
            return rs
        else:
            for num in range(len(rs)):
                sqlinfo = dict(sqlinfo, **rs[num])
            if len(re.findall('None', str(sqlinfo))) == len(sqlinfo):
                return []
            reslist.append(sqlinfo)
            return reslist


    def pg_insert_operator(self, sql):
        result = False
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result =  True
        except Exception as e:
            logger.error('ERROR: execute  {0} causes error'.format(sql))
            logger.error('ERROR: insert data from database error caused ：' + str(e))
        finally:
            cursor.close()
            conn.commit()
            conn.close()
        return result

    def pg_update_operator(self, sql):
        result = False
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result =  True
        except Exception as e:
            logger.error('ERROR: execute  {0} causes error'.format(sql))
            logger.error('ERROR: update data from database error caused ：' + str(e))
        finally:
            cursor.close()
            conn.commit()
            conn.close()
        return result

    def pg_delete_operator(self, sql):
        result = False
        # 执行查询
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result =  True
        except Exception as e:
            logger.error('ERROR: execute  {0} causes error'.format(sql))
            logger.error('ERROR: delete data from database error caused ：' + str(e))
        finally:
            cursor.close()
            conn.commit()
            conn.close()
        return result

    def close_pool(self):
        if self._pool != None:
            self._pool.close()




if __name__ == '__main__':
    ylbh = 'c383ac2b65a9413da9ed1d0d4b9b35cd'
    lj_sql = "1111SELECT c_bclj as yllj FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s';" % ylbh
    md = My_dbc()
    res = md.pg_select_operator(lj_sql)
    # res2 = md.pg_select_operator(lj_sql)
    print(res)