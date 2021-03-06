# -*- coding:utf-8 -*-
'''
Handle request with voice.
'''

import reply
from common import get_logger
logger = get_logger()

def handle_voice(rec_msg):
    to_user = rec_msg.FromUserName
    from_user = rec_msg.ToUserName
    reply_recognition = rec_msg.Recognition
    reply_msg = reply.TextMsg(to_user, from_user, reply_recognition)
    return reply_msg

if __name__ == '__main__':
    handle_voice(None)