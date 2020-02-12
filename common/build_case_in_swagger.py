import re

import requests

from common import my_log

logger = my_log.LogUtil().getLogger()

def swagger(url, cookie):
    if str(url)[0] != 'h':
        url = str('http://') + str(url)
    else:
        pass
    json_new = {} # 初始化参数，防止后续在赋值前被引用
    req = requests.get(url, headers={'cookie': cookie})
    if req.status_code == '401':
        req = requests.get(url, headers={'cookie': cookie})
    try:
        json_new = req.json()
    except Exception as ggg:
        logger.error('swagger地址返回的不数据不是json：' + str(ggg))
    caselist = []
    try:
        name = {}
        url = {}
        port = {}
        baseurl = {}
        name['key'] = 'name'
        name['value'] = json_new['info']['title']
        url_info = re.findall(r'(.*?):', str(json_new['host']))
        port_info = re.findall(r':(.*)', str(json_new['host']))
        url['key'] = 'url'
        url['value'] = url_info[0]
        port['key'] = 'port'
        port['value'] = port_info[0]
        if json_new['basePath'] == '/':
            baseurl['key'] = 'baseurl'
            baseurl['value'] = ''
        else:
            baseurl['key'] = 'baseurl'
            baseurl['value'] = json_new['basePath']
        infolist = [name, url, port, baseurl]
        num = 0
        for path in json_new['paths']:
            for a in json_new['paths'][path]:
                query = {}
                body = {}
                try:
                    for b in json_new['paths'][path][a]['parameters']:
                        if b['in'] == 'path':
                            pass
                        elif b['in'] == 'query':
                            query[b['name']] = b['description']
                        elif b['in'] == 'body':
                            bbb = re.findall(r'#/definitions/(.*)\'', str(b))
                            for c in json_new['definitions'][bbb[0]]['properties']:
                                body[c] = json_new['definitions'][bbb[0]
                                                                  ]['properties'][c]['description']
                        else:
                            pass
                except Exception as eee:
                    logger.error('解析swagger返回数据报错：' + str(eee))
                    pass
                ssr = {}
                num = num + 1
                ssr['num'] = num
                ssr['name'] = json_new['paths'][path][a]['tags'][0] + \
                    ':' + json_new['paths'][path][a]['summary']
                ssr['method'] = a
                ssr['url'] = r'http://' + '{{url}}' + ':' + '{{port}}' + \
                    '{{baseurl}}' + \
                    str(path).replace('{', '{{').replace('}', '}}')
                ssr['headers'] = '{"Content-Type": "application/json"}'
                ssr['cs'] = ''
                if len(query) == 0:
                    pass
                else:
                    ssr['cs'] = str(query).replace('\'', '\"')
                if len(body) == 0:
                    pass
                else:
                    ssr['cs'] = str(body).replace('\'', '\"')
                ssr['sfzx'] = '否'
                ssr['wait_time'] = ''
                ssr['front_sql'] = ''
                ssr['sql_res'] = ''
                ssr['yzfs'] = ''
                ssr['zdy_res'] = ''
                ssr['back_sql'] = ''
                ssr['res_for_key'] = ''
                caselist.append(ssr)
        return [caselist, infolist]
    except Exception as aaa:
        logger.error('解析swagger返回数据最外层报错：' + str(eee))



# if __name__ == '__main__':
#     aaa = swagger('http://172.18.12.118:9070/t3e-jyhzx/v2/api-docs', 'userToken=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtc3AtZ2F0ZXdheSIsInVzZXJJZCI6IjE2MDM1MTE0MzMiLCJpcCI6IjE3Mi4xOC40OS4xOCIsImV4cERhdGUiOjE1NjU2NjIwODQyMDQsInRndCI6IlRHVC0zMjc4LXlXRjNncWpBcFBtOUk2S2FmSExkejk5ZnpyN250NWZNV05aWkRKb2JXYmVxekE2bDVULWNhcyIsInN0IjoiU1QtMTk2MzYtUmVPTkpzMk9UQ0F2UU9vZzc1ZG0tY2FzIiwiaWF0IjoxNTY1NjYyMDI0fQ.3D5BJmcmIuyoLRg_Kf4COg5rRnIQb6E_7CgAuk6MOWjrwc5WSeEnuZr8Bj44XOxr8NRB9rBOc4H_rOn_pajrlA; JSESSIONID=node01asor0qltp5qkaahs449h51wg15132.node0')
#     print(aaa)
