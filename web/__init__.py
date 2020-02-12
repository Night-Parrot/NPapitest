import sys
import os
# 顺序很重要，main要在具体函数引用之前
from flask import Blueprint


main = Blueprint('main', __name__)

o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')

from . import project_list, yl_list, zx_list, up_down_file, run_case, ylzx_info, make_case, zx_info, tool_box