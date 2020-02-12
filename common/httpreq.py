import requests
import json

from common import re_fun_for_web, my_log, base_tool

logger = my_log.LogUtil().getLogger()

class httpclints(object):

    def __init__(self, reqinfo, keyv):
        self.reqinfo = reqinfo
        self.keyv = keyv

    def re_all(self):
        dictinfo = self.reqinfo
        # dictinfo['url'] = re_fun_for_web.re_fun_url(dictinfo['url'], self.keyv)
        dictinfo['url'] = base_tool.replace_for_web(dictinfo['url'], self.keyv)
        if dictinfo['headers'] != '':
            # dictinfo['headers'] = re_fun_for_web.re_fun_parameter(dictinfo['headers'], self.keyv)
            headers = base_tool.replace_for_web(dictinfo['headers'], self.keyv)
            try:
                headers = json.loads(headers.replace('\'', '\"'))
            except:
                headers = headers
            dictinfo['headers'] = headers
        if dictinfo['cs'] != '':
            # dictinfo['cs'] = re_fun_for_web.re_fun_parameter(dictinfo['cs'], self.keyv)
            cs = base_tool.replace_for_web(dictinfo['cs'], self.keyv)
            try:
                cs = json.loads(cs.replace('\'', '\"'))
            except:
                cs = cs
            dictinfo['cs'] = cs
        return dictinfo

    def http_post(self):
        # 传入参数说明：{url:请求地址, headers:主要用户登录验证cookie, cs:请求的参数}
        reqinfo = self.re_all()
        if reqinfo['url'] != '':
            # 地址不为空，开始执行
            url = reqinfo['url']
            headers = reqinfo['headers']
            data_json = self.reqinfo['cs']
            try:
                req = requests.post(url, data=json.dumps(data_json), headers=headers, allow_redirects=False)
                if req.status_code == 200:
                    return [req.status_code, req.json(), str(str(round(req.elapsed.total_seconds(),3)) + "秒")]
                else:
                    return [req.status_code, req.text, str(str(round(req.elapsed.total_seconds(),3)) + "秒")]
            except Exception as eee:
                logger.error('post请求的错误信息' + str(eee))
                return ['666', '请求报错了', '0秒']
        else:
            return ['666', '请求报错了', '0秒']

    def http_get(self):
        # 传入参数说明：{url:请求地址, headers:主要用户登录验证cookie, cs:请求的参数}
        reqinfo = self.re_all()
        if reqinfo['url'] != '':
            # 地址不为空，开始执行
            url = reqinfo['url']
            headers = reqinfo['headers']
            params = self.reqinfo['cs']
            try:
                req = requests.get(url, params=params, headers=headers, allow_redirects=False)
                if req.status_code == 200:
                    return [req.status_code, req.json(), str(str(round(req.elapsed.total_seconds(),3)) + "秒")]
                else:
                    return [req.status_code, req.text, str(str(round(req.elapsed.total_seconds(),3)) + "秒")]
            except Exception as eee:
                logger.error('get请求的错误信息' + str(eee))
                return ['666', '请求报错了', '0秒']
        else:
            return ['666', '请求报错了', '0秒']

    def http_del(self):
        # 传入参数说明：{url:请求地址, headers:主要用户登录验证cookie, cs:请求的参数}
        reqinfo = self.re_all()
        if reqinfo['url'] != '':
            # 地址不为空，开始执行
            url = reqinfo['url']
            headers = reqinfo['headers']
            req = requests.delete(url, headers=headers, allow_redirects=False)
            if req.status_code == 200:
                return [req.status_code, req.json(), str(str(round(req.elapsed.total_seconds(),3)) + "秒")]
            else:
                return [req.status_code, req.text, str(str(round(req.elapsed.total_seconds(),3)) + "秒")]
        else:
            return ['666', '请求报错了', '0秒']

    def http_patch(self):
        # 传入参数说明：{url:请求地址, headers:主要用户登录验证cookie, cs:请求的参数}
        reqinfo = self.re_all()
        if reqinfo['url'] != '':
            # 地址不为空，开始执行
            url = reqinfo['url']
            headers = reqinfo['headers']
            data_json = reqinfo['cs']
            if isinstance(data_json, dict):
                pass
            else:
                data_json = str(data_json)
            req = requests.patch(url, headers=headers, data=str(data_json), allow_redirects=False)
            if req.status_code == 200:
                return [req.status_code, req.json(), str(str(round(req.elapsed.total_seconds(),3)) + "秒")]
            else:
                return [req.status_code, req.text, str(str(round(req.elapsed.total_seconds(),3)) + "秒")]
        else:
            return ['666', '请求报错了', '0秒']
