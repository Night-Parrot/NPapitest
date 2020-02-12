import json
import re


from common import my_log

logger = my_log.LogUtil().getLogger()


def re_fun_sql(string, keyv):
    string = str(string)
    keynames = re.findall(r'{{(.+?)}}', string)
    for name in keynames:
        try:
            string = string.replace(
                str('{{' + str(name)) + '}}', str(keyv[name]))
        except Exception:
            pass
    return string.replace('\\', '')


def re_fun_parameter(string, keyv):
    string = str(string)
    keynames = re.findall(r'{{(.+?)}}', string)
    for name in keynames:
        try:
            string = string.replace(
                str('{{' + str(name)) + '}}', str(keyv[name]))
        except Exception:
            pass
    try:
        keynames = json.loads(string.replace('\'', '\"'))
    except:
        keynames = keynames
    return keynames


def re_fun_url(string, keyv):
    string = str(string)
    keynames = re.findall(r'{{(.+?)}}', string)
    for name in keynames:
        try:
            string = string.replace(
                str('{{' + str(name)) + '}}', str(keyv[name]))
        except Exception:
            pass
    return string


# if __name__ == '__main__':
#     sql_res = "SELECT c_mc as mc,n_ssdw as ssdw,c_bh_aj as bhAj,n_gj as gj,n_xb as xb ,n_mz as mz,n_dsrlx as dsrlx,n_nl as nl FROM jyhzx.db_jyhzx.t_zx_dsr WHERE c_bh = {{ajbh}}"
#     querystring = {"offset": "{{offset}}"}
#     url = 'http://172.0.0.1:9090/{{ajbh}}/{{dsrbh}}'
#     print(re_fun_sql(sql_res))
#     print(re_fun_parameter(querystring))
#     print(re_fun_url(url))
#     # print(type(re_fun_parameter(querystring)))
