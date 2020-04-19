import os
import sys
import asyncio
from flask import Blueprint, Flask, abort, jsonify, request
from flask_login import login_required
import math

from common import my_log


from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()
from main import all_dbc


@asyncio.coroutine
@main.route('/tjxx', methods=['get'])
@login_required
def tjxx():
    if not request.args or 'zxid' not in request.args:
        abort(400)
    # 根据ylbh查询出用例对应的用例文件
    zxid = request.args.get('zxid')
    sql_tjxx = "select  c_cg as cg, c_wcg as wcg, c_tg as tg, c_wtg as wtg from db_apitesting.t_at_zxxx where c_bh = '%s';" % zxid
    try:
        sql_tjxx_res = all_dbc.pg_select_operator(sql_tjxx)
    except Exception as eee:
        logger.error('查询通过率和成功率的sql错误:' + str(eee))
        return jsonify({'result': 'fail', 'msg': '查询失败'})
    res_info = [[{'item': '调用成功', 'count': 0, 'percent': 0}, {'item': '调用失败', 'count': 0, 'percent': 0}], 
                [{'item': '验证通过', 'count': 0, 'percent': 0}, {'item': '验证失败', 'count': 0, 'percent': 0}]]
    # 返回结果为空，即表示查询出现了问题，目前是为了解决查询时，数据实际还没生成的问题
    if len(sql_tjxx_res) == 0:
        return jsonify(res_info)
    try:
        res_info[0][0]['count'] = int(sql_tjxx_res[0]['cg'])
    except Exception as eee:
        logger.error('统计信息查询结果：' + str(sql_tjxx_res))
        res_info[0][0]['count'] = 0
    try:
        res_info[0][0]['percent'] = round(int(sql_tjxx_res[0]['cg'])/(int(sql_tjxx_res[0]['cg']) + int(sql_tjxx_res[0]['wcg'])), 4)
    except:
        res_info[0][0]['percent'] = 0
    res_info[0][1]['count'] = int(sql_tjxx_res[0]['wcg'])
    try:
        res_info[0][1]['percent'] = round((1 - int(sql_tjxx_res[0]['cg'])/(int(sql_tjxx_res[0]['cg']) + int(sql_tjxx_res[0]['wcg']))), 4)
    except:
        res_info[0][1]['percent']
    res_info[1][0]['count'] = int(sql_tjxx_res[0]['tg'])
    try:
        res_info[1][0]['percent'] = round(int(sql_tjxx_res[0]['tg'])/(int(sql_tjxx_res[0]['tg']) + int(sql_tjxx_res[0]['wtg'])), 4)
    except:
        res_info[1][0]['percent'] = 0
    res_info[1][1]['count'] = int(sql_tjxx_res[0]['wtg'])
    try:
        res_info[1][1]['percent'] = round((1 - int(sql_tjxx_res[0]['tg'])/(int(sql_tjxx_res[0]['tg']) + int(sql_tjxx_res[0]['wtg']))), 4)
    except:
        res_info[1][1]['percent'] = 0
    return jsonify(res_info)
    



# date: "接口111",
# actual: 175,
# expected: 400

@asyncio.coroutine
@main.route('/sjfb', methods=['get'])
@login_required
def sjfb():
    if not request.args or 'zxid' not in request.args:
        abort(400)
    zxid = request.args.get('zxid')
    sql_sjfb = "select n_qqmc as date, c_xysj as actual, 3000 as expected from db_apitesting.t_at_qqxx where c_bh_zx = '%s' order by n_xh asc;" % zxid
    try:
        sql_sjfb_res = all_dbc.pg_select_operator(sql_sjfb)
    except Exception as eee:
        logger.error('查询分布时间的sql错误:' + str(eee))
        return jsonify({'result': 'fail', 'msg': '查询失败'})
    for num in range(len(sql_sjfb_res)):
        if str(sql_sjfb_res[num]['actual']) == '0':
            sql_sjfb_res[num]['actual'] = 0
        else:
            sql_sjfb_res[num]['actual'] = int(float((sql_sjfb_res[num]['actual'])[:-1])*1000)
    return jsonify(sql_sjfb_res)