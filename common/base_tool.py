from common import my_log
import re
import os
import zipfile
import sys
import uuid
import re
import random
import time
from faker import Factory
import datetime


o_path = os.getcwd()
sys.path.append(o_path)
logger = my_log.LogUtil().getLogger()
faker = Factory.create('zh_CN')


def next_id():
    return uuid.uuid4().hex


def sql_split(str_sql):
    sql_list = []
    groups_list = re.split(r';', str(str_sql))
    for groups in groups_list:
        sql_dict = {}
        # 由于sql主体中也会包含':'，所以用正则匹配会有问题，改成获取第一个':'的位置，来对字符串分组
        if len(groups) == 0:
            pass
        else:
            try:
                index_num = str(groups).index(':')
                sql_dict[str(groups)[:index_num]] = str(groups)[index_num + 1:]
                sql_list.append(sql_dict)
            except Exception as eee:
                logger.error('sql分组报错：' + str(eee))
                logger.info('报错的具体sql：' + str(groups))
    return sql_list


def default_function(key_name):
    if str(key_name).upper() == '!UUID':
        return uuid.uuid4().hex
    else:
        return False


def replace_for_web(str_r, keywords={}):
    all_re = re.findall(r"{{(.+?)}}", str_r)
    if len(all_re) == 0:
        return str_r
    else:
        keynames = []
        for keyname in keywords:
            keynames.append(keyname)
        for xh in range(len(all_re)):
            if re.match(r"!randint\((.+?)\)", all_re[xh]):
                randnum = re.findall(r"!randint\((.+?)\)", all_re[xh])
                randnum = re.split(",", randnum[0])
                randnum = random.randint(int(randnum[0]), int(randnum[1]))
                str_r = str_r.replace("{{" + all_re[xh] + "}}", str(randnum))
            elif all_re[xh] == '!uuid':
                str_r = str_r.replace(
                    "{{" + all_re[xh] + "}}", uuid.uuid4().hex)
            elif re.match(r"!randtext\((.+?)\)", all_re[xh]):
                randnum = re.findall(r"!randtext\((.+?)\)", all_re[xh])
                try:
                    text_all = faker.paragraph(nb_sentences=1000, variable_nb_sentences=True).replace(
                        '.', '')[:int(randnum[0])]
                    str_r = str_r.replace(
                        "{{" + all_re[xh] + "}}", str(text_all))
                except:
                    str_r = str_r
            elif all_re[xh] == '!address':
                address = faker.address()[:-6]
                str_r = str_r.replace("{{" + all_re[xh] + "}}", str(address))
            elif all_re[xh] == '!name':
                name = faker.name()
                str_r = str_r.replace("{{" + all_re[xh] + "}}", str(name))
            elif all_re[xh] == '!job':
                job = faker.job()
                str_r = str_r.replace("{{" + all_re[xh] + "}}", str(job))
            elif all_re[xh] == '!company':
                company = faker.company()
                str_r = str_r.replace("{{" + all_re[xh] + "}}", str(company))
            elif re.match(r"!now\(\S*\)", all_re[xh]):
                date_type = re.findall(r"!now\((.+?)\)", all_re[xh])
                now = faker.date_time_between_dates(
                    datetime_start=None, datetime_end=None, tzinfo=None)
                if len(date_type) == 0:
                    str_r = str_r.replace("{{" + all_re[xh] + "}}", str(now))
                elif date_type[0] == 'ymd':
                    str_r = str_r.replace(
                        "{{" + all_re[xh] + "}}", str(now)[:10])
                elif date_type[0] == 'hms':
                    str_r = str_r.replace(
                        "{{" + all_re[xh] + "}}", str(now)[-8:])
                else:
                    str_r = str_r.replace("{{" + all_re[xh] + "}}", str(now))
            elif re.match(r"!randdate\((.+?)\)", all_re[xh]):
                date_info = re.findall(r"!randdate\((.+?)\)", all_re[xh])
                date_info = re.split(",", date_info[0])
                if len(date_info) == 2:
                    try:
                        date_time = faker.date_time_between_dates(
                            datetime_start=datetime.date(int(date_info[0][:4]), int(
                                date_info[0][5:6]), int(date_info[0][7:8])),
                            datetime_end=datetime.date(int(date_info[1][:4]), int(date_info[1][5:6]), int(date_info[1][7:8])))
                        str_r = str_r.replace(
                            "{{" + all_re[xh] + "}}", str(date_time))
                    except:
                        str_r = str_r
                elif len(date_info) == 3:
                    try:
                        date_time = faker.date_time_between_dates(
                            datetime_start=datetime.date(int(date_info[0][:4]), int(
                                date_info[0][5:6]), int(date_info[0][7:8])),
                            datetime_end=datetime.date(int(date_info[1][:4]), int(date_info[1][5:6]), int(date_info[1][7:8])))
                        if date_info[2] == 'ymd':
                            str_r = str_r.replace(
                                "{{" + all_re[xh] + "}}", str(date_time)[:10])
                    except:
                        str_r = str_r
                else:
                    str_r = str_r
            elif all_re[xh] in keynames:
                str_r = str_r.replace(
                    "{{" + all_re[xh] + "}}", keywords[all_re[xh]])
            else:
                pass
    return str_r


def ZipFile(path, destPath):
    try:
        zf = zipfile.ZipFile(destPath, "w", zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(path):
            # 将当前目录替换为空，即以当前目录为相对目录，如果当前目录下面还存在文件夹，则fpath为 【/子目录】
            logger.info(dirnames)
            fpath = dirpath.replace(path, "")
            fpath = fpath and fpath + os.sep or ""
            for file in filenames:
                zf.write(os.path.join(dirpath, file), fpath+file)
        zf.close()
    except Exception as eee:
        logger.error('压缩文件报错:' + str(eee))


'''
这是一个用来处理sybase查询结果的方法，目的是为了将查询结果转化为dict
当查询结果为多条时，逐条转化为dict并封装到一个list中返回
'''


def row_name(sql, sql_res):
    aaa = re.findall('SELECT(.+?)FROM', sql)
    bbb = re.split(',', aaa[0])
    names = []
    for name in bbb:
        name = name.replace(' as ', ' AS ')
        ccc = re.findall('AS (.*)', name)
        if len(ccc) == 0:
            ccc = [name]
        p = re.compile(r"^\s+|\s+$")
        ccc[0] = re.sub(p, '', ccc[0])
        names.append(ccc[0])
    if len(sql_res[0]) == len(names):
        if len(sql_res) > 1:
            res_all = []
            for res in sql_res:
                dict_row = {}
                for num in range(len(res)):
                    dict_row[names[num]] = res[num]
                res_all.append(dict_row)
        else:
            res_all = {}
            for num in range(len(sql_res[0])):
                res_all[names[num]] = sql_res[0][num]
    else:
        return False
    return res_all


if __name__ == '__main__':
    db = "1;2;3;4;5;"
    print(re.split(r';', str(db)))
    # print('@uuid'.upper())
    for num in range(50):
        print(replace_for_web('{{!uuid}}'))
