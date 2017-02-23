# -*- coding=utf-8 -*-

import requests
import configparser
import os.path as op
import json

import threading
import time

class Test(object):
    '接口测试-HTTP请求类'
    config_file = './config/config.ini'

    def __init__(self, auth_type, env, username='', password=''):
        # Load Config File
        if op.exists(self.config_file) and op.isfile(self.config_file):
            with open(self.config_file, 'r') as cfgfile:
                config_pars = configparser.ConfigParser()
                config_pars.readfp(cfgfile)
                self.config = {}
                _tmp_config_items = config_pars.sections()
                for v in _tmp_config_items:
                    self.config[v] = dict(config_pars.items(v))
        else:
            raise IOError('Config file ERROR,Open config file failed!')

        # Set the Environment
        if env in self.config['url_base'].keys():
            self.env = env
        else:
            raise ValueError('Don\'t support the ' + str(env) + ' environment')

        # API AUTH
        if auth_type in self.config:
            self.auth_key = self.config[auth_type]['key']
            self.auth_secret = self.config[auth_type]['secret']
        else:
            raise ValueError('Config File Don\'t support this AUTH')

        # Request Header
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        # Request Object
        self.s = requests

        # Do Login
        if username and password:
            self.login(username, password)


    def login(self, username, password):
        'Login,Get the token'
        post = {'username':username,'password':password}

        self.post_request('/account/login', post)
        if self.response_code == 200:
            self.login_info = self.response_data
            self.add_header('token', self.login_info.get('token',''))


    def add_header(self, key='', value=''):
        'Add Header'
        if key:
            self.headers[key] = value


    def build_url(self, api):
        'Build Request URL'
        if self.env in self.config['url_base'].keys():
            return self.config['url_base'][self.env] + api
        else:
            raise ValueError('Don\'t find this kind of Api config')


    def format_response(self, response):
        self.response_code = response.status_code
        self.response_data = dict(response.json())


    def get_request(self, api):
        'GET Request'
        req_url = self.build_url(api)
        res = self.s.get(req_url, auth=(self.auth_key,self.auth_secret), headers=self.headers)
        self.format_response(res)


    def post_request(self, api, data, type='json'):
        'Post Request'
        req_url = self.build_url(api)
        res = self.s.post(req_url,data = json.dumps(data), auth=(self.auth_key,self.auth_secret), headers=self.headers)
        self.format_response(res)

if __name__ == '__main__':
    try:
        t = Test('app', 'local', 'aaaa', '123456');
        for i in range(100):
            t.get_request('/member/assets/coin')
            print(t.response_code)
    except Exception as e:
        print(e)
    else:
        print('End----')
