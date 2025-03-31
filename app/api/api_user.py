
import sys, os
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from loguru import logger
from app.api.response import response

@logger.catch()
def main(headers: map, params: map):
    
    action = params.get("action")

    if action == "login":
        return login()
    else:
        return response(code=404, msg="Not Found")

def login():
    return response()
