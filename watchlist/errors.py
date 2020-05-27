from flask import render_template
from watchlist import app
from watchlist.models import User

@app.errorhandler(400)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('errors/400.html'), 400  # 返回模板和状态码


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    # return render_template('404.html', user=user), 404  # 返回模板和状态码
    return render_template('errors/404.html'), 404  # 返回模板和状态码

@app.errorhandler(405)
def page_not_allowed(e):  # 接受异常对象作为参数
    user = User.query.first()
    # return render_template('404.html', user=user), 404  # 返回模板和状态码
    return render_template('errors/405.html'), 405  # 返回模板和状态码
