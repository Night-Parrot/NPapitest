import os, re
import sys
import asyncio
from flask import Blueprint, Flask, abort, jsonify, request, make_response
from flask_login import login_required
import math

from common import my_log, login_tool, cache_tool


from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()
from main import all_dbc


@asyncio.coroutine
@main.route('/<xmurl>/zx_list/<pagenum>', methods=['get'])
@login_required
def zx_list(xmurl, pagenum): #执行列表查询，返回总页数、总条数、每页数据
    username = login_tool.login_tools().get_username().decode('utf-8')
    xmmc = cache_tool.res_cache(username)
    logger.info(xmmc)
    if xmmc[0] == None:
        xmmc_list = {}
    else:
        xmmc_list = re.split(r',', xmmc[0])
    if xmurl in xmmc_list or xmmc[0] == None:
        sql_list = "SELECT zx.c_bh as zxbh,yl.c_ylmc as ylmc,to_char(zx.dt_zxsj, 'yyyy-mm-dd hh24:mi:ss') as zxsj,zx.c_cgl as cgl,zx.c_fgl as fgl,zx.c_tgl as tgl, c_sfci AS zxfs "\
            "FROM db_apitesting.t_at_zxxx zx LEFT JOIN db_apitesting.t_at_ylxx yl ON zx.c_bh_yl = yl.c_bh LEFT JOIN db_apitesting.t_at_xmxx xm ON yl.c_bh_xm = xm.c_bh "\
                "WHERE xm.c_url = '%s' ORDER BY zx.dt_zxsj DESC, zx.c_bh DESC LIMIT %s OFFSET %s;" % (xmurl, 10, (int(pagenum) - 1)*10)
        sql_count = "SELECT count(1) as counts "\
            "FROM db_apitesting.t_at_zxxx zx LEFT JOIN db_apitesting.t_at_ylxx yl ON zx.c_bh_yl = yl.c_bh LEFT JOIN db_apitesting.t_at_xmxx xm ON yl.c_bh_xm = xm.c_bh "\
                "WHERE xm.c_url = '%s';" % xmurl
        try:
            project_dict = {}
            res_list = all_dbc.pg_select_operator(sql_list)
            res_count = all_dbc.pg_select_operator(sql_count)
            project_dict['maxpage'] = math.ceil(res_count[0]['counts']/10)
            project_dict['maxsize'] = res_count[0]['counts']
            project_dict['nowpage'] = int(pagenum)
            project_dict['reslist'] = res_list
            return jsonify(project_dict)
        except Exception as eee:
            logger.error(eee)
            return jsonify({'result': 'fail'})
    else:
        abort(403)




@asyncio.coroutine
@main.route('/zx_list/del_zx', methods=['post'])
@login_required
def zx_del(): #执行记录删除
    if not request.json or 'zxbh' not in request.json:
        abort(400)
    delzxbh = request.json['zxbh']
    sql_del_zx = "DELETE FROM db_apitesting.t_at_zxxx WHERE c_bh = '%s';" % delzxbh #删除zxxx主表的数据
    sql_del_qq = "DELETE FROM db_apitesting.t_at_qqxx WHERE c_bh_zx = '%s';" % delzxbh #删除qqxx子表的数据
    try:
        for sql in [sql_del_qq, sql_del_zx]:
            all_dbc.pg_delete_operator(sql)
        return jsonify({'result': 'success'})
    except Exception as eee:
        logger.error(eee)
        return jsonify({'result': 'fail'})




@asyncio.coroutine
@main.route('/zx_list/<zxbh>', methods=['get'])
@login_required
def zx_info(zxbh): #执行详细
    sql_info = "SELECT c_fgl as fgl, c_cgl as cgl, c_tgl as tgl FROM db_apitesting.t_at_zxxx WHERE c_bh = '%s';" % zxbh
    try:
        res_list = all_dbc.pg_select_operator(sql_info)
        return jsonify(res_list)
    except Exception as eee:
        logger.error(eee)
        return jsonify({'result': 'fail'})




@asyncio.coroutine
@main.route('/zx_list/<zxbh>/<pagenum>', methods=['get'])
@login_required
def zx_qqxx_list(zxbh, pagenum): #请求信息列表查询，返回总页数、总条数、每页数据
    sql_list = "SELECT n_xh as xh, n_qqmc as mc, c_qqdz as dz, c_xysj as xysj,to_char(zx.dt_zxsj, 'yyyy-mm-dd hh24:mi:ss') as zxsj, n_jkzt as jkzt, c_yzjg as jzjg, "\
        "c_qqcs as qqcs, c_yqfhz as yqfhz, c_sjfhz as sjfhz FROM db_apitesting.t_at_qqxx "\
            "WHERE c_bh_zx = '%s' ORDER BY n_xh ASC LIMIT %s OFFSET %s;" % (zxbh, 10, (int(pagenum) - 1)*10)
    sql_count = "SELECT count(1) as counts FROM db_apitesting.t_at_qqxx "\
            "WHERE c_bh_zx = '%s';" % zxbh
    try:
        project_dict = {}
        res_list = all_dbc.pg_select_operator(sql_list)
        res_count = all_dbc.pg_select_operator(sql_count)
        project_dict['maxpage'] = math.ceil(res_count[0]['counts']/10)
        project_dict['maxsize'] = res_count[0]['counts']
        project_dict['nowpage'] = int(pagenum)
        project_dict['reslist'] = res_list
        return jsonify(project_dict)
    except Exception as eee:
        logger.error(eee)
        return jsonify({'result': 'fail'})