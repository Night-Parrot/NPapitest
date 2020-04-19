import asyncio
import datetime
import json
import os
import sys, re, math
from flask_login import login_required

from flask import (Blueprint, Flask, abort, jsonify, request)

from common import my_log, login_tool, cache_tool, base_tool, run_caselist_new, panda_for_web, db_clints_for_web
from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()
from main import all_dbc




@asyncio.coroutine
@main.route('/<xmurl>/ci_list/<pagenum>', methods=['get'])
@login_required
def ci_list(xmurl, pagenum):
    ci_list_sql = "SELECT ci.c_bh AS key,ci.c_api AS url, ci.c_zxcs AS times, ci.c_ylsl AS ylsl, to_char(ci.dt_zxdysj, 'yyyy-mm-dd hh24:mi:ss') AS zxdysj, 0 AS ck, 0 AS bj FROM db_apitesting.t_at_xmxx xm left join db_apitesting.t_at_ci ci on xm.c_bh = ci.c_bh_xm WHERE xm.c_url = '%s' ORDER BY ci.dt_cjsj DESC LIMIT %s OFFSET %s;" % (xmurl, 5, (int(pagenum) - 1)*5)
    ci_list_count_sql = "SELECT count(1) AS counts FROM db_apitesting.t_at_xmxx xm right join db_apitesting.t_at_ci ci on xm.c_bh = ci.c_bh_xm WHERE xm.c_url = '%s';" % xmurl
    try:
        ci_list_res = all_dbc.pg_select_operator(ci_list_sql)
        ci_list_count_res = all_dbc.pg_select_operator(ci_list_count_sql)
    except Exception as eee:
        logger.error('CI列表信息查询失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    if ci_list_count_res[0]['counts'] == 0:
        return jsonify({'maxpage': 0,'maxsize': 0,'nowpage': 0,'reslist':[]})
    else:
        ci_list = {}
        ci_list['maxpage'] = math.ceil(ci_list_count_res[0]['counts']/5)
        ci_list['maxsize'] = ci_list_count_res[0]['counts']
        ci_list['nowpage'] = int(pagenum)
        ci_list['reslist'] = ci_list_res
        return jsonify(ci_list)





@asyncio.coroutine
@main.route('/<xmurl>/ci_yl_list', methods=['get'])
@login_required
def ci_yl_list(xmurl):
    yl_list_sql = "SELECT yl.c_bh AS key, yl.c_ylmc AS title FROM db_apitesting.t_at_xmxx xm left join db_apitesting.t_at_ylxx yl on xm.c_bh = yl.c_bh_xm WHERE xm.c_url = '%s';" % xmurl
    try:
        yl_list_res = all_dbc.pg_select_operator(yl_list_sql)
    except Exception as eee:
        logger.error('CI用例信息查询失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    return jsonify(yl_list_res)





@asyncio.coroutine
@main.route('/ci_info/<ci_id>', methods=['get'])
@login_required
def ci_info(ci_id):
    yl_list_sql = "SELECT c_yl_list AS list, c_api AS api FROM db_apitesting.t_at_ci WHERE c_bh = '%s';" % ci_id
    try:
        yl_list_res = all_dbc.pg_select_operator(yl_list_sql)
    except Exception as eee:
        logger.error('CI详情信息查询失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    yl_list = re.split(',', str(yl_list_res[0]['list']))
    if len(yl_list) == 0:
        return jsonify({'result': 'fail'})
    else:
        yl_info = str(yl_list)[1:-1]
        yl_info_sql = "SELECT c_bh AS key, c_ylmc AS title FROM db_apitesting.t_at_ylxx WHERE c_bh IN (%s);" % yl_info
        try:
            yl_info_res = all_dbc.pg_select_operator(yl_info_sql)
        except Exception as eee:
            logger.error('CI详情信息查询失败：' + str(eee))
            logger.exception(eee)
            return jsonify({'result': 'fail'})
        res_dic = {}
        res_dic['result'] = 'success'
        res_dic['api_linux'] = com_spl(yl_list_res[0]['api'])
        res_dic['api_docker'] = ''
        res_dic['res_list'] = yl_info_res
        return jsonify(res_dic)




@asyncio.coroutine
@main.route('/del_ci/<ci_id>', methods=['delete'])
@login_required
def del_ci(ci_id):
    del_sql = "DELETE FROM db_apitesting.t_at_ci WHERE c_bh = '%s';" % ci_id
    try:
        all_dbc.pg_delete_operator(del_sql)
    except Exception as eee:
        logger.error('CI信息删除失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    return jsonify({'result': 'success'})




@asyncio.coroutine
@main.route('/add_ci', methods=['post'])
@login_required
def add_ci():
    if not request.json or 'xmurl' not in request.json or 'ylinfo' not in request.json:
        abort(400)
    xmurl = request.json['xmurl']
    ylinfo = request.json['ylinfo']
    if len(ylinfo) == 0:
        return jsonify({'result': 'fail'})
    xm_id_sql = "SELECT c_bh AS xm_id FROM db_apitesting.t_at_xmxx WHERE c_url = '%s';" % xmurl
    try:
        xm_id_res = all_dbc.pg_select_operator(xm_id_sql)
    except Exception as eee:
        logger.error('CI项目编号查询失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    ci_id = base_tool.next_id()
    api_url = '/apitest/ci_control/' + ci_id
    ci_sql = "INSERT INTO db_apitesting.t_at_ci(c_bh, c_api, c_yl_list, dt_zxdysj, c_zxcs, c_bh_xm, c_ylsl, dt_cjsj) VALUES"\
        " ('%s', '%s', '%s', NULL, '0', '%s', '%s', now());" % (ci_id, api_url, ",".join(ylinfo), xm_id_res[0]['xm_id'], len(ylinfo))
    try:
        all_dbc.pg_insert_operator(ci_sql)
    except Exception as eee:
        logger.error('CI项目创建失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    return jsonify({'result': 'success'})



@asyncio.coroutine
@main.route('/update_ci', methods=['patch'])
@login_required
def update_ci():
    if not request.json or 'ci_key' not in request.json or 'ylinfo' not in request.json:
        abort(400)
    ci_key = request.json['ci_key']
    ylinfo = request.json['ylinfo']
    if len(ylinfo) == 0:
        return jsonify({'result': 'fail'})
    ci_up_sql = "UPDATE db_apitesting.t_at_ci SET c_yl_list = '%s', c_ylsl = '%s', dt_cjsj = now() WHERE c_bh = '%s';" % (",".join(ylinfo), len(ylinfo), ci_key)
    logger.info(ci_up_sql)
    try:
        all_dbc.pg_update_operator(ci_up_sql)
    except Exception as eee:
        logger.error('CI项目更新失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    return jsonify({'result': 'success'})



@asyncio.coroutine
@main.route('/ci_control/<ci_id>', methods=['post'])
def ci_run(ci_id):
    if not request.json:
        logger.error('CI调用失败，请求参数' + str(request))
        abort(400)
    cs_info = request.json
    yl_list_sql = "SELECT c_yl_list AS list FROM db_apitesting.t_at_ci WHERE c_bh = '%s';" % ci_id
    try:
        yl_list_res = all_dbc.pg_select_operator(yl_list_sql)
    except Exception as eee:
        logger.error('CI执行用例查询失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    if len(yl_list_res) == 0 or len(yl_list_res[0]['list']) == 0:
        return jsonify({'result': 'fail', 'msg': 'CI设置不存在或绑定用例为空'})
    else:
        yl_list = re.split(',', yl_list_res[0]['list'])
        for yl_id in yl_list:
            ylinfo_sql = "SELECT c_bclj as yllj, c_api_count AS api_docs FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s';" % yl_id
            yl_cs_sql = "SELECT c_key AS key, c_value AS value FROM db_apitesting.t_at_zxcs WHERE c_bh_yl = '%s';" % yl_id
            try:
                ylinfo_res = all_dbc.pg_select_operator(ylinfo_sql)
                yl_cs_res = all_dbc.pg_select_operator(yl_cs_sql)
            except Exception as eee:
                logger.error('CI执行查询用例路径失败：' + str(eee))
                logger.exception(eee)
                return jsonify({'result': 'fail'})
            new_kv = {}
            logger.info(str(yl_cs_res))
            for cs in yl_cs_res:
                new_kv[cs['key']] = cs['value']
            if len(ylinfo_res) != 1:
                return jsonify({'result': 'fail', 'msg': '用例可能已经不存在了'})
            else:
                yl_path = ylinfo_res[0]['yllj']
                api_docs = ylinfo_res[0]['api_docs']
                if str(api_docs) == 'null' or api_docs == '':
                    api_docs = ''
                try:
                    sfjs = cs_info['sfjs']
                    if str(sfjs) == '0':
                        sfjs = True
                    else:
                        sfjs = False
                except:
                    sfjs = False
                try:
                    case_info_all = panda_for_web.read_case(yl_path)
                except Exception as eee:
                    logger.error('用例读取失败：' + str(eee))
                    return jsonify({'result': 'fail', 'msg': '用例文件不存在或用例内容不正确，请重新上传'})
                if case_info_all == False:
                    return jsonify({'result': 'fail', 'msg': '用例文件不存在或用例内容不正确，请重新上传'})
                case_info_all.insert(0, new_kv)
                try:
                    db_case = db_clints_for_web.db_clints(case_info_all[2])
                except Exception as eee:
                    return jsonify({'result': 'fail', 'msg': str(eee)})
                if db_case == False:
                    return jsonify({'result': 'fail', 'msg': '数据库连接创建失败，请检查用例中的数据库配置'})
                logger.info("开始关闭数据链接")
                db_clints_for_web.db_tools().db_close()
                logger.info("完成关闭数据链接")
                zx_num = "UPDATE db_apitesting.t_at_ylxx SET n_zxcs = n_zxcs + 1 WHERE c_bh = '%s';" % yl_id
                try:
                    all_dbc.pg_update_operator(zx_num)
                except Exception as eee:
                    logger.error('更新执行次数失败' + str(eee))
                    return jsonify({'result': 'fail'})
                zxid = base_tool.next_id()
                zxjl_sql = "INSERT INTO db_apitesting.t_at_zxxx(c_bh, c_bh_yl, dt_zxsj, c_fgl, c_cgl, c_tgl, n_zt, c_cg, c_wcg, c_tg, c_wtg, c_sfci) VALUES"\
                            " ('%s', '%s', now(), '0%', '0%', '0%', 0, 0, 0, 0, 0, 0);" % (zxid, yl_id)
                try:
                    all_dbc.pg_insert_operator(zxjl_sql)
                except Exception as eee:
                    logger.error('新增执行信息失败' + str(eee))
                    return jsonify({'result': 'fail'})
                logger.info('···开始调用线程池···')
                logger.info(str(sfjs) + str(zxid) + str(api_docs))
                run_caselist_new.run_caselist(zxid, yl_id, case_info_all, api_docs, sfjs, cs_info)
                logger.info('···调用线程池完毕···')
        ci_up_sql = "UPDATE db_apitesting.t_at_ci SET c_zxcs = c_zxcs + 1, dt_zxdysj = now() WHERE c_bh = '%s';" % ci_id
        try:
            all_dbc.pg_update_operator(ci_up_sql)
        except Exception as eee:
            logger.error('更新CI信息失败' + str(eee))
            logger.exception(eee)
            return jsonify({'result': 'fail'})
        return jsonify({'result': 'success', 'msg': 'CI执行成功'})

        

@asyncio.coroutine
@main.route('/sql/<yl_id>', methods=['get'])
def sql(yl_id):
    ylinfo_sql = "SELECT c_bclj as yllj, c_api_count AS api_docs FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s';" % yl_id
    try:
        ylinfo_res = all_dbc.pg_select_operator(ylinfo_sql)
    except Exception as eee:
        logger.error('CI执行查询用例路径失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail'})
    return jsonify(ylinfo_res)







def com_spl(url):
    ip = cache_tool.res_cache('localip')
    url = 'http://' + str(ip) + str(url)
    a = "curl -H \"Content-Type:application/json\" -X POST -d '{\"url\":\"部署服务启的ip地址\",\"sfjs\": \"是否计算覆盖度，0计算，1不计算\"}' '%s'" % url
    return a



