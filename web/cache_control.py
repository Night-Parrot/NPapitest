import asyncio
import datetime
import json
import os
import sys, re
from flask_login import login_required

from flask import (Blueprint, Flask, abort, jsonify, request)

from common import my_log, login_tool, cache_tool, login_tool
from . import main

o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()


@asyncio.coroutine
@main.route('/reload_cache', methods=['get'])
@login_required
def reload_cache():
    username = login_tool.login_tools().get_username().decode('utf-8')
    if username != 'lianglei':
        abort(403)
    else:
        try:
            cache_tool.add_cache()
            return jsonify({'result': 'success', 'msg': '缓存刷新成功'})
        except Exception as eee:
            logger.error('缓存刷新失败：' + str(eee))
            logger.exception(eee)
            return jsonify({'result': 'fail', 'msg': '缓存刷新失败'})