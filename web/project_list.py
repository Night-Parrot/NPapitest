import os
import sys
import asyncio
import math
from flask import Blueprint, Flask, abort, jsonify, request

from common import my_log

from . import main


o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
logger = my_log.LogUtil().getLogger()
logger.info(str(o_path))
from main import all_dbc


@asyncio.coroutine
@main.route('/project_list', methods=['get'])
def project_list():
    sql = "SELECT c_bh as xmbh,c_xmmc as xmmc,c_url as xmdz FROM db_apitesting.t_at_xmxx"
    sql_count = "SELECT count(1) as counts FROM db_apitesting.t_at_xmxx"
    try:
        project_dict = {}
        res_list = all_dbc.pg_select_operator(sql)
        logger.info("res-list" + str(res_list))
        res_count = all_dbc.pg_select_operator(sql_count)
        project_dict['maxsize'] = res_count[0]['counts']
        project_dict['reslist'] = res_list
        return jsonify(project_dict)
    except Exception as eee:
        logger.error('项目列表接口报错：' + str(eee))
        return jsonify({'result': 'fail'})
