from main import all_dbc
import json
import math
import os
import re
import sys
import vthread
import time

import pandas as pd
from jsondiff import diff

from common import (all_assert_new, base_tool, db_clints_for_web, httpreq,
                    my_log, re_fun_for_web)
# from db_mod import db_connect

o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append('..')
logger = my_log.LogUtil().getLogger()
from web import JSONEncoder




@vthread.pool()
def run_caselist(zxid, ylbh, case_info_all):
    # logger.info('子进程id: ' + str(os.getpid()))
    # 初始化成功失败信息，用于每次计算成功率和通过率
    logger.info("···开始执行用例···")
    try:
        db_case = db_clints_for_web.db_clints(case_info_all[2])
    except Exception as eee:
        logger.error('子进程内，用例数据库连接异常，原因：' + str(eee))
        try:
            update_zt = "UPDATE db_apitesting.t_at_zxxx SET n_zt = '2' WHERE c_bh = '%s';" % zxid
            all_dbc.pg_update_operator(update_zt)
        except Exception as eee:
            logger.error("数据库连接失败，更新执行状态时报的错" + str(eee))
            return False
            # os._exit(0)
    if db_case == False:
        logger.error("子进程创建数据库连接失败")
        try:
            update_zt = "UPDATE db_apitesting.t_at_zxxx SET n_zt = '2' WHERE c_bh = '%s';" % zxid
            all_dbc.pg_update_operator(update_zt)
        except Exception as eee:
            logger.error("数据库连接失败，更新执行状态时报的错" + str(eee))
            return False
            # os._exit(0)
    '''
    准备开始初始化参数，用于后续用例的执行
    由于其他方法在调用的同时，需要将参数化后的执行参数也传进去
    所以需要在这里进行参数化
    '''
    for re_key in case_info_all[0]:
        case_info_all[0][re_key] = base_tool.replace_for_web(
            case_info_all[0][re_key])
    # logger.info('替换后的参数：' + str(case_info_all[0]))
    '''
    计算所有需要执行的用例数量，给后续计算进度使用
    '''
    all_case_num = 0
    for case in range(case_info_all[1][0]):
        if case_info_all[1][1]['sfzx'][case] == '是':
            all_case_num = all_case_num + 1
    logger.info('开始执行')
    res_info = {'当前条数': 0, '请求成功': 0, '请求失败': 0, '验证通过': 0, '验证失败': 0}
    for case in range(case_info_all[1][0]):
        # logger.info('执行过程中的参数：' + str(case_info_all[0]))
        if case_info_all[1][1]['sfzx'][case] == '是':
            res_info['当前条数'] = res_info['当前条数'] + 1
            case_name = case_info_all[1][1]['name'][case]
            url = base_tool.replace_for_web(
                case_info_all[1][1]['url'][case], case_info_all[0])
            url = url
            method = case_info_all[1][1]['method'][case]
            cs = base_tool.replace_for_web(
                case_info_all[1][1]['cs'][case], case_info_all[0])
            try:
                cs = json.loads(cs.replace('\'', '\"'))
            except:
                cs = cs
            front_sql = case_info_all[1][1]['front_sql'][case]
            if front_sql != '':
                front_sql = base_tool.sql_split(front_sql)
                db_sql = db_clints_for_web.db_tools(
                    front_sql, db_case, case_info_all[0])
                db_sql.front_back_sql_run()
            else:
                pass
            httpinfo = {}
            response = []
            httpinfo['url'] = case_info_all[1][1]['url'][case]
            httpinfo['cs'] = case_info_all[1][1]['cs'][case]
            httpinfo['headers'] = case_info_all[1][1]['headers'][case]
            httpreq_now = httpreq.httpclints(httpinfo, case_info_all[0])
            if case_info_all[1][1]['method'][case].upper() == 'POST':
                response = httpreq_now.http_post()
            elif case_info_all[1][1]['method'][case].upper() == 'GET':
                response = httpreq_now.http_get()
            elif case_info_all[1][1]['method'][case].upper() == 'PATCH':
                response = httpreq_now.http_patch()
            elif case_info_all[1][1]['method'][case].upper() == 'DELETE':
                response = httpreq_now.http_del()
            else:
                pass
            status = response[0]
            req_time = response[2]
            response = response[1]
            sql_res = ''
            if status == 200:
                if case_info_all[1][1]['wait_time'][case] != '':
                    try:
                        time.sleep(float(case_info_all[1][1]['wait_time'][case]))
                    except Exception as eee:
                        logger.error('等待时间错误：' + str(eee))
                res_info['请求成功'] = res_info['请求成功'] + 1
                sql_res = case_info_all[1][1]['sql_res'][case]
                if sql_res != '':
                    sql_res = base_tool.sql_split(sql_res)
                    db_sql = db_clints_for_web.db_tools(
                        sql_res, db_case, case_info_all[0])
                    sql_res = db_sql.res_sql_run()
                    if str(sql_res) == 'False':
                        sql_res = {}
                    elif len(sql_res) == 1 and 'countsum' in str(sql_res):
                        sql_res = sql_res['countsum']
                    else:
                        sql_res = sql_res
                else:
                    sql_res = {}
                if case_info_all[1][1]['yzfs'][case] != '=':
                    if case_info_all[1][1]['zdy_res'][case] != '':
                        try:
                            zdy_res = case_info_all[1][1]['zdy_res'][case]
                            zdy_res = base_tool.replace_for_web(zdy_res, case_info_all[0])
                            zdy_res = json.loads(str(zdy_res))
                            if str(zdy_res) == '[]':
                                sql_res = case_info_all[1][1]['zdy_res'][case]
                            elif isinstance(zdy_res, list) and len(sql_res) == 0:
                                sql_res = zdy_res
                            else:
                                for key in zdy_res:
                                    if key in sql_res.keys():
                                        if isinstance(zdy_res[key], list) and isinstance(sql_res[key], list) and len(zdy_res[key]) == 1 and len(sql_res[key]) == 1:
                                            sql_res[key] = [
                                                {**zdy_res[key][0], **sql_res[key][0]}]
                                        else:
                                            pass
                                    else:
                                        sql_res[key] = zdy_res[key]
                        except Exception as eee:
                            logger.error(
                                '这是在将sql_res和zdy_res合并时的错误信息：' + str(eee))
                            sql_res = case_info_all[1][1]['zdy_res'][case]
                    else:
                        pass
                    sql_res = json.dumps(sql_res, ensure_ascii=False)
                    response = json.dumps(response, ensure_ascii=False)
                    sql_res = json.loads(sql_res)
                    response = json.loads(response)
                    matchinfo = diff(sql_res, response, syntax='symmetric')
                    matchinfo_r = all_assert_new.diff_json_match(
                        matchinfo, [], [], []).find_diff()  # 不要乱用自定义默认值函数，血的教训....  T_T
                else:
                    zdy_res = case_info_all[1][1]['zdy_res'][case]
                    zdy_res = base_tool.replace_for_web(zdy_res, case_info_all[0])
                    zdy_res = json.loads(str(zdy_res))
                    sql_res = json.dumps(sql_res, ensure_ascii=False, cls=JSONEncoder.CustomJsonEncoder)
                    sql_res = json.loads(sql_res)
                    logger.info(str(zdy_res))
                    logger.info(str(sql_res))
                    matchinfo = diff(sql_res, zdy_res, syntax='symmetric')
                    matchinfo_r = all_assert_new.diff_json_match(
                        matchinfo, [], [], []).find_diff()  # 不要乱用自定义默认函数，血的教训....  
                # 处理未设置任何验证内容时的情况，diff_json_match方法会返回False，False时不进行匹配，match_info直接赋值为接口返回结果
                if matchinfo_r == False:
                    res_info['验证通过'] = res_info['验证通过'] + 1
                    match_status = '未验证'
                    match_info = response
                else:
                    # 匹配结果为空或缺少字段，都算未通过
                    if len(matchinfo_r['匹配结果']) != 0 or len(matchinfo_r['返回值缺少']) != 0:
                        match_status = '不通过'
                        match_info = matchinfo_r
                        res_info['验证失败'] = res_info['验证失败'] + 1
                    else:
                        match_status = '通过'
                        res_info['验证通过'] = res_info['验证通过'] + 1
                        match_info = matchinfo_r
                    if case_info_all[1][1]['back_sql'][case] != '':
                        back_sql = base_tool.sql_split(
                            case_info_all[1][1]['back_sql'][case])
                        db_sql = db_clints_for_web.db_tools(
                            back_sql, db_case, case_info_all[0])
                        db_sql.front_back_sql_run()
            else:
                res_info['请求失败'] = res_info['请求失败'] + 1
                res_info['验证失败'] = res_info['验证失败'] + 1
                match_status = '接口请求异常'
                match_info = response
            # 插入执行信息
            zxxx_insert = "INSERT INTO db_apitesting.t_at_qqxx(c_bh, c_bh_zx, n_xh, n_qqmc, c_qqdz, c_xysj, dt_zxsj, n_jkzt, c_yzjg, c_qqcs, c_yqfhz, c_sjfhz, c_bh_yl, c_xylx, c_matchinfo)"\
                " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', now(), '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (base_tool.next_id(), zxid, res_info['当前条数'],
                                                                                                                          case_name, url, req_time, status, match_status, str(
                    cs).replace('\'', '\"'), str(sql_res).replace('\'', '\"'), str(response).replace('\'', '\"'),
                    ylbh, method.replace('\'', '\"'), str(match_info).replace('\'', '\"').replace('\\', ''))
            try:
                all_dbc.pg_insert_operator(zxxx_insert)
            except Exception as eee:
                logger.error("插入接口调用信息时失败：" + str(eee))
            '''
            计算进度比例
            '''
            jd = round(int(res_info['当前条数'])/all_case_num, 4) * 100
            # 更新用例执行百分比    res_info = {'请求成功': 0, '请求失败': 0, '验证通过': 0, '验证失败': 0}
            zxxx_jsjg = "UPDATE db_apitesting.t_at_zxxx SET c_jd = '%s', c_fgl = '%s', c_cgl = '%s', c_tgl = '%s', c_cg = '%s', c_wcg = '%s', c_tg = '%s', c_wtg = '%s' "\
                        "WHERE c_bh = '%s';" % (jd, 100, res_info['请求成功']/all_case_num, res_info['验证通过']/all_case_num, res_info['请求成功'],
                                                res_info['请求失败'], res_info['验证通过'], res_info['验证失败'], zxid)
            try:
                all_dbc.pg_update_operator(zxxx_jsjg)
            except Exception as eee:
                logger.error("更新执行数据时报的错" + str(eee))
            '''
            开始提取返回值中的参数
            '''
            try:
                if case_info_all[1][1]['res_for_key'][case] != '':
                    try:
                        kv_path = case_info_all[1][1]['res_for_key'][case]
                        for_key = response
                        key_name = re.split(r'\:', kv_path)
                        key_path = re.split(r'\.', key_name[1])
                        for value_path in key_path:
                            if value_path == '*':
                                pass
                            else:
                                for_key = for_key[value_path]
                        case_info_all[0][key_name[0]] = for_key
                    except Exception as eee:
                        update_zt = "UPDATE db_apitesting.t_at_zxxx SET n_zt = '2' WHERE c_bh = '%s';" % zxid
                        all_dbc.pg_update_operator(update_zt)
                        logger.error('从返回值提起参数报错：' + str(eee))
                        logger.info('中断执行') 
                        logger.info("开始关闭数据链接")
                        db_clints_for_web.db_tools().db_close()
                        logger.info("完成关闭数据链接")
                        return False
            except Exception as eee:
                # logger.error("兼容旧版用例" + str(eee))
                pass
            if status == '666':
                try:
                    update_zt = "UPDATE db_apitesting.t_at_zxxx SET n_zt = '2' WHERE c_bh = '%s';" % zxid
                    all_dbc.pg_update_operator(update_zt)
                    logger.error('调用被测服务报错了')
                    logger.info("开始关闭数据链接")
                    db_clints_for_web.db_tools().db_close()
                    logger.info("完成关闭数据链接")
                    return False
                    # os._exit(0)
                except Exception as eee:
                    logger.error("更新执行状态时报的错" + str(eee))
                    logger.info("开始关闭数据链接")
                    db_clints_for_web.db_tools().db_close()
                    logger.info("完成关闭数据链接")
                    return False
                    # os._exit(0)
        else:
            pass
    # 关闭用例执行时的数据库链接
    logger.info("开始关闭数据链接")
    db_clints_for_web.db_tools().db_close()
    logger.info("完成关闭数据链接")
    # 更新执行状态
    try:
        update_zt = "UPDATE db_apitesting.t_at_zxxx SET n_zt = '1' WHERE c_bh = '%s';" % zxid
        all_dbc.pg_update_operator(update_zt)
    except Exception as eee:
        logger.error("更新执行状态时报的错" + str(eee))
    logger.info('用例执行结束')
