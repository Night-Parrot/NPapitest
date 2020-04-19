import os, sys
o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
from common import my_log
logger = my_log.LogUtil().getLogger()


from main import app, all_dbc, cache_local
import socket


'''
获取本机IP的方法，将本机ip放到缓存中
'''
def get_host_ip():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
  finally:
    s.close()
  return ip


'''
创建缓存，从数据库查询出用户与项目的对照关系
[{'user': 'q', 'xm': 'T3C-ssf,T3E-jyhzx'}, {'user': 'lianglei', 'xm': 'test_pro,T3E-jyhzx,T3C-ssf'}]
'''
def add_cache():
    with app.app_context():
        cache_local.clear()
    user_xm_sql = "SELECT c_username as user, c_xmxx as xm, c_name as name FROM db_apitesting.t_zx_user;"
    user_xm = all_dbc.pg_select_operator(user_xm_sql)
    org_info_sql = "SELECT c_bh AS id, c_mc AS mc, c_pid AS pid FROM db_apitesting.t_at_org;"
    org_info = all_dbc.pg_select_operator(org_info_sql)
    org_pid_sql = "SELECT c_bh AS id, c_pid AS pid FROM db_apitesting.t_at_org ORDER BY c_pid;"
    org_pid = all_dbc.pg_select_operator(org_pid_sql)
    if len(org_pid) != 0:
        org_group = {}
        for info in org_pid:
            if info['pid'] == '':
                org_group[info['id']] = []
            elif info['pid'] not in org_group.keys():
                org_group[info['pid']] = [info['id']]
            else:
                org_group[info['pid']].append(info['id'])
                # org_group[info['pid']] = org_group[info['pid']].append(info['id'])
        # for info in org_group:
        with app.app_context():
            cache_local.set('org_group', org_group)
    if len(org_info) != 0:
        for info in org_info:
            with app.app_context():
                cache_local.set(info['id'], [info['mc'], info['pid']])
    # logger.info(str(user_xm))
    logger.info('··开始加载用户信息缓存···' + str(cache_local))
    if len(user_xm) != 0:
        for info in user_xm:
            with app.app_context():
                cache_local.set(info['user'], [info['xm'], info['name']])
    with app.app_context():
        cache_local.set('localip', get_host_ip())
        logger.info('···用户缓存加载完毕···' + str(cache_local))
        logger.info(cache_local.get('q'))


def res_cache(name):
    with app.app_context():
        try:
            name = name.decode('utf-8')
        except Exception as e:
            logger.error(e)
        logger.error('key名：' + str(name))
        value = cache_local.get(name)
        logger.info('缓存：' + str(value))
        return value


def new_cache(key, value, timeout = ''):
    with app.app_context():
        try:
            if timeout == '':
                cache_local.set(key, value)
            else:
                cache_local.set(key, value, timeout=timeout)
            return True
        except Exception as eee:
            logger.error('新增缓存失败：' + str(eee))
            return False

def del_cache(key):
    with app.app_context():
        try:
            cache_local.delete(key)
            return True
        except Exception as eee:
            logger.error('删除缓存失败：' + str(eee))
            return False




add_cache()