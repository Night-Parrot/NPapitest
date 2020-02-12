import os
import sys
import asyncio
from flask import Blueprint, Flask, abort, jsonify, request
import math

from common import my_log


from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()
from main import all_dbc

@asyncio.coroutine
@main.route('/ylzx_info/<zxid>/<pagenum>', methods=['get'])
def ylzx_info(zxid, pagenum): #列表查询，返回总页数、总条数、每页数，支持状态参数
    zxid = zxid
    pagenum = pagenum
    zt = request.args.get('zt') # 1：全部, 2：请求成功, 3：请求失败, 4：验证通过, 5：验证失败
    gjz = request.args.get('gjz') # 查询用的关键字
    if zt == '1':
        tj = ''
    elif zt == '2':
        tj = " AND n_jkzt = '200'"
    elif zt == '3':
        tj = " AND n_jkzt != '200'"
    elif zt == '4':
        tj = " AND c_yzjg != '不通过'"
    elif zt == '5':
        tj = " AND c_yzjg = '不通过'"
    else:
        return jsonify({'result': 'fail', 'msg': '参数不正确'})
    sql_zt = "SELECT n_zt as zt, c_jd as jd FROM db_apitesting.t_at_zxxx WHERE c_bh = '%s';" % zxid
    sql_num_base = "SELECT count(1) as counts FROM db_apitesting.t_at_qqxx WHERE c_bh_zx = '%s'" % zxid
    sql_allnum_base = "SELECT count(1) as counts FROM db_apitesting.t_at_qqxx WHERE c_bh_zx = '%s'" % zxid
    sql_num_base_cg = "SELECT count(1) as counts FROM db_apitesting.t_at_qqxx WHERE c_bh_zx = '%s' AND n_jkzt = '200'" % zxid
    sql_num_base_tg = "SELECT count(1) as counts FROM db_apitesting.t_at_qqxx WHERE c_bh_zx = '%s' AND c_yzjg != '不通过'" % zxid
    sql_base = "SELECT c_bh as key, n_qqmc as name, c_qqdz as url, c_xysj as xysj, to_char(dt_zxsj, 'yyyy-mm-dd hh24:mi:ss') as zxsj, "\
                "n_jkzt as jkzt, c_yzjg as yzjg, c_qqcs as cs, c_yqfhz as yqfhz, c_sjfhz as sjfhz, c_matchinfo as matchinfo "\
                "FROM db_apitesting.t_at_qqxx WHERE c_bh_zx = '%s'" % zxid
    like_text = " and n_qqmc like '%s'" % str("%" + gjz + "%")
    paga = " order by n_xh LIMIT 10 OFFSET " + str((int(pagenum)-1) * 10)
    if len(gjz) == 0:
        sql_allnum = sql_allnum_base
        sql_num = sql_num_base + tj
        sql_all = sql_base + tj + paga
        sql_num_cg = sql_num_base_cg
        sql_num_tg = sql_num_base_tg
    else:
        sql_allnum = sql_allnum_base + like_text
        sql_num = sql_num_base + tj + like_text
        sql_all = sql_base + tj + like_text + paga
        sql_num_cg = sql_num_base_cg + like_text
        sql_num_tg = sql_num_base_tg + like_text
    try:
        list_allnum = all_dbc.pg_select_operator(sql_allnum)
        list_con = all_dbc.pg_select_operator(sql_num)
        list_all = all_dbc.pg_select_operator(sql_all)
        list_cg = all_dbc.pg_select_operator(sql_num_cg)
        list_tg = all_dbc.pg_select_operator(sql_num_tg)
        zx_nt = all_dbc.pg_select_operator(sql_zt)
    except Exception as eee:
        logger.error(eee)
        return jsonify({'result': 'fial', 'msg': str(eee)})
    project_dict = {}
    project_dict['zt'] = zx_nt[0]['zt']
    project_dict['jd'] = zx_nt[0]['jd']
    project_dict['maxpage'] = math.ceil(list_con[0]['counts']/10)
    project_dict['maxsize'] = list_con[0]['counts']
    data_list = [list_allnum[0]['counts'], list_cg[0]['counts'], int(list_allnum[0]['counts'])-int(list_cg[0]['counts']),
                                 list_tg[0]['counts'], int(list_allnum[0]['counts'])-int(list_tg[0]['counts'])]
    for idx, val in enumerate(data_list):
        if val < 0:
            data_list[idx] = 0
    project_dict['counts'] = data_list
    project_dict['nowpage'] = int(pagenum)
    for info in list_all:
        re_name = ['key', 'cs', 'yqfhz', 'sjfhz', 'matchinfo']
        re_dict = {}
        for n in re_name:
            re_dict[n] = info[n]
            if n != 'key':
                del info[n]
        info['innerlist'] = [re_dict]
    project_dict['reslist'] = list_all
    return jsonify(project_dict)