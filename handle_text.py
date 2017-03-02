# -*- coding:utf-8 -*-
'''
pass
'''

import urllib
import json
import reply
import time


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
