
from flask import json

def response(code = 0, data = {}, msg = 'ok'):
    res = {
        'code': code,
        'data': data,
        'msg': msg
    }
    return json.jsonify(res)