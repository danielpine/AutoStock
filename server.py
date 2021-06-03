# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Pine
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from api.price_provider import get_info_from_sina
from flask import (Flask, Response, escape, jsonify, redirect, request,
                   session, url_for)
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer

from util.logger import log

app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True
user_socket_list = []


@app.route('/orange')
def orange():
    user_socket = request.environ.get('wsgi.websocket')
    log.info('request %s', request)
    log.info('user_socket %s', user_socket)
    if user_socket:
        user_socket_list.append(user_socket)
        log.info('user_socket_list depth %s', len(user_socket_list))
    while True:
        try:
            msg = user_socket.receive()
            log.info('received: %s', msg)
            for sock in user_socket_list:
                try:
                    sock.send('received: %s' + msg)
                except:
                    continue
        except Exception as e:
            log.error(e)
            if user_socket and user_socket in user_socket_list:
                user_socket_list.remove(user_socket)
            return ''


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/query_price/<ids>')
def query_price(ids):
    return get_info_from_sina(ids)

from config import APP_SETTINGS

ENV = APP_SETTINGS.prop('application.env')
 
if __name__ == "__main__":
    if ENV == 'DEV' :
        log.info(u'Started Starting as DEV')
        app.run(threaded=True)
    else:    
        log.info(u'Started Starting as PRO')
        srv = WSGIServer(('0.0.0.0', 5000),
                        app,
                        handler_class=WebSocketHandler,
                        log=log)
        srv.serve_forever()
