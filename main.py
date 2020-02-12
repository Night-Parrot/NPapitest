import os
import sys
import asyncio
from flask import Blueprint, Flask


app = Flask(__name__)
from flask_cors import CORS

from db_mod import db_connect
all_dbc = db_connect.My_dbc()
from web import main
from web import JSONEncoder
from common import my_log
o_path = os.getcwd()
sys.path.append(o_path)

logger = my_log.LogUtil().getLogger()




CORS(app, supports_credentials=True)
# app.register_blueprint(main, url_prefix='/apitest')
app.register_blueprint(main)
app.json_encoder = JSONEncoder.MyJSONEncoder
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload')


app.config['ALLOWED_EXTENSIONS'] = ['.xlsx']
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*60



if __name__ == '__main__':
    app.run(host="172.18.49.18", port=8585, debug=True)
    # app.run()

