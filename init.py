# -*- coding:utf-8 -*-

import sys
import xlrd
import threading
import time

from test import Test

class Init(object):
    def __init__(self, file, platform):

        # 测试环境
        self.platform = platform

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
            # 依次调用列表
            for val in self.e_data:
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
            print(r.response_data)
            print(r.response_time)

if __name__ == '__main__':
    start = Init('./list.xlsx','test')
    start.main()
