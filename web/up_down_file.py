import os
import sys
import asyncio
from urllib.parse import quote
import chardet
from flask import Blueprint, Flask, abort, jsonify, request, send_from_directory, make_response
import math
from flask_uploads import UploadSet
from flask_uploads import configure_uploads, patch_request_class
from flask_login import login_required

from common import my_log, panda_for_web, base_tool


from . import main


o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
logger = my_log.LogUtil().getLogger()
from main import all_dbc
from main import app

# file = UploadSet('file')



@asyncio.coroutine
@main.route('/uploadfile', methods=['post'])
@login_required
def uploadfile(): #上传文件
    if 'file' not in request.files or 'xmdz' not in request.form:
        abort(400)
    xmdz = request.form.get('xmdz')
    file = request.files.get('file')
    sql_xm_bh = "SELECT c_bh, c_code_team AS code, c_test_team AS test FROM db_apitesting.t_at_xmxx WHERE c_url = '%s';" % (xmdz)
    try:
        xm_info = all_dbc.pg_select_operator(sql_xm_bh)
        if len(xm_info) == 0:
            return jsonify({'result': 'fail', 'msg': '项目不存在'})
        else:
            xmbh = xm_info[0]['c_bh']
    except Exception as eee:
        logger.error('根据项目地址查询项目编号失败' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
    all_name = os.path.splitext(file.filename)
    file_name = all_name[-2]
    Suffix = all_name[-1]
    if Suffix in app.config['ALLOWED_EXTENSIONS']:
        file_uuid = base_tool.next_id()
        newpath = os.path.join(app.config['UPLOAD_FOLDER'], xmdz)
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        newpath_all = os.path.join(newpath, str(file_uuid + '.xlsx'))
        try:
            file.save(newpath_all)
        except Exception as eee:
            logger.error('文件保存失败: ' + str(eee))
            return jsonify({'result': 'fail', 'msg': str(eee)})
        # 开始解析参数，如果解析失败，不进行用例保存
        try:
            cs_res = panda_for_web.read_keylist(newpath_all)
        except Exception as eee:
            return jsonify({'result': 'fail', 'msg': '解析参数失败，请检查参数sheet页'})
        ylbh = base_tool.next_id()
        sql_addyl = "INSERT INTO db_apitesting.t_at_ylxx(c_bh, c_bh_xm, c_ylmc, dt_scsj, dt_zxzxsj, n_zxcs, c_bclj, c_edit_key, c_sfbj, dt_gxsj, c_code_team, c_test_team) "\
                    "VALUES ('%s', '%s', '%s', now(), NULL, 0, '%s', '%s', 2, now(), '%s', '%s');" % (ylbh, xmbh, file_name, newpath_all, ylbh, xm_info[0]['code'], xm_info[0]['test'])
        try:
            all_dbc.pg_insert_operator(sql_addyl)
        except Exception as eee:
            logger.error('插入用例信息错误：' + str(eee))
            return jsonify({'result': 'fail'})
        intnum = 1
        for num in cs_res:
            sql_addcs = "INSERT INTO db_apitesting.t_at_zxcs(c_bh, c_bh_yl, c_key, c_value, n_xh) VALUES "\
            "('%s', '%s', '%s', '%s', '%s')" % (base_tool.next_id(), ylbh, num, cs_res[num], intnum)
            try:
                all_dbc.pg_insert_operator(sql_addcs)
            except Exception as eee:
                logger.error('插入参数报错：' + str(eee))
                return jsonify({'result': 'fail', 'msg': '参数插入失败'})
            intnum = intnum + 1
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'msg': '文件类型错误，仅支持.xlsx格式'})



