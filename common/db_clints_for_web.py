import re

import psycopg2
import psycopg2.extras
import json
import pypyodbc as pyodbc

from common import my_log, re_fun_for_web, base_tool

logger = my_log.LogUtil().getLogger()



def db_clints(db_info):
    if len(db_info) == 0:
        logger.info('用例中未读取到数据库配置信息')
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
                logger.error('创建abase的错误信息：' + str(eee))
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
                logger.error('创建sybase的错误信息：' + str(eee))
                return False
        else:
            pass
    return db_connect





class db_tools(object):

    def __init__(self, sql_list='', db_clints='', keyv=''):
        self.sql_list = sql_list
        self.db_clints = db_clints
        self.keyv = keyv

    def front_back_sql_run(self):
        false_num = 0
        for sql_dict in self.sql_list:
            for db_clint_name in sql_dict:
                try:
                    # sql = re_fun_for_web.re_fun_sql(sql_dict[db_clint_name], self.keyv)
                    sql = str(base_tool.replace_for_web(sql_dict[db_clint_name], self.keyv)).replace('\\', '')
                    cur = self.db_clints[db_clint_name][1]
                    cur.execute(str(sql).replace('\n', ''))
                    self.db_clints[db_clint_name][0].commit()
                except Exception as e:
                    logger.error("这是个数据库异常" +str(e))
                    self.db_clints[db_clint_name][0].rollback()
                finally:
                    false_num = false_num + 1
        if false_num != 0:
            return False
        else:
            return True

    def res_sql_run(self):
        sqlinfo = {}
        for sql_dict in self.sql_list:
            for db_clint_name in sql_dict:
                try:
                    # 添加复杂dict结构的封装，针对sql查询结果不在json第一层的情况  11-4  
                    # sql的dict传入的时候结构为{"db_name(dict_name)": "sql主体"}
                    # 需要对key值再做拆分，并将分离出来的dict_name作为sqlinfo的key值进行补充
                    # 我太难了
                    cf_dict = re.findall((r'(\w+)'), db_clint_name) #拆分步骤，分解完后是['db_name', 'dict_name']
                    if len(cf_dict) == 2:
                        # sql = re_fun_for_web.re_fun_sql(sql_dict[db_clint_name], self.keyv)
                        sql = str(base_tool.replace_for_web(sql_dict[db_clint_name], self.keyv)).replace('\\', '')
                        cur = self.db_clints[cf_dict[0]][1]
                        cur.execute(sql)
                        r = cur.fetchall()
                        '''
                        这里需要判断sql执行的数据库是否为sybase，如果是的话，需要调用转换dict的方法
                        '''
                        if self.db_clints[cf_dict[0]][2] == 'SYBASE':
                            r = base_tool.row_name(sql, r)
                        # 如果查询结果为多条,则直接返回多条的list,如果有指定的key名,则封装到key内
                        # 这样的话,就没办法处理list的合并,所以,如果要匹配多条记录,则必须在一条sql内查询出所有的验证字段
                        if isinstance(r, list) and len(r) != 1:
                            # sqlinfo[cf_dict[1]] = json.dumps(r, ensure_ascii=False)
                            sqlinfo[cf_dict[1]] = r
                        else:
                            if cf_dict[1] in sqlinfo.keys():
                                sqlinfo[cf_dict[1]] = {**sqlinfo[cf_dict[1]][0], **r[0]}
                                sqlinfo[cf_dict[1]] = [sqlinfo[cf_dict[1]]]
                            else:
                                sqlinfo[cf_dict[1]] = {**{}, **r[0]}
                    elif len(cf_dict) == 1:
                        # sql = re_fun_for_web.re_fun_sql(sql_dict[db_clint_name], self.keyv)
                        sql = str(base_tool.replace_for_web(sql_dict[db_clint_name], self.keyv)).replace('\\', '')
                        cur = self.db_clints[db_clint_name][1]
                        cur.execute(sql)
                        r = cur.fetchall()
                        sqlinfo = {**sqlinfo, **r[0]}
                    else:
                        return False
                except Exception as ee:
                    logger.error(ee)
                    pass
        if len(str(sqlinfo)) == 0:
            return False
        else:
            return sqlinfo

    def db_close(self):
        for db_name in self.db_clints:
            self.db_clints[db_name][1].close()
        return True
