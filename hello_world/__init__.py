from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>hello world</h1>'


@app.route('/user/<name>')
def hello_user(name):
    return 'hi, %s' % name

