import time
from datetime import datetime
from util import result
from util.result import message
from geventwebsocket.websocket import WebSocket

from apscheduler.schedulers.blocking import BlockingScheduler
from util.logger import log

scheduler = BlockingScheduler()

user_socket_list = []


# @scheduler.scheduled_job('cron', second='*/15', day_of_week="0-4", hour="9-11,13-15")
@scheduler.scheduled_job('cron', second='*/15')
def stock_monitoring():
    log.info('Starting stock_monitoring job %s', int(time.time()))
    for ws in user_socket_list:
        print(ws)
        if not ws.closed:
            ws.send(result.
                    socket_message(
                        2000,
                        'threshold value over times 1',
                        'Monitoring Message'
                    ))
    log.info('Finish   stock_monitoring job %s', int(time.time()))


def start():
    scheduler.start()


def shutdown():
    scheduler.shutdown()
