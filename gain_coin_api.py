#-*- coding=utf-8 -*-
from test import Test

import threading

# request_num 请求数量
def gain_coin(n):
    request_num = 10
    print('Starting Request : '+ str(n) + '\n')
    r = Test('app', 'test', '18671188982', '123456')
    for v in range(request_num):
        print(str(n) + '--- ' + str(v) + '\n')
        r.get_request('/member/assets/coin')
        print(str(r.response_code) + '\n')
        print(r.response_data, '\n')

def main(num):
    threads = []
    for x in range(0, num):
        threads.append(threading.Thread(target=gain_coin,args=(x,)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    try:
        main(4)
    except Exception as e:
        print(e)
    else:
        print('end-------')
