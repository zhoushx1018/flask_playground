from flask import Flask,render_template
from flask import url_for, escape
app = Flask(__name__)

name = 'Steve Zhou'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


@app.route('/')
def hello():
    return '<h1>hello world</h1>'

@app.route('/watchlist')
def index():
    return render_template('index.html', name=name, movies=movies)


@app.route('/user/<name>')
def hello_user(name):
    return 'hi, %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('hello_user', name='steveZhou'))
    return ( 'get url|hello=%s|hello_user=%s' %(url_for('hello'), url_for('hello_user', name='steveZhou') ))
