# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle

urls = (
    '/weixin', 'Handle',
    '/', 'Hello',
)
class Hello(object):
    def GET(self):
        return "hello world"

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
