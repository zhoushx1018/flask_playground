# flask_playground
flask playground

《flask入门教程》https://read.helloflask.com 

从零开始编码


## 安装

git clone源码
```
$ git clone https://github.com/zhoushx1018/flask_playground.git
```

## 安装依赖
```
$ pip3 install -r requirements.txt
```

## 初始化DB数据

```
$ flask forge
```

## 启动http服务

```
## Running on http://0.0.0.0:8080/
$ 
$ flask run -h 0.0.0.0  -p 8080 
```

## 在本地尝试访问服务
此时无法维护（增删改）“电影列表”，只能查看
```
$ curl http://localhost:8080/
```

## 注册（新增）管理员账号，用于维护列表
用管理员账号登录后，可以维护（增删改）“电影列表”
```
$ flask admin

```



##　通过浏览器访问服务

```
http://IP:8080/
```

＃＃　查看路由列表

```
$ flask routes
```



##  (命令行)批量单元测试

```
$ pwd
/home/ubuntu/sourceBuffer/github.com/zhoushx1018/flask_playground
$ python3 -m unittest discover
$ 
```

## 支付宝沙箱，支付测试
```

http://IP:8080/alipay/send_test_order
 
```

