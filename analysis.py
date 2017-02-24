# -*- coding:utf-8 -*-

import os
import csv

'''
        接口测试结果 CSV 文件数据分析
'''

class Analysis(object):
        """docstring for Analysis"""
        def __init__(self, file, delimiter=','):
                if os.path.isfile(file):
                        self.file = file
                else:
                        raise ValueError('文件不存在')
                self.delimiter = delimiter

        def main(self):
                time = []
                with open(self.file, 'r') as f:
                        reader = csv.DictReader(f, delimiter = self.delimiter)
                        print(reader.fieldnames)
                        # print(reader.line_num)
                        for row in reader:
                                time.append(dict(row)['response_time'])
                                print(dict(row))

an = Analysis('./csv/会员信息.csv', '|')
an.main()
