import os
import sys
import asyncio
import chardet
import requests
from flask import Blueprint, Flask, abort, jsonify, request, send_from_directory, make_response, render_template
from . import main
from main import all_dbc
from common import my_log, cache_tool, login_tool, base_tool, panda_for_web
from flask_login import login_required

o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
logger = my_log.LogUtil().getLogger()



@asyncio.coroutine
@main.route('/edit_page/<ylbh>/<ylmc>', methods=['get'])
@login_required
def edit_page(ylbh, ylmc):
    info = {}
    info['ylbh'] = ylbh
    ip = cache_tool.res_cache('localip')
    wjlj = 'http://' + str(ip) + ':8585/downloadfile/' + str(ylbh)
    # wjlj = 'http://' + str(ip) + '/apitest/downloadfile/' + str(ylbh)  #生产参数
    edit_key_sql = "SELECT c_edit_key as key FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s'" % (ylbh)
    editing_tag = "UPDATE db_apitesting.t_at_ylxx SET c_sfbj = 1 WHERE c_bh = '%s'" % (ylbh)
    try:
        edit_key = all_dbc.pg_select_operator(edit_key_sql)
        all_dbc.pg_update_operator(editing_tag)
    except Exception as eee:
        logger.error('查询edit_key报错：' + str(eee))
    logger.warn(wjlj) 
    info['lj'] = wjlj
    info['key'] = edit_key[0]['key']
    username = login_tool.login_tools().get_username().decode('utf-8')
    info['name'] = username
    return render_template('edit.html', title = ylmc, info = info)



@asyncio.coroutine
@main.route('/view_page/<ylbh>/<ylmc>', methods=['get'])
@login_required
def view_page(ylbh, ylmc):
    info = {}
    info['ylbh'] = ylbh
    ip = cache_tool.res_cache('localip')
    wjlj = 'http://' + str(ip) + ':8585/downloadfile/' + str(ylbh)
    # wjlj = 'http://' + str(ip) + '/apitest/downloadfile/' + str(ylbh) #生产参数
    edit_key_sql = "SELECT c_edit_key as key FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s'" % (ylbh)
    try:
        edit_key = all_dbc.pg_select_operator(edit_key_sql)
    except Exception as eee:
        logger.error('查询edit_key报错：' + str(eee))
    logger.warn(wjlj) 
    info['lj'] = wjlj
    info['key'] = edit_key[0]['key']
    username = login_tool.login_tools().get_username().decode('utf-8')
    info['name'] = username
    return render_template('view.html', title = ylmc, info = info)





@asyncio.coroutine
@main.route('/office_update',methods=['post'])
def office_update():
    # logger.info(request.json)
    if request.json['status'] == 2:
        logger.info('编辑结束，开始保存用例···')
        file_id = request.json['key']
        file = requests.get(request.json['url'], stream=False)
        sql_yl_bh = "SELECT c_bh as ylbh, c_bclj as yllj FROM db_apitesting.t_at_ylxx WHERE c_edit_key = '%s'" % (file_id)
        try:
            yl_old = all_dbc.pg_select_operator(sql_yl_bh)
            yllj_old = yl_old[0]['yllj']
            yl_bh = yl_old[0]['ylbh']
        except Exception as eee:
            logger.error('更新用例时,查询失败:' + str(eee))
            return jsonify({'result': 'fail'})
        # 开始保存新的用例文件
        # 获取原来的保存路径
        p_old, f = os.path.split(yllj_old)
        # 删除之前的用例文件
        if(os.path.exists(yllj_old)):
            try:
                os.remove(yllj_old)
            except Exception as eee:
                logger.error('删除原用例失败:' + str(eee))
        file_uuid = base_tool.next_id()
        newpath = p_old
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        newpath_all = os.path.join(newpath, str(file_uuid + '.xlsx'))
        try:
            with open(newpath_all, "wb") as f:
                f.write(file.content)
        except Exception as eee:
            logger.error('文件保存失败: ' + str(eee))
        # 开始解析参数，如果解析失败，不进行用例保存
        cs_res = panda_for_web.read_keylist(newpath_all)
        # 删除之前的参数 
        cs_del_sql = "DELETE FROM db_apitesting.t_at_zxcs WHERE c_bh_yl = '%s'" % yl_bh
        try:
            all_dbc.pg_delete_operator(cs_del_sql)
        except Exception as eee:
            logger.error('删除参数出错:' + str(eee))
        intnum = 1
        '''
        待优化，将sql放到外层组装，最终一起执行
        '''
        for num in cs_res:
            sql_addcs = "INSERT INTO db_apitesting.t_at_zxcs(c_bh, c_bh_yl, c_key, c_value, n_xh) VALUES "\
            "('%s', '%s', '%s', '%s', '%s')" % (base_tool.next_id(), yl_bh, num, cs_res[num], intnum)
            # logger.info(sql_addcs)
            try:
                all_dbc.pg_insert_operator(sql_addcs)
            except Exception as eee:
                logger.error('插入参数报错：' + str(eee))
            intnum = intnum + 1
        try:
            sql_addyl = "UPDATE db_apitesting.t_at_ylxx SET dt_gxsj = now(), c_bclj = '%s', c_sfbj = 2, c_edit_key = '%s' WHERE c_bh = '%s'" % (newpath_all, str(base_tool.next_id())[:20], yl_old[0]['ylbh'])
            # logger.info(str(sql_addyl))
            all_dbc.pg_update_operator(sql_addyl)
        except Exception as eee:
            logger.error('插入用例信息错误：' + str(eee))
        logger.info('保存结束')
        return jsonify({"error": 0})
    elif request.json['status'] == 4:
        file_id = request.json['key']
        try:
            sql_upyl = "UPDATE db_apitesting.t_at_ylxx SET c_sfbj = 2 WHERE c_edit_key = '%s'" % (file_id)
            all_dbc.pg_update_operator(sql_upyl)
            return jsonify({"error": 0})
        except Exception as eee:
            logger.error('插入用例信息错误：' + str(eee))
            return jsonify({'result': 'fail'})
    else:
        return jsonify({"error": 0})