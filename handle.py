# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import sys
import linecache
from handle_text import handle_text
from handle_event import hello, bye

class Handle(object):
    '''
    p
    '''

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "weixinliwenlong"  # 请按照公众平台官网\基本配置中信息填写

            import_info = [token, timestamp, nonce]
            import_info.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, import_info)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, argument:
            return argument

    def POST(self):
        try:
            web_data = web.data()
            print "Handle Post webdata: ", web_data  # 后台打日志

            rec_msg = receive.parse_xml(web_data)

            if isinstance(rec_msg, receive.Msg)\
                    and rec_msg.MsgType == 'text':
                return handle_text(rec_msg).send()

            elif isinstance(rec_msg, receive.Msg)\
                    and rec_msg.MsgType == 'event':

                if rec_msg.Event == "subscribe":
                    return hello(rec_msg).send()
                elif rec_msg.Event == "unsubscribe":
                    return bye(rec_msg).send()

            else:
                print "暂且不处理"
                return "success"
        except Exception, argment:
            PrintException()
            return argment

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
