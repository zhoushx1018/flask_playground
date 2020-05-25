from flask import Flask
from flask import url_for, escape
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>hello world</h1>'


@app.route('/user/<name>')
def hello_user(name):
    return 'hi, %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('hello_user', name='steveZhou'))
    return 'Test page'
