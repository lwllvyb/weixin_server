# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import sys
import os
import time
import linecache
from handle_text import auto_reply, handle_get_zhiyou, handle_get_cpu, handle_get_gpu, handle_get_home_temp, handle_get_home_humidity
from handle_event import hello, bye
from handle_voice import handle_voice
from common import get_logger
logger = get_logger()

TEXT_HANDLES = {
    "CPU": handle_get_cpu,
    "GPU": handle_get_gpu,
    "室内温度": handle_get_home_temp,
    "室内湿度": handle_get_home_humidity,
    "知友": handle_get_zhiyou,
}


class Handle(object):
    '''
    Handle all the request with get/post.
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
            if hashcode == signature:
                return echostr
            else:
                logger.info(
                    "handle/GET hashcode [%s] signature [%s] " % (hashcode, signature))
                return ""
        except Exception, argument:
            logger.error("exception [%s]" % (argument))
            return argument

    def POST(self):
        try:
            web_data = web.data()
            rec_msg = receive.parse_xml(web_data)

            if not isinstance(rec_msg, receive.Msg):
                return "success"

            if rec_msg.MsgType == 'text':
                if rec_msg.Content in TEXT_HANDLES.keys():
                    handle_func = TEXT_HANDLES[rec_msg.Content]
                    reply_msg = handle_func(rec_msg, self.render)
                    return reply_msg
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
                logger.error("msgtype [%s]" % (rec_msg.MsgType))
                return "success"
        except Exception, argment:
            print_exception(logger)
            return argment


def print_exception(logger):
    '''
    Print exception.
    '''
    _, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    logger.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno,
                                                              line.strip(), exc_obj))
