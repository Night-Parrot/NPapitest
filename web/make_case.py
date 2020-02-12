import asyncio
import datetime
import json
import math
import os
import re
import sys
import uuid

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import (Blueprint, Flask, abort, jsonify, request,
                   send_from_directory, send_file, make_response, Response)
from flask_uploads import UploadSet, configure_uploads, patch_request_class

from common import base_tool
from common import build_case_in_swagger as sw
from common import httpreq, my_log, panda_for_web
from main import app

from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()


@asyncio.coroutine
@main.route('/makecase', methods=['get'])
def make_case():
    if not request.args or 'url' not in request.args:
        abort(400)
    # 根据ylbh查询出用例对应的用例文件
    url = request.args.get('url')
    try:
        cookie = request.args.get('cookie')
    except Exception as eee:
        pass
    if url == '':
        return jsonify({'result': 'fail', 'msg': 'swagger地址是必填项'})
    try:
        swagger_info = sw.swagger(url, cookie)
    except Exception as eee:
        logger.error("用例生成的错误：" + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
    try:
        key_names = re.findall(r'{{(.*?)}}', str(swagger_info[0]))
        key_names = list(set(key_names))
        keys = []
        for key in swagger_info[1]:
            keys.append(key['key'])
        new_key = list(set(key_names) - set(keys))
        for key in new_key:
            key_value = {}
            key_value['key'] = key
            key_value['value'] = ''
            swagger_info[1].append(key_value)

        id = uuid.uuid4().hex
        filename = str(id + '.xlsx')
        file_path = os.getcwd() + '/case_demo/' + filename
    except Exception as eee:
        logger.error("解析swagger返回数据的错误：" + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            swagger_info_case = pd.DataFrame(swagger_info[0])
            keywords = pd.DataFrame(swagger_info[1])
            swagger_info_case.sort_values(by=['name'], ascending=False)
            keywords.to_excel(writer, sheet_name='keywords', index=False)
            swagger_info_case.to_excel(writer, sheet_name='caselist', index=False)
            dbinfo = {'name': '', 'db_type': '', 'db_ip': '', 'db_port': '',
                    'db_user': '', 'db_password': '', 'db_name': ''}
            dbinfo = pd.DataFrame(dbinfo, index=[0])
            dbinfo.to_excel(writer, sheet_name='db_config', index=False)
            workbook = writer.book
            workbook_case = writer.sheets['caselist']
            workbook_keys = writer.sheets['keywords']
            workbook_db = writer.sheets['db_config']
            workbook_db.set_column('A:G', 15)
            workbook_keys.set_column('A:A', 10)
            workbook_keys.set_column('B:B', 20)
            workbook_case.set_column('B:B', 30)
            workbook_case.set_column('A:A', 6)
            workbook_case.set_column('D:F', 30)
            workbook_case.set_column('I:O', 30)
            workbook_case.set_column('C:C', 8)
            workbook_case.set_column('G:G', 6)
            workbook_case.set_column('H:H', 10)
            workbook_case.set_column('J:J', 6)
            writer.save()
        # file_path = 'D:\\github\\apitesting\\case_demo\\1.xlsx'  #测试用文件
        p, f = os.path.split(file_path)
        logger.error(file_path)
        # return send_from_directory(p, f, as_attachment=True)
        # return send_file(file_path)
        response = make_response(send_from_directory(p, f, as_attachment=True))
        # response.headers["Content-Disposition"] = "attachment; filename={}"
        response.headers["content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        # response.headers["Content-Type"] = "text/plain;charset=utf-8"
        return response
    except Exception as eee:
        logger.error("用例保存方法的错误：" + str(eee))
        return jsonify({'result': 'fail', 'msg': str(eee)})
