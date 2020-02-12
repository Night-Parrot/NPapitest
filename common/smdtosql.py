# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 18:20:22 2019

@author: yinxw
"""

import queue
import openpyxl
import os
from common import my_log


logger = my_log.LogUtil().getLogger()



def read_file(file_path):
    smd = {}
    logger.info('读取文件信息:{}'.format(file_path))
    # print('读取文件信息:{}'.format(file_path))
    try:
        wb = openpyxl.load_workbook(file_path)
        sheet_col = wb['COL']
        # sheet_tab = wb.get_sheet_by_name('TAB')
    except Exception as e:
        logger.error(e)
        print('文件读取失败!!\nERROR:{}'.format(e))
    else:
        smd['schema_name'] = sheet_col['A1'].value if sheet_col['A1'].value else '请输入模式'
        for i in range(1,sheet_col.max_row):
            if sheet_col['A{}'.format(i)].value in smd and sheet_col['A{}'.format(i)].value[:2].lower() == 't_':
                smd[sheet_col['A{}'.format(i)].value].extend([[sheet_col['B{}'.format(i)].value, 
                                                               sheet_col['C{}'.format(i)].value,
                                                               sheet_col['G{}'.format(i)].value,
                                                               sheet_col['H{}'.format(i)].value,
                                                               sheet_col['AA{}'.format(i)].value]])
            elif sheet_col['A{}'.format(i)].value != None and sheet_col['A{}'.format(i)].value[:2] in ('T_','t_'):
                smd[sheet_col['A{}'.format(i)].value] = [[sheet_col['B{}'.format(i)].value, 
                                                          sheet_col['C{}'.format(i)].value,
                                                          sheet_col['G{}'.format(i)].value,
                                                          sheet_col['H{}'.format(i)].value,
                                                          sheet_col['AA{}'.format(i)].value]]
        smd['file_name'] = file_path.split('\\')[-1].split('.')[0]  
        logger.info('读取完成')
        print('读取完成')
        return smd

def write_file(filename, field_list, path, schema):
    try:
        f = open(path + '/' + filename + '.sql', mode = 'w+', encoding = 'utf-8')
    except Exception as e:
        logger.error(e)
        # print('打开文件失败!!\nERROR:{}'.format(e))
    else:
        ch = ','
        f.write('INSERT INTO {0}.{1} (\n'.format(schema, filename))
        for field in range(len(field_list)):
            if field == len(field_list) - 1:
                ch = ''
            f.write('{0}{1}\n'.format(field_list[field][0], ch))
        f.write(') VALUES (\n')
        ch = ','
        for types in range(len(field_list)):
            if types == len(field_list) - 1:
                ch = ''
            if field_list[types][4]:
                f.write('\'${{__CSVRead({0},0)}}${{__CSVRead({0},next)}}\'{2}  --{1}\n'.format(field_list[types][4], field_list[types][1], ch))
            elif field_list[types][0].lower() == 'c_bh':
                f.write('replace(public.uuid_generate_v4()||\'\',\'-\',\'\'){1}  --{0}\n'.format(field_list[types][1], ch))
            elif field_list[types][2].lower() in ('c', 'vc', 'text'):
                f.write('\'加压{0}${{__RandomString(8, 0123456789,)}}\'{1}  --{0}\n'.format(field_list[types][1], ch))
            elif field_list[types][2].lower() == 'int':
                f.write('\'${{__Random(0,10,)}}\'{1}  --{0}\n'.format(field_list[types][1], ch))
            elif field_list[types][2].lower() == 'n':
                f.write('\'${{__Random(100,999,)}}.${{__Random(1,99,)}}\'{1}  --{0}\n'.format(field_list[types][1], ch))
            elif field_list[types][2].lower() == 'dt':
                f.write('\'${{__RandomDate(yyyy-MM-dd,2015-01-01,2019-12-31,,)}} ${{__time(hh:mm:ss,)}}\'{1}  --{0}\n'.format(field_list[types][1], ch))
            elif field_list[types][2].lower() == 'd':
                f.write('\'${{__RandomDate(yyyy-MM-dd,2015-01-01,2019-12-31,,)}}\'{1}  --{0}\n'.format(field_list[types][1], ch))
            else:
                f.write('\'\'{1}  --{0}\n'.format(field_list[types][1], ch))
        f.write(');')
    finally:
        f.close()
    
def read_folder(folder_path):
    queues = queue.Queue()
    logger.info('读取文件夹信息')
    # print('读取文件夹信息')
    try:
        files = [f for f in os.listdir(folder_path) if f[-3:] == 'lsx']
    except Exception as e:
        logger.error(e)
        # print('系统找不到指定路径!!\nERROR:{}'.format(e))
        # return
    if not files:
        logger.error('没有找到xlsx结尾的文件, 请检查路径!')
        # print('没有找到xlsx结尾的文件, 请检查路径!')
        # return
    try:
        for file_name in files:
            if file_name.split('.')[0] not in [f for f in os.listdir(folder_path)]:
                os.makedirs(folder_path + '/' + file_name.split('.')[0])
    except Exception as e:
        logger.error(e)
        # print('创建文件夹失败!!\nERROR:{}'.format(e))
        # return
    else:
        path_list = [folder_path+'/'+ file for file in files]
        for path in path_list:
            date = read_file(path)
            if date:
                queues.put(date)
        return queues

if __name__ == "__main__":
    smd_path = input('请输入smd路径:')
    m_queues = read_folder(smd_path)
    if m_queues:
        while not m_queues.empty():
            smd = m_queues.get()
            for table in smd:
                if table not in ('file_name', 'schema_name'):
                    write_file(table, smd[table], smd_path + '/' + smd['file_name'], smd['schema_name'])
    input('输入回车键退出!')
