# -*- coding:utf-8 -*-
'''
pass
'''

import urllib
import json
import reply
import time
import redis
from common import get_logger
logger = get_logger()

KEY_REPLYS = {
    "知友": [
        '知友们，中秋快乐！',  # title
        '给知友的祝福。',  # desc
        'http://pic33.nipic.com/20130923/11927319_180343313383_2.jpg',  # picture
        'http://viewer.maka.im/k/J64391B8',  # url
    ],
}


def handle_get_zhiyou(rec_msg, render):
    if rec_msg.Content in KEY_REPLYS.keys():
        pic_info = KEY_REPLYS[rec_msg.Content]
        to_user = rec_msg.FromUserName
        from_user = rec_msg.ToUserName
        # pic_info 必须是二维数组
        pic_info = [pic_info]
        reply = render.reply_morepic(
            to_user, from_user, pic_info, 1)
        return reply


def handle_get_cpu(rec_msg, render):
    to_user = rec_msg.FromUserName
    from_user = rec_msg.ToUserName

    r = redis.Redis(host="localhost", port="6379", db=0)
    set_name = "CPU_TEMP"
    value = r.hget(set_name, "value")
    date = r.hget(set_name, "date")
    reply_msg = render.reply_text(to_user, from_user,
                                  int(time.time()),
                                  "时间: %s CPU温度: %s" % (date, value))
    return reply_msg

def handle_get_gpu(rec_msg, render):
    to_user = rec_msg.FromUserName
    from_user = rec_msg.ToUserName

    r = redis.Redis(host="localhost", port="6379", db=0)
    set_name = "GPU_TEMP"
    value = r.hget(set_name, "value")
    date = r.hget(set_name, "date")
    reply_msg = render.reply_text(to_user, from_user,
                                  int(time.time()),
                                  "时间: %s GPU温度: %s" % (date, value))
    return reply_msg

def auto_reply(Content):
    '''
    Handle the request with text
    '''
    content = Content  # 获得用户所输入的内容

    key = "e311457a3602414ba100184367aa767c"  # 图灵机器人的key
    url = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='\
          + content
    page = urllib.urlopen(url)
    html = page.read()
    dic_json = json.loads(html)
    reply_content = dic_json['text']
    return reply_content


if __name__ == '__main__':
    handle_text(None)
