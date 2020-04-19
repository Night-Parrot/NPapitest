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



def swagger_count(all_url, cookie):
    if ',' in all_url:
        url_list = re.split(r',', all_url)
    else:
        url_list = [all_url]
    all_api_info = {}
    for url in url_list:
        if str(url)[0] != 'h':
            url = str('http://') + str(url)
        else:
            pass
         # 初始化参数，防止后续在赋值前被引用
        req = requests.get(url, headers={'cookie': cookie})
        if req.status_code == '401':
            req = requests.get(url, headers={'cookie': cookie})
        try:
            json_new = req.json()
        except Exception as ggg:
            logger.error('swagger地址返回的不数据不是json：' + str(ggg))
            return False
        caselist = []
        try:
            ssr = {}
            if json_new['basePath'] == '/':
                ssr['value'] = ''
            else:
                ssr['value'] = json_new['basePath']
            num = 0
            for path in json_new['paths']:
                for a in json_new['paths'][path]:
                    ssr['method'] = a
                    ssr['path'] = str(path)
                    url_path = '/' + ssr['method'] + ssr['value'] + ssr['path']
                    url_path = re.sub(r'{[^\s]*?}', '{*}', url_path)
                    caselist.append(url_path)
            all_info = {'counts': len(caselist), 'info': caselist}
            b = re.findall(r'[a-zA-z]+://[^\s]*?/', url)
            all_api_info[b[0]] = all_info
        except Exception as aaa:
            logger.error('解析swagger返回数据最外层报错：' + str(eee))
            return False
    return all_api_info


if __name__ == '__main__':
    aaa = swagger_count('http://172.18.17.177:30120/v2/api-docs', '')
    print(aaa)
