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


from monitor import trigger
import json
from util import result
from util.utils import AutoJSONEncoder
from app import app
from models import StockMonitor
from config import status
from database import db
import threading
from scheduler import scheduler
from config import APP_SETTINGS
from api.price_provider import get_info_from_sina
from flask import (Flask, Response, escape, jsonify,
                   redirect, request, session, url_for)
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from util.logger import log
from flask_sqlalchemy import sqlalchemy

user_socket_list = []

db.create_all()


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


@app.route('/user/check')
def check():
    trigger.check()
    return result.success()


@app.route('/user/list')
def user():
    mons = StockMonitor.query.all()
    log.info(json.dumps(mons, cls=AutoJSONEncoder, indent=2))
    return json.dumps(mons, cls=AutoJSONEncoder, indent=2)


@app.route('/user/add', methods=["POST"])
def add():
    body = request.get_json()
    print(body)
    mon = StockMonitor.of(body)
    db.session.add(mon)
    db.session.commit()
    return json.dumps(mon, cls=AutoJSONEncoder, indent=2)


def bootstrap():
    ENV = APP_SETTINGS.prop('application.env')
    if ENV == 'DEV':
        log.info(u'Started Starting as DEV')
        # app.run(threaded=True, use_reloader=False)
        app.run(threaded=True)
    else:
        log.info(u'Started Starting as PRO')
        server = WSGIServer(('0.0.0.0', 5000),
                            app,
                            handler_class=WebSocketHandler,
                            log=log)
        server.serve_forever()


def start_scheduler_thread():
    status['val'] = status['val']+1
    print(status['val'])
    scheduler_thread = threading.Thread(target=scheduler.start, args=())
    scheduler_thread.setDaemon(True)
    scheduler_thread.start()


@app.errorhandler(sqlalchemy.exc.IntegrityError)
def handle_invalid_usage(error):
    return result.error(error.code)


@app.teardown_appcontext
def shutdown_scheduler(a):
    pass


if __name__ == "__main__":
    # start_scheduler_thread()
    bootstrap()
    # scheduler.shutdown()
