import pandas as pd

from common import my_log, base_tool

logger = my_log.LogUtil().getLogger()


def read_case(file_path):
    try:
        # df_keywords = pd.read_excel(
        #     file_path, sheet_name='keywords', keep_default_na=False)
        # df_keywords = kvlist
        # keep_default_na是用来过滤空单元格返回的nan的
        df_caselist = pd.read_excel(
            file_path, sheet_name='caselist', keep_default_na=False)
        df_dbinfo = pd.read_excel(
            file_path, sheet_name='db_config', keep_default_na=False)
    except Exception as eee:
        logger.error('读取用例出错，sheet名称不正确或缺失：' + str(eee))
        return False
    '''
    参数化不再在读取用例时进行，放到用例执行前去执行----2019-11-15
    # keywordlist = {}
    # for rows in df_keywords.index.values:
    #     row_data = df_keywords.loc[rows].values
    #     # 调用公用工具，生成初始化方法对应的参数
    #     res_key = base_tool.default_function(row_data[1])
    #     if res_key == False:
    #         keywordlist[row_data[0]] = row_data[1]
    #     else:
    #         keywordlist[row_data[0]] = res_key
    # for key in df_keywords:
    #     # 调用公用工具，生成初始化方法对应的参数
    #     res_key = base_tool.default_function(df_keywords[key])
    #     if res_key == False:
    #         keywordlist[key] = df_keywords[key]
    #     else:
    #         keywordlist[key] = res_key
    '''
    casedict = df_caselist.reindex().to_dict()
    rows_all = len(df_caselist.index.values)
    db_info = {}
    for rows in df_dbinfo.index.values:
        row_data = df_dbinfo.loc[rows].to_dict()
        db_info[df_dbinfo.loc[rows, ['name']].values[0]] = row_data
    return [[rows_all, casedict], db_info]



def read_keylist(file_path):
    try:
        df_keywords = pd.read_excel(
            file_path, sheet_name='keywords', keep_default_na=False)
    except Exception as eee:
        logger.error('读取用例keylist出错，sheet名称不正确或缺失：' + str(eee))
    keywordlist = {}
    for rows in df_keywords.index.values:
        row_data = df_keywords.loc[rows].values
        keywordlist[row_data[0]] =row_data[1]
    return keywordlist