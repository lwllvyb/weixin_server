#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, g, request, make_response, render_template,\
                url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/weixin')
def wechat_auth():
    if request.method == 'GET':
        if len(request.args) > 3:
            token = 'weixinliwenlong'
            query = request.args
            signature = query['signature']
            timestamp = query['timestamp']
            nonce = query['nonce']
            echostr = query['echostr']
            s = [timestamp, nonce, token]
            s.sort()
            s = ''.join(s)
            sha1str = hashlib.sha1(s).hexdigest()
            if sha1str == signature:
                return make_response(echostr)
            else:
                return make_response("认证失败")
        else:
            return "认证失败"

if __name__ == '__main__':
    app.debug = True
    app.run()
