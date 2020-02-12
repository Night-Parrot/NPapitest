import asyncio
import datetime
import json
import math
import os
import sys


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import (Blueprint, Flask, abort, jsonify, request,
                   send_from_directory)
from flask_uploads import UploadSet, configure_uploads, patch_request_class

from common import (base_tool, db_clints_for_web,
                    httpreq, my_log, panda_for_web, run_caselist_new)
from multiprocessing import Process
from main import app

from . import main

o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
logger = my_log.LogUtil().getLogger()
from main import all_dbc



@asyncio.coroutine
@main.route('/runcase', methods=['post'])
def run_case():
    if not request.json or 'ylbh' not in request.json or 'list' not in request.json:
        abort(400)
    # 根据ylbh查询出用例对应的用例文件
    ylbh = request.json['ylbh']
    cs_res = request.json['list']
    # 删除之前的参数
    cs_del_sql = "DELETE FROM db_apitesting.t_at_zxcs WHERE c_bh_yl = '%s'" % ylbh
    try:
        all_dbc.pg_delete_operator(cs_del_sql)
    except Exception as eee:
        logger.error('删除参数信息报错:' + str(eee))
        return jsonify({'result': 'fail', 'msg':' 删除参数失败'})
    intnum = 1
    new_kv = {}
    for num in range(len(cs_res)):
        sql_addcs = "INSERT INTO db_apitesting.t_at_zxcs(c_bh, c_bh_yl, c_key, c_value, n_xh) VALUES "\
                    "('%s', '%s', '%s', '%s', '%s')" % (base_tool.next_id(), ylbh, cs_res[num]['zxcs_key'], cs_res[num]['zxcs_value'], intnum)
        try:
            all_dbc.pg_insert_operator(sql_addcs)
            new_kv[cs_res[num]['zxcs_key']] = cs_res[num]['zxcs_value']
        except Exception as eee:
            logger.error('插入参数报错：' + str(eee))
            return jsonify({'result': 'fail', 'msg': '参数插入失败'})
        intnum = intnum + 1
    lj_sql = "SELECT c_bclj as yllj FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s';" % ylbh
    try:
        yl_path = all_dbc.pg_select_operator(lj_sql)
        if len(yl_path) == 0:
            return jsonify({'result': 'fail', 'msg': '用例文件不存在，请重新上传'})
    except Exception as eee:
        logger.error('查询用例路径失败：' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
    # 读取文件，返回格式[参数dict, [总条数, 用例信息], 数据库数组]
    try:
        case_info_all = panda_for_web.read_case(yl_path[0]['yllj'])
        # logger.info(case_info_all)
    except Exception as eee:
        logger.error('用例读取失败：' + str(eee))
        return jsonify({'result': 'fail', 'msg': '用例文件不存在或用例内容不正确，请重新上传'})
    if case_info_all == False:
        return jsonify({'result': 'fail', 'msg': '用例文件不存在或用例内容不正确，请重新上传'})
    # 将参数放入用例信息的首位
    case_info_all.insert(0, new_kv)
    # logger.info(case_info_all)
    # 初始化用例中使用的数据库连接
    try:
        db_case = db_clints_for_web.db_clints(case_info_all[2])
        
    except Exception as eee:
        return jsonify({'result': 'fail', 'msg': str(eee)})
    if db_case == False:
        return jsonify({'result': 'fail', 'msg': '数据库连接创建失败，请检查用例中的数据库配置'})
    logger.info("开始关闭数据链接")
    db_clints_for_web.db_tools().db_close()
    logger.info("完成关闭数据链接")
     # 更新执行次数
    zx_num = "UPDATE db_apitesting.t_at_ylxx SET n_zxcs = n_zxcs + 1 WHERE c_bh = '%s';" % ylbh
    try:
        all_dbc.pg_update_operator(zx_num)
    except Exception as eee:
        logger.error('更新执行次数失败' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
     # 插入用例执行记录
    zxid = base_tool.next_id()
    # 开始执行用例
    logger.info('···开始调用线程池···')
    run_caselist_new.run_caselist(zxid, ylbh, case_info_all)
    logger.info('···调用线程池完毕···')
    '''
    # 创建子进程
    ~~~~~此处由于进程创建时完整复制当前进程的内容，包括数据库连接，因此会导致在主进程（不知原因，可能是因为程序报错）关闭时，导致子进程的数据库连接发生异常~~~~~
    ~~~~~由此修改为调用线程池中的预留线程，通过vthread提供的线程池装饰器来实现，在主进程中直接调用对应的被装饰函数即可~~~~~
    p = Process(target=run_caselist_new.run_caselist, args=(zxid, ylbh, case_info_all, ))
    logger.info('创建子进程，主进程id：' + str(os.getpid()))
    try:
        p.start()
    except Exception as eaa:
        logger.error('子进程启动失败：' + str(eaa))
        return jsonify({'result': 'fail', 'msg': str(eaa)})
    logger.info('子进程状态' + str(p.is_alive()))
    '''
    '''
    runcase_data = {'zxid': str(zxid),'ylbh': str(ylbh),'case_info_all': str(case_info_all)}
    runcase_data = json.dumps(runcase_data, ensure_ascii=False)
    logger.info(str(runcase_data))
    headers = {'Content-Type': 'application/json'}
    try:
        # requests.post('http//:localhost:9999/apitest/runcase_for_real', data=runcase_data)
        requests.post('http://172.18.49.18:8585/runcase_for_real', data=runcase_data.encode('utf-8'), headers=headers, allow_redirects=False)
    except Exception as eee:
        logger.error('调用执行用例接口失败：' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
    logger.info('用例执行接口调用成功')
    '''
    zxjl_sql = "INSERT INTO db_apitesting.t_at_zxxx(c_bh, c_bh_yl, dt_zxsj, c_fgl, c_cgl, c_tgl, n_zt, c_cg, c_wcg, c_tg, c_wtg) VALUES"\
                " ('%s', '%s', now(), 0, 0, 0, 0, 0, 0, 0, 0);" % (zxid, ylbh)
    try:
        all_dbc.pg_insert_operator(zxjl_sql)
    except Exception as eee:
        logger.error('插入执行信息失败' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
    return jsonify({'result': 'success', 'msg': '成功', 'zxid': zxid})




@asyncio.coroutine
@main.route('/zxcs', methods=['get'])
def zxcs():
    if not request.args or 'ylbh' not in request.args:
        abort(400)
    ylbh = request.args.get('ylbh')
    # 根据ylbh查询出对应的执行参数
    zxcs_sql_count = "SELECT count(1), c_bh_yl as ylbh FROM db_apitesting.t_at_zxcs WHERE c_bh_yl = '%s' GROUP BY c_bh_yl" % ylbh
    zxcs_sql = "SELECT c_bh as key, c_key as zxcs_key, c_value as zxcs_value FROM db_apitesting.t_at_zxcs WHERE c_bh_yl = '%s' ORDER BY n_xh ASC" % ylbh
    try:
        counts = all_dbc.pg_select_operator(zxcs_sql_count)
        list = all_dbc.pg_select_operator(zxcs_sql)
    except Exception as eee:
        logger.error('查询参数的sql报错了：' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
    res_info = {}
    if len(counts) != 1:
        res_info['ylbh'] = ylbh
        res_info['maxsize'] = 0
        res_info['reslist'] = []
        return jsonify(res_info)
    else:
        res_info['ylbh'] = counts[0]['ylbh']
        res_info['maxsize'] = counts[0]['count']
        res_info['reslist'] = list
        return jsonify(res_info)