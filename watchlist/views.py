from flask import url_for
from flask import request, redirect, flash
from flask_login import login_user,login_required, logout_user, current_user
from watchlist import app, db
from watchlist.models import Movie, User, Message, AliPayTradeReturn
from flask import render_template
from watchlist.tools import GetRealIP
from flask import render_template_string


# @app.route('/')
# def hello():
#     return '<h1>hello world</h1>'

# @app.route('/watchlist')
# def index():
#     return render_template('index.html', name=name, movies=movies)

# @app.route('/watchlist-from-db')
# def index_from_db():
#     user = User.query.first()  # 读取用户记录
#     movies = Movie.query.all()  # 读取所有电影记录
#     return render_template('index.html', movies=movies)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    user = User.query.first()
    movies = Movie.query.all()
    messages = Message.query.order_by(Message.timestamp.desc()).all()

    return render_template('index.html', user=user, movies=movies, messages=messages)

@app.route('/message', methods=['POST'])
def message():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        name = request.form.get('GuestName')  # 传入表单对应输入字段的 name 值
        body = request.form.get('GuestMessage')
        # 验证数据
        if not name or not body or len(body) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页

        # 保存表单数据到数据库
        message = Message(name=name, body=body)  # 创建记录
        db.session.add(message)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/user', defaults={'name':"admin"})
@app.route('/user/<name>')
def hello_user(name):
    return 'hi, %s' % name

@app.route('/hello-template-injection')
def hello_ssti():
    person = {'name':"world", 'secret':"UGhldmJoZj8gYWl2ZnZoei5wYnovcG5lcnJlZg=="}
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    template = '''<h2>Hello %s!</h2>''' % person['name']
    return render_template_string(template, person=person)


@app.route('/test')
@login_required
def test():
    # print(url_for('hello'))
    # print(url_for('hello_user', name='steveZhou'))
    # return ( 'get url|hello=%s|hello_user=%s' %(url_for('hello'), url_for('hello_user', name='steveZhou') ))
    # return render_template('result.html')

    realIP = GetRealIP(request)
    message = 'realIP={}\n'.format(realIP)
    print(message)
    flash(message)
    app.logger.debug("11111111|message=%s" , message)
    return render_template('notify.html')



@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        app.logger.debug("start validate")
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            app.logger.info("login success|userName=%s" % user.username)
            return redirect(url_for('index'))  # 重定向到主页

        app.logger.error("Invalid username or password|userName=%s" % user.username)
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


@app.route('/logout')
@login_required  # 登录保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


# 订单支付完成，跳转到对应的页面
@app.route('/result/', methods=['GET', 'POST'])
def result():
    out_trade_no = request.args['out_trade_no']
    total_amount = request.args['total_amount']
    aliPayTradeReturn = AliPayTradeReturn(order_no=out_trade_no, pay_amount= total_amount)

    return render_template('result.html', aliPayTradeReturn=aliPayTradeReturn)

@app.route('/notify/', methods=['GET', 'POST'])
def notify():
    # 订单支付完成，跳转到对应的页面
    return render_template('notify.html')

@app.route('/alipay/send_test_order', methods=['GET','POST'])
def sendOrder():
    from .alipay import Pay
    payUrl = Pay().post(GetRealIP(request))
    re_url = payUrl['re_url']
    print("re_url=%s\n" % re_url)

    # return redirect(url_for('index'))
    return redirect(re_url)
