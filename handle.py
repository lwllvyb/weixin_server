# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import sys
import os
import time
import linecache
from handle_text import auto_reply
from handle_event import hello, bye
from handle_voice import handle_voice


g_KEY_REPLYS = {
    "知友": [
        '知友们，中秋快乐！',  # title
        '给知友的祝福。',  # desc
        'http://pic33.nipic.com/20130923/11927319_180343313383_2.jpg',  # picture
        'http://viewer.maka.im/k/J64391B8',  # url
    ],
}


class Handle(object):
    '''
    p
    '''

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

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

            rec_msg = receive.parse_xml(web_data)

            if not isinstance(rec_msg, receive.Msg):
                return "success"

            if rec_msg.MsgType == 'text':
                global g_KEY_REPLYS

                if rec_msg.Content in g_KEY_REPLYS.keys():
                    pic_info = g_KEY_REPLYS[rec_msg.Content]
                    to_user = rec_msg.FromUserName
                    from_user = rec_msg.ToUserName
                    # pic_info 必须是二维数组
                    pic_info = [pic_info]
                    reply = self.render.reply_morepic(
                        to_user, from_user, pic_info, 1)
                    return reply
                else:

                    reply_content = auto_reply(rec_msg.Content)
                    to_user = rec_msg.FromUserName
                    from_user = rec_msg.ToUserName

                    reply_msg = self.render.reply_text(to_user, from_user,
                                                       int(time.time()),
                                                       reply_content)

                    return reply_msg

            elif rec_msg.MsgType == 'event':
                if rec_msg.Event == "subscribe":
                    return hello(rec_msg).send()
                elif rec_msg.Event == "unsubscribe":
                    return bye(rec_msg).send()

            elif rec_msg.MsgType == 'voice':
                return handle_voice(rec_msg).send()

            else:
                print "暂且不处理"
                return "success"
        except Exception, argment:
            print_exception()
            return argment


def print_exception():
    '''
    Print exception.
    '''
    _, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno,
                                                       line.strip(), exc_obj)
