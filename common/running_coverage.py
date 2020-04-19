import re, numpy




def make_path_info(path_list):
    path_info = {}
    for running_path in path_list:   
        b = re.findall(r'[a-zA-z]+://[^\s]*?/', running_path[1])
        if b[0] in path_info.keys():
            pass
        else:
            path_info[b[0]] = []
        n = 1
        for index_str in re.finditer('/', running_path[2]):
            if n == 3:
                path = running_path[2][index_str.span()[0]:]
                fin_path = '/' + running_path[0] + path
                break
            else:
                n = n + 1
        ggg = re.sub(r'{{[^\s]*?}}', '{*}', fin_path)
        path_info[b[0]].append(ggg)
    for url in path_info:
        path_info[url] = list(set(path_info[url]))
        path_info[url] = {'counts': len(path_info[url]), 'info': path_info[url]}
    return path_info


def cover_cal(api_counts, path_list):
    if isinstance(api_counts, int):
        cot = 0
        for ip_info in path_list:
            if path_list[ip_info]['counts'] > cot:
                cot = path_list[ip_info]['counts']
            else:
                pass
        try:
            cover = int(cot)/int(api_counts)
        except:
            return False
        cover = round(cover, 4)
        return cover
    else:
        '''
        这是粗略计算，仅计算总数，不对具体接口名称做校验，有点失真
        cov_list = []
        for ip_info_run in path_list:
            if ip_info_run in api_counts.keys():
                cov_one = int(path_list[ip_info_run]['counts'])/int(api_counts[ip_info_run]['counts'])
                if cov_one > 1:
                    cov_one = 1.00
                else:
                    cov_one = round(cov_one, 2)
                cov_list.append(cov_one)
            else:
                pass
        print(cov_list)
        if len(cov_list) == 0:
            return '计算异常'
        else:
            average_a = numpy.mean(cov_list)
            average_a = round(average_a, 2)
            return average_a
        '''
        cov_list = []
        for ip_info_run in path_list:
            if ip_info_run in api_counts.keys():
                n = 0
                for api_name in path_list[ip_info_run]['info']:
                    if api_name in api_counts[ip_info_run]['info']:
                        n = n + 1
                    else:
                        pass
                if n == 0:
                    pass
                else:
                    cov_one = int(n)/int(api_counts[ip_info_run]['counts'])
                    if cov_one > 1:
                        cov_one = 1
                    else:
                        cov_one = round(cov_one, 4)
                    cov_list.append(cov_one)
            else:
                pass
        print(cov_list)
        if len(cov_list) == 0:
            return '计算异常'
        else:
            average_a = numpy.mean(cov_list)
            average_a = round(average_a, 4)
            return average_a





if __name__ == '__main__':
    a = []
    b = 21
    c = cover_cal(b, make_path_info(a))
    print(c)
    print(type(c))
            
