# -*- coding:utf-8 -*-
'''
pass
'''

import urllib
import json
import reply


def handle_text(rec_msg):
    '''
    Handle the request with text
    '''
    content = rec_msg.Content  # 获得用户所输入的内容
    key = "e311457a3602414ba100184367aa767c"  # 图灵机器人的key
    url = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='\
          + content.encode('UTF-8')

    page = urllib.urlopen(url)
    html = page.read()
    dic_json = json.loads(html)
    reply_content = dic_json['text']
    print 'reply:', reply_content
    to_user = rec_msg.FromUserName
    from_user = rec_msg.ToUserName

    reply_msg = reply.TextMsg(to_user, from_user, reply_content)
    return reply_msg


if __name__ == '__main__':
    handle_text(None)
