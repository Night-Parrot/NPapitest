'''
为了更好的在用例执行过程中调用各种不同的数据库，该方法提供统一的入口进行管理
上层调用时仅需传入需要执行的sql即可（【dbname: sql】，这种格式）
同时提供数据库创建连接的方法，调用时仅需要传入连接信息即可，格式参见用例模板的中的数据格式
'''

import re
import pypyodbc as pyodbc   # sybase用的
import psycopg2             # postgresql用的
import psycopg2.extras      # postgresql用的
import json

# from common import my_log, re_fun_for_web, base_tool

# logger = my_log.LogUtil().getLogger()


import pandas as pd



def read_dbinfo(file_path):
    try:
        df_dbinfo = pd.read_excel(
            file_path, sheet_name='db_config', keep_default_na=False)
    except Exception as eee:
        print(eee)
    db_info = {}
    for rows in df_dbinfo.index.values:
        row_data = df_dbinfo.loc[rows].to_dict()
        db_info[df_dbinfo.loc[rows, ['name']].values[0]] = row_data
    # df_keywords = df_keywords.reindex().to_dict()
    return db_info








def db_tool_connect(db_info):
    if len(db_info) == 0:
        # logger.info('用例中未读取到数据库配置信息')
        return False 
    db_connect = {}
    for name in db_info:
        database = db_info[name]['db_name']
        user = db_info[name]['db_user']
        password = db_info[name]['db_password']
        host = db_info[name]['db_ip']
        port = db_info[name]['db_port']
        if db_info[name]['db_type'].upper() == 'ABASE' or db_info[name]['db_type'].upper() == 'ARTERYBASE':
            try:
                db_fun = []
                build_db_for_commit = psycopg2.connect(
                    database=database, user=user, password=password, host=host, port=port)
                db_fun.append(build_db_for_commit)
                build_db_for_cur = build_db_for_commit.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor)
                db_fun.append(build_db_for_cur)
                db_fun.append(db_info[name]['db_type'].upper())
                db_connect[name] = db_fun
            except Exception as eee:
                # logger.error('创建用例内数据库连接的错误信息：' + str(eee))
                return False
        elif db_info[name]['db_type'].upper() == 'SYBASE':
            try:
                db_fun = []
                sy_conn = pyodbc.connect("DRIVER={Adaptive Server Enterprise};DATABASE=%s;SERVER=%s;PORT=%s;UID=%s;PWD=%s" % (database, host, port, user, password))
                db_fun.append(sy_conn)
                cur = sy_conn.cursor()
                db_fun.append(cur)
                db_fun.append(db_info[name]['db_type'].upper())
                db_connect[name] = db_fun
            except Exception as eee:
                # logger.error('创建sybase的错误信息：' + str(eee))
                return False
        else:
            pass
    return db_connect


def db_close(db_info):
    print('开始关闭')
    for db_name in db_info:
        # db_info[db_name][0].close()
        db_info[db_name][1].close()
    print('完成')
    return True

if __name__ == '__main__':
    path = 'D:\\download_edge\\111.xlsx'
    res = read_dbinfo(path)
    # print(res)
    db_c = db_tool_connect(res)
    print(db_c)
    sql = "SELECT C_MC as MC,C_BH as bh, '5000' as time FROM T_ZX_DSR WHERE C_BH = '02491B0C9B4B8C9D5667E65A13E0C5BA'" # 一个查询SQL
    # print(db_c['jyhzx'][2])
    print(db_c['jyhzx'][1])
    db_c['zxba'][1].execute(sql)
    bbb = db_c['zxba'][1].fetchall()
    print(bbb)