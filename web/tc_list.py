import os
import sys
import asyncio
from flask import Blueprint, Flask, abort, jsonify, request
import math
from flask_login import login_required

from common import my_log, base_tool, cache_tool, login_tool


from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()
from main import all_dbc


@asyncio.coroutine
@main.route('/add_tc', methods=['post'])
@login_required
def add_tc():
    if not request.json or 'tc_text' not in request.json:
        abort(400)
    username = login_tool.login_tools().get_username().decode('utf-8')
    if username == 'guest':
        return jsonify({'result': 'guest', 'msg': '游客就别吐槽了呗！_(ÒωÓ๑ゝ∠)_'})
    tc_text = request.json['tc_text']
    tc_id = base_tool.next_id()
    name = cache_tool.res_cache(username)[1]
    add_tc_sql = "INSERT INTO db_apitesting.c_at_tc (c_id, c_name, c_text, dt_tjsj, c_fkxx, c_fkzt, dt_fksj) VALUES ('%s', '%s', '%s', now(), NULL, '0', NULL);" % (tc_id, name, tc_text)
    try:
        all_dbc.pg_insert_operator(add_tc_sql)
    except Exception as eee:
        logger.error('提交吐槽信息失败：' + str(eee))
        logger.exception(eee)
        return jsonify({'result': 'fail', 'msg': '吐槽失败！(,,#ﾟДﾟ) 请联系管理员'})
    return jsonify({'result': 'success', 'msg': '提交成功'})