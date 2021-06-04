import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from util.logger import log

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', second='*/15', day_of_week="0-4", hour="9-11,13-15")
def stock_monitoring():
    log.info('Starting job %s', int(time.time()))
    log.info('Finish   job %s', int(time.time()))


def start():
    scheduler.start()


def shutdown():
    scheduler.shutdown()
