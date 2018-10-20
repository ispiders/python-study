import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

def allowCORS ():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST',
        'Access-Control-Expose-Headers': '',
        'Access-Control-Allow-Credentials': 'false',
        'Access-Control-Max-Age': '0'
    }

def corsOption (request):
    return web.Response(headers = allowCORS())


def index(request):
    return web.Response(headers = {'content-type': 'text/html'}, body = b'<h1>Hello World</h1>')


def login (request):

    username = request.query.get('username');
    password = request.query.get('password');

    if username == 'qjk' and password == '123456':
        return web.Response(status = 200, headers = allowCORS(), text = 'login success')
    else:
        return web.Response(status = 401, headers = allowCORS(), text = '帐号密码错误')


host = '0.0.0.0'
port = 80

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)

    app.router.add_route('GET', '/', index)

    app.router.add_route('OPTIONS', '/api/*', corsOption)
    app.router.add_route('GET', '/api/login', login)

    srv = yield from loop.create_server(app.make_handler(), host, port)
    logging.info('server started at http://' + str(host) + ':' + str(port) + '...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()