from jsondiff import diff
import json
import os
import sys
import time


o_path = os.getcwd()
sys.path.append(o_path)
from common import my_log
logger = my_log.LogUtil().getLogger()


class diff_json_match(object):
    # 初始化参数
    def __init__(self, diff_json, sqlless, reqless, matchinfo):
        self.diff_json = diff_json
        self.sqlless = sqlless
        self.reqless = reqless
        self.matchinfo = matchinfo

    def find_diff(self):
        # 开始循环&递归解析结果集
        # $insert 代表查询缺失， 比较时自动忽略， 不作为验证标准
        # $update 代表相同key的value不一致， 作为验证的重要标准
        # $delete 代表缺失内容， 作为验证的重要标准
        # 无标示的代表不一致， list结果集时， 返回索引值和内容， dict结果集时， 但会key值和内容
        if isinstance(self.diff_json, list):
            return False
        for diff_name in self.diff_json:
            if str(diff_name) == '$delete':
                self.reqless.append(self.diff_json[diff_name])
            # jsondiff的'symmetric'比较方式，不返回update集合，故忽略
            # elif str(diff_name) == '$update':
            #     self.reqless.append(self.diff_json[diff_name])
            elif str(diff_name) == '$insert':
                self.sqlless.append(self.diff_json[diff_name])
            else:
                if 'delete' in str(self.diff_json[diff_name]) or 'insert' in str(self.diff_json[diff_name]) or 'update' in str(self.diff_json[diff_name]):
                    diff_json_match(self.diff_json[diff_name], self.sqlless, self.reqless, self.matchinfo).find_diff()
                else:
                    self.matchinfo.append({diff_name: self.diff_json[diff_name]})
        return {'查询缺少': self.sqlless, '返回值缺少': self.reqless, '匹配结果': self.matchinfo}



if __name__ == '__main__':
    a = {}
    b = {'code': 500, 'data': None, 'message': '服务器内部处理错误', 'success': False}
    matchinfo = diff(a, b, syntax='symmetric')
    print(matchinfo)
    # matchinfo = [{}, {'code': 500, 'data': None, 'message': '服务器内部处理错误', 'success': False}]

    mmm = diff_json_match(matchinfo, [], [], []).find_diff()
    print(mmm)
