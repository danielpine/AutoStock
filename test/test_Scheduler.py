from scheduler import scheduler
from unittest import TestCase
from util.logger import log


class TestScheduler(TestCase):
    def test_start(self):
        log.info("Satrt...")
        # scheduler.start()
        log.info("End...")
