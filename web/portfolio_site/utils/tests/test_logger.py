"""UT Test module for the modules of logger."""
from unittest import TestCase

from utils.logger import Logger

class LoggerTest(TestCase):
    """This class is an object to test the Logger."""

    def test_write_log(self):
        log = Logger('mylog')
        log.initialize()
        log.info('teststeetetetet')
        log.err('erererererer')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
