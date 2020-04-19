import os
import sys
import asyncio
import math
from flask import Blueprint, Flask, abort, jsonify, request
from flask_login import login_required

from common import my_log, login_tool, cache_tool

from . import main


o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
logger = my_log.LogUtil().getLogger()
from main import all_dbc


@asyncio.coroutine
@main.route('/project_list', methods=['get'])
@login_required
def project_list():
    username = login_tool.login_tools().get_username().decode('utf-8')
    xmmc = cache_tool.res_cache(username)
    if xmmc[0] == None:
        sql = "SELECT c_bh as xmbh,c_xmmc as xmmc,c_url as xmdz FROM db_apitesting.t_at_xmxx"
        sql_count = "SELECT count(1) as counts FROM db_apitesting.t_at_xmxx"
    else:
        xmmc = xmmc[0].replace(',', '\',\'')
        xmmc = '\'' + str(xmmc) + '\''
        sql = "SELECT c_bh as xmbh,c_xmmc as xmmc,c_url as xmdz FROM db_apitesting.t_at_xmxx WHERE c_url IN (%s)" % xmmc
        sql_count = "SELECT count(1) as counts FROM db_apitesting.t_at_xmxx WHERE c_url IN (%s)" % xmmc
    try:
        project_dict = {}
        res_list = all_dbc.pg_select_operator(sql)
        res_count = all_dbc.pg_select_operator(sql_count)
        project_dict['maxsize'] = res_count[0]['counts']
        project_dict['reslist'] = res_list
        return jsonify(project_dict)
    except Exception as eee:
        logger.error('项目列表接口报错：' + str(eee))
        return jsonify({'result': 'fail'})        




@asyncio.coroutine
@main.route('/index_rate', methods=['post'])
# @login_required
def index_rate():
    if not request.json or 'tjfs' not in request.json or 'limit' not in request.json:
        abort(400)
    # tjfs【统计方式】    1: 用例名称，2：项目名称，3：开发团队名称，4：测试团队名称
    tjfs = request.json['tjfs']
    limit = request.json['limit']
    if isinstance(limit, int):
        pass
    else:
        abort(400)
    if tjfs == 1:
        cov_rate_sql = "SELECT ylxx.c_ylmc AS type, Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2) AS value, concat(Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2), '%%') AS sold FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl WHERE zxxx.c_fgl NOT IN ('计算中', '异常中断，未计算', '不计算') GROUP BY ylxx.c_bh, ylxx.c_ylmc ORDER BY value ASC LIMIT %d;" % limit
        pass_rate_sql = "SELECT ylxx.c_ylmc AS type, Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2) AS value, concat(Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2), '%%') AS sold FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl GROUP BY ylxx.c_bh, ylxx.c_ylmc ORDER BY value ASC LIMIT %d;" % limit
    elif tjfs == 2:
        cov_rate_sql = "SELECT xmxx.c_xmmc AS type, aaa.avg_num AS value, aaa.sold_text as sold FROM (SELECT ylxx.c_bh_xm AS xmbh, Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2) AS avg_num, concat(Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2), '%%') AS sold_text FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl WHERE zxxx.c_fgl NOT IN ('计算中', '异常中断，未计算', '不计算') GROUP BY ylxx.c_bh_xm ORDER BY avg_num ASC LIMIT %d) aaa LEFT JOIN db_apitesting.t_at_xmxx xmxx ON aaa.xmbh = xmxx.c_bh ORDER BY aaa.avg_num ASC;" % limit
        pass_rate_sql = "SELECT xmxx.c_xmmc AS type, aaa.avg_num AS value, aaa.sold_text as sold FROM (SELECT ylxx.c_bh_xm AS xmbh, Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2) AS avg_num, concat(Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2), '%%') AS sold_text FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl GROUP BY ylxx.c_bh_xm ORDER BY avg_num ASC LIMIT %d) aaa LEFT JOIN db_apitesting.t_at_xmxx xmxx ON aaa.xmbh = xmxx.c_bh ORDER BY aaa.avg_num ASC;" % limit
    elif tjfs == 3:
        cov_rate_sql = "SELECT ylxx.c_code_team AS type, Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2) AS value, concat(Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2), '%%') AS sold FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl WHERE zxxx.c_fgl NOT IN ('计算中', '异常中断，未计算', '不计算') GROUP BY ylxx.c_code_team ORDER BY value ASC LIMIT %d;" % limit
        pass_rate_sql = "SELECT ylxx.c_code_team AS type, Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2) AS value, concat(Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2), '%%') AS sold FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl GROUP BY ylxx.c_code_team ORDER BY value ASC LIMIT %d;" % limit
    elif tjfs == 4:
        cov_rate_sql = "SELECT ylxx.c_test_team AS type, Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2) AS value, concat(Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2), '%%') AS sold FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl WHERE zxxx.c_fgl NOT IN ('计算中', '异常中断，未计算', '不计算') GROUP BY ylxx.c_test_team ORDER BY value ASC LIMIT %d;" % limit
        pass_rate_sql = "SELECT ylxx.c_test_team AS type, Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2) AS value, concat(Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2), '%%') AS sold FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl GROUP BY ylxx.c_test_team ORDER BY value ASC LIMIT %d;" % limit
    else:
        abort(400)
    try:
        cov_rate_res = all_dbc.pg_select_operator(cov_rate_sql)
        pass_rate_res = all_dbc.pg_select_operator(pass_rate_sql)
    except Exception as eee:
        logger.error('首页统计sql报错：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail', 'msg': str(eee)})
    if tjfs == 3 or tjfs == 4:
        for info_cov in cov_rate_res:
            try:
                name = cache_tool.res_cache(info_cov['type'])
            except:
                name = info_cov['type']
            info_cov['type'] = name[0]
        for info_pass in pass_rate_res:
            try:
                name = cache_tool.res_cache(info_pass['type'])
            except:
                name = info_pass['type']
            info_pass['type'] = name[0]
    return jsonify([cov_rate_res, pass_rate_res])




