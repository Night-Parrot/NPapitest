import asyncio
import datetime
import json
import os
import sys, re
from flask_login import login_required

from flask import (Blueprint, Flask, abort, jsonify, request,
                   send_from_directory, send_file, make_response, Response)
from flask_uploads import UploadSet, configure_uploads, patch_request_class

from common import my_log, login_tool
from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()


@asyncio.coroutine
@main.route('/login', methods=['post'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    username = request.json['username']
    password = request.json['password']
    ccc = login_tool.login_tools().user_load(username.strip(), password)
    if ccc != False:
        return jsonify({'result': 'success', 'msg': '登录成功'})
    else:
        return jsonify({'result': 'fail', 'msg': '账户或密码错误，请重新输入，或联系管理员重置'})


@asyncio.coroutine
@main.route('/logout', methods=['get'])
@login_required
def logout():
    msg = login_tool.login_tools().logout()
    return jsonify({'result': 'success', 'msg': msg})




@asyncio.coroutine
@main.route('/updatepwd', methods=['post'])
@login_required
def updatepwd():
    if not request.json or 'new_password' not in request.json:
        abort(400)
    new_password = request.json['new_password']
    if 6 <= len(new_password) <= 18:
        username = login_tool.login_tools().get_username().decode('utf-8')
        res = login_tool.update_password(new_password, username)
        if res:
            return jsonify({'result': 'success', 'msg': '密码修改成功！'})
        else:
            return jsonify({'result': 'fail', 'msg': '密码修改失败，请联系管理员！'})
    else:
        return jsonify({'result': 'fail', 'msg': '密码需在6~18位之间'})