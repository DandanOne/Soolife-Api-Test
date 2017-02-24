# -*- coding:utf-8 -*-

import sys
import xlrd
import threading
import time
import csv
import os
import datetime

from test import Test

class Init(object):
    def __init__(self, file, platform='test', csv_file=''):

        # 测试环境
        self.platform = platform
        #self.csv_file = './log_csv.csv' if  not csv_file else csv_file

        # 读取列表
        data = xlrd.open_workbook(file)
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols

        # 标题
        colnames =  table.row_values(0)

        # 数据转为 dict
        self.e_data = []
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            if row:
                row_data = {}
                for i in range(len(colnames)):
                    row_data[colnames[i]] = row[i]
                if int(row_data['test_it']) != 0:
                    self.e_data.append(row_data)

    # 执行
    def main(self):
        if self.e_data:
            keys = list(self.e_data[0].keys())
            keys.remove('test_it')
            keys.extend(['response_data','response_time','response_code','test_time'])

            # 依次调用列表
            for val in self.e_data:
                self.csv_file ='./csv/' + val['remark'] + '.csv'
                if not os.path.isfile(self.csv_file):
                    self.write_csv(header = keys)

                print('Sterting Test API:' + val['remark'] + ' ;Address :'+val['url'])

                # 多线程
                container = []
                for x in range(int(val['concurrent_num'])):
                    container.append(threading.Thread(target=self.deal_request, args=(val,)))

                for i in container:
                    i.start()

                for i in container:
                    i.join()

                time.sleep(2)

    # 调用
    def deal_request(self, r_args):
        method = r_args['method']
        online = int(r_args['online_status'])
        request_nums = int(r_args['requests_nums'])
        concurrent_num = int(r_args['concurrent_num'])
        url = r_args['url']
        data = r_args['data']

        for e in range(request_nums):
            if online:
                r = Test('app', self.platform, r_args['username'], r_args['password'])
            else:
                r = Test('app', self.platform)

            if method == 'get':
                r.get_request(url)
            elif method == 'post':
                r.post_request(url, data)
            elif method == 'put':
                r.put_request(url, data)
            elif method == 'delete':
                r.delete_request(url, data)
            else:
                print('暂不支持此种请求方式')
                exit(0)
            print(r.response_code, end='\n')
            #print(r.response_time, end='\n')
            #print(r.response_data, end='\n')
            self.write_csv(row = [url, method, data, request_nums, concurrent_num, online, \
                                  r_args['username'], r_args['password'], r_args['remark'], \
                                  r.response_data,r.response_time,r.response_code,str(int(time.time()))])

    # 写测试记录
    def write_csv(self, row=None, header=None):
    	with open(self.csv_file, 'a') as c:
    		writer = csv.writer(c, delimiter = '|')
    		if header:
    			writer.writerow(header)
    		else:
    			writer.writerow(row)


if __name__ == '__main__':
    try:
        start = Init('./list.xlsx', 'test')
        start.main()
    except Exception as e:
        print(e)
    else:
        print('测试完成')
    finally:
        print('测试结束')
