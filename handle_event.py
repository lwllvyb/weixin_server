# -*- coding:utf-8 -*-
'''
Handle request with event.
'''

import reply
from common import get_logger
logger = get_logger()

def hello(rec_msg):
    '''
    Handle subscribe event
    '''
    to_user = rec_msg.FromUserName
    from_user = rec_msg.ToUserName
    reply_content = "欢迎订阅欢乐平台，这是李文龙的私人订阅号。"
    reply_msg = reply.TextMsg(to_user, from_user, reply_content)
    return reply_msg

def bye(rec_msg):
    '''
    Handle subscribe event
    '''
    to_user = rec_msg.FromUserName
    from_user = rec_msg.ToUserName
    reply_content = "byebye。"
    reply_msg = reply.TextMsg(to_user, from_user, reply_content)
    return reply_msg

if __name__ == '__main__':
    hello(None)
