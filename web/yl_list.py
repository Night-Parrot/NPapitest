import os
import sys
import asyncio
from flask import Blueprint, Flask, abort, jsonify, request
import math
from flask_login import login_required

from common import my_log


from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()
from main import all_dbc


@asyncio.coroutine
@main.route('/<xmurl>/yl_list/<pagenum>', methods=['get'])
@login_required
def yl_list(xmurl, pagenum): #列表查询，返回总页数、总条数、每页数据
    sql_list = "select yl.c_bh as ylbh,yl.c_ylmc as ylmc,to_char(yl.dt_scsj, 'yyyy-mm-dd hh24:mi:ss') as scsj,yl.n_zxcs as zxcs,yl.c_sfbj as bjzt "\
    "from db_apitesting.t_at_xmxx xm left join db_apitesting.t_at_ylxx yl on xm.c_bh = yl.c_bh_xm "\
    "where xm.c_url = '%s' ORDER by yl.dt_scsj desc LIMIT %s OFFSET %s;" % (xmurl, 8, (int(pagenum) - 1)*8)
    sql_count = "select count(1) as counts "\
    "from db_apitesting.t_at_xmxx xm left join db_apitesting.t_at_ylxx yl on xm.c_bh = yl.c_bh_xm "\
    "where xm.c_url = '%s';" % xmurl
    try:
        project_dict = {}
        res_count = all_dbc.pg_select_operator(sql_count)
        # 判断一下最大页数，如果当前请求页数超出数据的最大页数，直接返回最大页的数据
        if math.ceil(res_count[0]['counts']/8) < int(pagenum):
            sql_list = "select yl.c_bh as ylbh,yl.c_ylmc as ylmc,to_char(yl.dt_scsj, 'yyyy-mm-dd hh24:mi:ss') as scsj,yl.n_zxcs as zxcs,yl.c_sfbj as bjzt "\
                    "from db_apitesting.t_at_xmxx xm left join db_apitesting.t_at_ylxx yl on xm.c_bh = yl.c_bh_xm "\
                    "where xm.c_url = '%s' ORDER by yl.dt_scsj desc LIMIT %s OFFSET %s;" % (xmurl, 8, (int(math.ceil(res_count[0]['counts']/8)) - 1)*8)
            pagenum = math.ceil(res_count[0]['counts']/8)
        res_list = all_dbc.pg_select_operator(sql_list)
        project_dict['maxpage'] = math.ceil(res_count[0]['counts']/8)
        project_dict['maxsize'] = res_count[0]['counts']
        project_dict['nowpage'] = int(pagenum)
        xh = 0
        for arr in res_list:
            arr['xh'] = xh
            arr['update'] = 0
            xh = xh + 1
        project_dict['reslist'] = res_list
        return jsonify(project_dict)
    except Exception as eee:
        logger.error(eee)
        return jsonify({'result': 'fail'})




@asyncio.coroutine
@main.route('/del_yl/<ylbh>', methods=['delete'])
@login_required
def yl_del(ylbh): #用例记录删除，todo缺少文件实体的删除
    sql_path = "SELECT c_bclj as yllj FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s'" % ylbh #查询路径，要先查
    sql_del_yl = "DELETE FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s'" % ylbh #删除ylxx主表的数据
    # sql_del_zx = "DELETE FROM db_apitesting.t_at_zxxx WHERE c_bh_yl = '%s'" % ylbh #删除zxxx子表的数据
    # sql_del_qq = "DELETE FROM db_apitesting.t_at_qqxx WHERE c_bh_yl = '%s'" % ylbh #删除qqxx子表的数据
    sql_del_cs = "DELETE FROM db_apitesting.t_at_zxcs WHERE c_bh_yl = '%s'" % ylbh #删除zxcs子表的数据
    try:
        yl_path = all_dbc.pg_select_operator(sql_path)
    except Exception as eee:
        logger.error('查询路径报的错：' + str(eee))
        return jsonify({'result': 'fail', 'msg': '用例删除失败'})
    if(os.path.exists(yl_path[0]['yllj'])):
        try:
            os.remove(yl_path[0]['yllj'])
        except Exception as eee:
            logger.error('删除原用例文件失败:' + str(eee))
            return jsonify({'result': 'fail', 'msg': str(eee)})
    try:
        # for sql in [sql_del_yl, sql_del_qq, sql_del_zx, sql_del_cs]:
        for sql in [sql_del_yl, sql_del_cs]:
            all_dbc.pg_delete_operator(sql)
        return jsonify({'result': 'success'})
    except Exception as eee:
        logger.error(eee)
        return jsonify({'result': 'fail'})