@asyncio.coroutine
@main.route('/updatefile', methods=['post'])
@login_required
def updatefile(): #上传文件
    if 'file' not in request.files or 'ylbh' not in request.form:
        abort(400)
    ylbh = request.form.get('ylbh')
    file = request.files.get('file')
    sql_yl_bh = "SELECT c_bclj as yllj FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s'" % (ylbh)
    try:
        yl_old = all_dbc.pg_select_operator(sql_yl_bh)
        if len(yl_old) == 0:
            return jsonify({'result': 'fail', 'msg': '用例信息已不存在,请刷新页面'})
        else:
            yllj_old = yl_old[0]['yllj']
    except Exception as eee:
        logger.error('更新用例时,查询失败:' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
    # 开始保存新的用例文件
    # 获取原来的保存路径
    p_old, f = os.path.split(yllj_old)
    all_name = os.path.splitext(file.filename)
    # file_name = all_name[-2]
    Suffix = all_name[-1]
    if Suffix in app.config['ALLOWED_EXTENSIONS']:
        # 删除之前的用例文件
        if(os.path.exists(yllj_old)):
            try:
                os.remove(yllj_old)
            except Exception as eee:
                logger.error('删除原用例失败:' + str(eee))
                return jsonify({'result': 'fail', 'msg': str(eee)})
        file_uuid = base_tool.next_id()
        newpath = p_old
        if not os.path.isdir(newpath):
            os.makedirs(newpath)
        newpath_all = os.path.join(newpath, str(file_uuid + '.xlsx'))
        try:
            file.save(newpath_all)
        except Exception as eee:
            logger.error('文件保存失败: ' + str(eee))
            return jsonify({'result': 'fail', 'msg': str(eee)})
        # 开始解析参数，如果解析失败，不进行用例保存
        try:
            cs_res = panda_for_web.read_keylist(newpath_all)
        except Exception as eee:
            return jsonify({'result': 'fail', 'msg': '解析参数失败，请检查参数sheet页'})
        # 删除之前的参数 
        cs_del_sql = "DELETE FROM db_apitesting.t_at_zxcs WHERE c_bh_yl = '%s'" % ylbh
        try:
            all_dbc.pg_delete_operator(cs_del_sql)
        except Exception as eee:
            logger.error('删除参数出错:' + str(eee))
            return jsonify({'result': 'fail', 'msg': '删除参数报错'})
        intnum = 1
        for num in cs_res:
            sql_addcs = "INSERT INTO db_apitesting.t_at_zxcs(c_bh, c_bh_yl, c_key, c_value, n_xh) VALUES "\
            "('%s', '%s', '%s', '%s', '%s')" % (base_tool.next_id(), ylbh, num, cs_res[num], intnum)
            try:
                all_dbc.pg_insert_operator(sql_addcs)
            except Exception as eee:
                logger.error('插入参数报错：' + str(eee))
                return jsonify({'result': 'fail', 'msg': '参数插入失败'})
            intnum = intnum + 1
        try:
            new_edit_key = base_tool.next_id()
            sql_addyl = "UPDATE db_apitesting.t_at_ylxx SET c_bclj = '%s', c_edit_key = '%s', dt_gxsj = now() WHERE c_bh = '%s'" % (newpath_all, new_edit_key, ylbh, )
            all_dbc.pg_insert_operator(sql_addyl)
        except Exception as eee:
            logger.error('插入用例信息错误：' + str(eee))
            return jsonify({'result': 'fail'})
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'msg': '文件类型错误，仅支持.xlsx格式'})






@asyncio.coroutine
@main.route('/downloadfile/<ylbh>', methods=['get'])
def downloadfile(ylbh): #下载文件
    sql_filepath = "SELECT c_bclj as lj,c_ylmc as mc FROM db_apitesting.t_at_ylxx WHERE c_bh = '%s';" % ylbh
    logger.info(sql_filepath)
    try:
        filepath = all_dbc.pg_select_operator(sql_filepath)
        new_filepath = filepath[0]['lj']
        p, f = os.path.split(new_filepath)
        if os.path.isfile(new_filepath):
            response = make_response(send_from_directory(p, f, as_attachment=True))
            logger.info('编码格式:' + str(chardet.detect(str.encode(filepath[0]['mc']))))
            logger.info('文件名称:' + str(filepath[0]['mc'].encode('utf-8').decode('latin-1')))
            response.headers["content-disposition"] = "attachment; filename={}".format(str('测试文件名称.xlsx').encode().decode('latin-1'))
            response.headers["content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            response.headers["Access-Control-Expose-Headers"] = "Content-disposition" # 解决前端无法访问到返回头中的文件名称的问题
            # response.headers["Content-Disposition"] = "{}".format(filepath[0]['mc'].encode().decode('latin-1'))
            return response
        else:
            return jsonify({'result': 'fail', 'msg': '文件不存在'})
    except Exception as eee:
        logger.error('文件下载报错：' + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})





@asyncio.coroutine
@main.route('/downloadyhsc', methods=['get'])
def downloadyhsc(): #下载用户手册
    try:
        logger.info(os.getcwd())
        filepath = os.getcwd() + '/upload/使用说明.docx'
        logger.error(filepath)
        p, f = os.path.split(filepath)
        if os.path.isfile(filepath):
            response = make_response(send_from_directory(p, f, as_attachment=True))
            return response
        else:
            return jsonify({'result': 'fail', 'msg': '文件不存在'})
    except Exception as eee:
        logger.error(eee)
        return jsonify({'result': 'fail', 'msg': str(eee)})



@asyncio.coroutine
@main.route('/downloadkbyl', methods=['get'])
def downloadkbyl(): #下载空白用例
    try:
        logger.info(os.getcwd())
        filepath = os.getcwd() + '/upload/用例模板.xlsx'
        logger.error(filepath)
        p, f = os.path.split(filepath)
        if os.path.isfile(filepath):
            response = make_response(send_from_directory(p, f, as_attachment=True))
            return response
        else:
            return jsonify({'result': 'fail', 'msg': '文件不存在'})
    except Exception as eee:
        logger.error(eee)
        return jsonify({'result': 'fail', 'msg': str(eee)})