## 作用

这个使用于搭建微信订阅号服务器使用

## 将内网映射到外网，可以使用
### 使用方法
1. 注册用户，登陆 [natapp](https://natapp.cn)， 下载对应版本的 natapp 执行文件

2. 记录 authtoken

3. 执行以下命令
```
./natapp -authtoken=***********
```

4. 自动映射到 127.0.0.1:5000 , 5000 端口可以在网站上修改

5. http://*****.natappfree.cc -> 127.0.0.1:5000 即为外网网址，可以用于搭建微信公众号服务器

# UPDATE
2017.3.13
add common.py file. In common.py, can use get_logger() function to use logging.
Debuging will be easy!

# TODO
1.  add logging ,make it easy to debug.
2.
