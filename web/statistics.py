import os
import sys
import asyncio
import math
from flask import Blueprint, Flask, abort, jsonify, request

from common import my_log, login_tool, cache_tool

from . import main


o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
logger = my_log.LogUtil().getLogger()
from main import all_dbc


@asyncio.coroutine
@main.route('/update_time_order', methods=['get'])
def update_time_order():
    '''
    获取更新时间最靠前的5个项目
    '''
    sql_time_order = "SELECT ylxx.c_bh AS key, xmxx.c_xmmc AS name, ylxx.c_ylmc AS ylmc, to_char(ylxx.dt_gxsj, 'yyyy-mm-dd hh24:mi:ss') AS time FROM db_apitesting.t_at_ylxx ylxx,db_apitesting.t_at_xmxx xmxx WHERE ylxx.c_bh_xm = xmxx.c_bh AND ylxx.dt_gxsj IS NOT NULL ORDER BY ylxx.dt_gxsj DESC LIMIT 5;"
    try:
        project_dict = all_dbc.pg_select_operator(sql_time_order)
        return jsonify(project_dict)
    except Exception as eee:
        logger.error('项目列表接口报错：' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})        



@asyncio.coroutine
@main.route('/run_time_order', methods=['get'])
def run_time_order():
    '''
    获取执行时间最靠前的5个项目
    '''
    sql_time_order = "SELECT aaa.c_bh AS key, xmxx.c_xmmc AS name, aaa.c_ylmc AS ylmc, aaa.c_tgl AS tgl, aaa.c_fgl AS fgl, aaa.time FROM (SELECT zxxx.c_bh, ylxx.c_bh_xm, ylxx.c_ylmc, zxxx.c_fgl, zxxx.c_tgl, to_char(zxxx.dt_zxsj, 'yyyy-mm-dd hh24:mi:ss') AS time FROM db_apitesting.t_at_zxxx zxxx LEFT JOIN db_apitesting.t_at_ylxx ylxx ON zxxx.c_bh_yl = ylxx.c_bh WHERE zxxx.dt_zxsj IS NOT NULL AND zxxx.n_zt > '0' ORDER BY zxxx.dt_zxsj DESC LIMIT 5) aaa LEFT JOIN db_apitesting.t_at_xmxx xmxx ON aaa.c_bh_xm = xmxx.c_bh ORDER BY aaa.time DESC;"
    try:
        project_dict = all_dbc.pg_select_operator(sql_time_order)
        return jsonify(project_dict)
    except Exception as eee:
        logger.error('项目列表接口报错：' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})