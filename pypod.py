#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2
import sys
import json
import socket
import time

import functools


def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s begin call' % (text, func.__name__))
            func(*args, **kw)
            print('%s %s end call' % (text, func.__name__))
        return wrapper
    if isinstance(text, str):  # 如果用户传入自定义log头，直接调用decorator装饰器
        return decorator
    function = text  # 如果用户没有传入自定义log头，log将以函数为参数，所以将传入函数参数传到decorator装饰器，并将默认log替换text。
    text = "execute:"
    return decorator(function)


class DnsPod(object):
    '''
    id, token
    '''
    @log
    def __init__(self, id, token):
        self.id = id
        self.token = token
        self.get_domain_id()
        self.get_record_list()
        self.sub_domain = "www"
        self.format = "json"
        self.current_ip = None
        self.temp_ip = None

    @log
    def get_domain_id(self):
        '''
        get_domain_id
        '''
        try:
            data = "login_token=%s,%s&format=json" % (self.id, self.token)
            ret_data = urllib2.urlopen(
                "https://dnsapi.cn/Domain.List", data=data)
            json_data = ret_data.readline()
            data = json.loads(json_data)

            self.domain_id = data["domains"][0]["id"]
            return True
        except Exception, e:
            print e
            return False

    @log
    def get_record_list(self):
        try:
            data = "login_token=%s,%s&format=json&domain_id=%s" % (
                self.id, self.token, self.domain_id)
            ret_data = urllib2.urlopen(
                "https://dnsapi.cn/Record.List", data=data)
            json_data = ret_data.readline()
            data = json.loads(json_data)
            records = data["records"]
            self.records = records
            return True

        except Exception, e:
            print e
            return False

    @log
    def get_ip(self):
        sock = socket.create_connection(('ns1.dnspod.net', 6666))
        ip = sock.recv(16)
        sock.close()
        self.temp_ip = ip
        return ip

    @log
    def ip_change(self):
        if self.current_ip != self.get_ip():
            return True
        return False

    @log
    def get_params(self, record):
        return 'login_token=%s,%s&format=json&domain_id=%s&record_id=%s&record_line_id=%s&sub_domain=www&value=%s'\
            % (self.id, self.token, self.domain_id, record["id"], record["record_line_id"], self.temp_ip)

    @log
    def ddns(self):
        ret_data = urllib2.urlopen(
            "https://dnsapi.cn/Record.List", data=self.get_params(self.records[0]))
        json_data = ret_data.readline()
        data = json.loads(json_data)
        print data
        return True

    @log
    def set_ddns(self):
        if self.ip_change():
            if self.ddns():
                self.current_ip = self.temp_ip
if __name__ == '__main__':
    dns_pod = DnsPod("26570", "28eea0a64d0c064e00e2bdea588a7a2f")
    print dns_pod.get_ip()
    while True:
        try:
            dns_pod.set_ddns()
        except Exception, e:
            print e
        time.sleep(30)