@asyncio.coroutine
@main.route('/run_times/<tjfs>', methods=['get'])
# @login_required
def run_times(tjfs):
    # tjfs【统计方式】    1: 用例名称，2：项目名称，3：开发团队名称，4：测试团队名称
    tjfs = int(tjfs)
    if tjfs == 1:
        run_times_sql = "SELECT ylxx.c_ylmc AS name, Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2) AS x, Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2) AS y, sum(ylxx.n_zxcs) AS z FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl WHERE zxxx.c_fgl NOT IN ('计算中', '异常中断，未计算', '不计算') GROUP BY ylxx.c_ylmc;"
    elif tjfs == 2:
        run_times_sql = "SELECT xmxx.c_xmmc AS name, aaa.avg_num_fg AS x, aaa.avg_num_tg AS y, aaa.times AS z FROM (SELECT ylxx.c_bh_xm AS xmbh, Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2) AS avg_num_fg, Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2) AS avg_num_tg, sum(ylxx.n_zxcs) AS times FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl WHERE zxxx.c_fgl NOT IN ('计算中', '异常中断，未计算', '不计算') GROUP BY ylxx.c_bh_xm) aaa LEFT JOIN db_apitesting.t_at_xmxx xmxx ON aaa.xmbh = xmxx.c_bh;"
    elif tjfs == 3:
        run_times_sql = "SELECT xmxx.c_code_team AS name, Round(AVG(aaa.avg_num_fg), 2) AS x, Round(AVG(aaa.avg_num_tg),2) AS y, sum(aaa.times) AS z FROM (SELECT ylxx.c_bh_xm AS xmbh, Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2) AS avg_num_fg, Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2) AS avg_num_tg, sum(ylxx.n_zxcs) AS times FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl WHERE zxxx.c_fgl NOT IN ('计算中', '异常中断，未计算', '不计算') GROUP BY ylxx.c_bh_xm) aaa LEFT JOIN db_apitesting.t_at_xmxx xmxx ON aaa.xmbh = xmxx.c_bh GROUP BY xmxx.c_code_team;"
    elif tjfs == 4:
        run_times_sql = "SELECT xmxx.c_test_team AS name, Round(AVG(aaa.avg_num_fg), 2) AS x, Round(AVG(aaa.avg_num_tg),2) AS y, sum(aaa.times) AS z FROM (SELECT ylxx.c_bh_xm AS xmbh, Round(AVG(CAST(LEFT(zxxx.c_fgl, -1) AS numeric)), 2) AS avg_num_fg, Round(AVG(CAST(LEFT(zxxx.c_tgl, -1) AS numeric)), 2) AS avg_num_tg, sum(ylxx.n_zxcs) AS times FROM db_apitesting.t_at_ylxx ylxx INNER JOIN db_apitesting.t_at_zxxx zxxx ON ylxx.c_bh = zxxx.c_bh_yl WHERE zxxx.c_fgl NOT IN ('计算中', '异常中断，未计算', '不计算') GROUP BY ylxx.c_bh_xm) aaa LEFT JOIN db_apitesting.t_at_xmxx xmxx ON aaa.xmbh = xmxx.c_bh GROUP BY xmxx.c_test_team;"
    else:
        abort(400)
    try:
        run_times_res = all_dbc.pg_select_operator(run_times_sql)
    except Exception as eee:
        logger.error('执行次数sql报错：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail', 'msg': str(eee)})
    if tjfs == 3 or tjfs == 4:
        for info_run in run_times_res:
            try:
                name = cache_tool.res_cache(info_run['name'])
            except:
                name = info_run['name']
            info_run['name'] = name[0]
    return jsonify(run_times_res)







