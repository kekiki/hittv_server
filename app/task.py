# python3 -m venv path/to/venv
# source path/to/venv/bin/activate
# python3 -m pip install xyz

import sys, os

# BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, BASE)

from flask import Flask, render_template, request
from gevent import pywsgi
from loguru import logger
from api import api_video

DEBUG = not os.path.realpath(__file__).startswith('/home')
# DEBUG = False

app = Flask(__name__)
app.debug = DEBUG

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pages/<name>/terms.html')
def terms(name):
    return render_template('terms.html', name=name)

@app.route('/pages/<name>/privacy.html')
def privacy(name):
    return render_template('privacy.html', name=name)

@app.route('/api/user', methods=['POST'])
def app_api_user():
    print("\nheaders:\n", request.headers, "\nparams:\n", request.data)
    return "Hello"
    # headers = request.headers
    # params = json.loads(request.data)
    
    # print("headers", headers, "params", params)
    # return api_user.main(headers = headers, params = params)

@app.route('/api/video', methods=['GET', 'POST'])
def app_api_video():
    return api_video.main()

if __name__ == '__main__':
    if DEBUG:
        app.run(host='0.0.0.0', port=80)
    else:
        logger.add("runtime_{time}.log", rotation="500 MB")    # 文件过大于500M就会重新生成一个文件
        logger.add("runtime_{time}.log", rotation="00:00")     # 每天0点创建新文件
        logger.add("runtime_{time}.log", rotation="1 week")    # 文件每过一周就会创建新文件
        logger.add("runtime_{time}.log", retention="5 days")   # 只保留最近五天的日志文件
        # logger.add("runtime_{time}.log", compression="zip")  # 以zip格式对日志进行保存

        server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
        server.serve_forever()
        