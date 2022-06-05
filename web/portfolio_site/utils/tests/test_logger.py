"""UT Test module for the modules of logger."""
from unittest import TestCase

from utils.logger import Logger

class LoggerTest(TestCase):
    """This class is an object to test the Logger."""

    def test_write_log(self):
        """This tests to write logs with the Logger Module
        """
        log = Logger('mylog')
        log.initialize()
        log.info('teststeetetetet')
        log.err('erererererer')
        self.assertEqual(1,1)
