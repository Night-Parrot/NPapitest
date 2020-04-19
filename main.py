import os
import sys
import asyncio
import datetime
from flask import Blueprint, Flask, jsonify
from flask_login import LoginManager 
from db_mod import db_connect


app = Flask(__name__)

login_manager = LoginManager()
from flask_cors import CORS

all_dbc = db_connect.My_dbc()

from flask_caching import Cache
# 简单缓存
cache_local = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 60*60*24000000})


o_path = os.getcwd()
sys.path.append(o_path)
from web import main
from web import JSONEncoder




from common import login_tool, my_log, cache_tool
logger = my_log.LogUtil().getLogger()




@login_manager.user_loader
def load_user(user_id):
    curr_user = login_tool.User()
    curr_user.id = user_id
    return curr_user



app.secret_key = 'EVANGELION'
login_manager.login_message = '请登录'
login_manager.session_protection = 'strong'
login_manager.init_app(app)





CORS(app, supports_credentials=True)
app.register_blueprint(main)
app.register_blueprint(main, url_prefix='/apitest')  # 生产配置
app.json_encoder = JSONEncoder.MyJSONEncoder
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload')
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    hours=1)  # 登录超时的时间设置


app.config['ALLOWED_EXTENSIONS'] = ['.xlsx']
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*60




if __name__ == '__main__':
    app.run(host="172.18.48.41", port=8585, debug=False,  use_reloader=False)
    # app.run()

