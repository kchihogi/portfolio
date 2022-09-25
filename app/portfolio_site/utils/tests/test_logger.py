"""UT Test module for the modules of logger."""
import glob
import os
from logging import Formatter

from unittest import TestCase

from utils.logger import Logger

class LoggerTest(TestCase):
    """This class is an object to test the Logger."""

    def test_no_initialize(self):
        """This test to write logs without initializing, otherwise raise TypeError.
        """
        log = Logger('mylog')
        with self.assertRaises(TypeError):
            log.info('This raises the TypeError exception.')

    def test_write_log(self):
        """This tests to write logs with the Logger Module
        """
        log = Logger('mylog')
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')

        log_dir = os.getcwd() + '/log'
        log_file = log_dir + '/log.log'
        err_log_file = log_dir + '/error_log.log'
        self.assertTrue(os.path.isfile(log_file))
        self.assertTrue(os.path.isfile(err_log_file))
        with open(log_file,encoding='utf8') as file:
            total_lines = sum(1 for line in file)
        self.assertEqual(total_lines, 4)
        with open(err_log_file,encoding='utf8') as file:
            total_lines = sum(1 for line in file)
        self.assertEqual(total_lines, 2)
        log.clean()

    def test_set_dir(self):
        """This tests to write logs in a specified dirctory.
        """
        log_dir = os.getcwd() + '/foo_log'
        for file in glob.glob(log_dir + '/**', recursive=True):
            if os.path.isfile(file):
                os.remove(file)
        if os.path.exists(log_dir):
            os.removedirs(log_dir)
        log = Logger('mylog2')
        log.set_dir('foo_log')
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')
        log_file = log_dir + '/log.log'
        err_log_file = log_dir + '/error_log.log'
        self.assertTrue(os.path.isfile(log_file))
        self.assertTrue(os.path.isfile(err_log_file))
        log.clean()

    def test_set_log_file(self):
        """This tests not to write log file.
        """
        log = Logger('mylog3')
        log.set_log_file(False)
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')
        log_dir = os.getcwd() + '/log'
        log_file = log_dir + '/log.log'
        err_log_file = log_dir + '/error_log.log'
        self.assertFalse(os.path.isfile(log_file))
        self.assertTrue(os.path.isfile(err_log_file))
        log.clean()

    def test_set_err_log_file(self):
        """This tests not to write log file.
        """
        log = Logger('mylog4')
        log.set_err_log_file(False)
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')
        log_dir = os.getcwd() + '/log'
        log_file = log_dir + '/log.log'
        err_log_file = log_dir + '/error_log.log'
        self.assertTrue(os.path.isfile(log_file))
        self.assertFalse(os.path.isfile(err_log_file))
        log.clean()

    def test_set_console(self):
        """This tests not to write console.
        """
        log = Logger('mylog5')
        log.set_console(False)
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')
        log.clean()

    def test_set_format(self):
        """This tests to write logs with a changed format.
        """
        log = Logger('mylog6')
        fmt = "%(asctime)s :[%(levelname)s]%(message)s"
        log.cons_logger.set_format(Formatter(fmt))
        log.log_file_logger.set_format(Formatter(fmt))
        log.err_log_file_logger.set_format(Formatter(fmt))
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')
        log.clean()

    def test_set_log_file_cycle(self):
        """This tests to write logs after changing file rotation.
        """
        log = Logger('mylog7')
        log.log_file_logger.set_log_file_cycle(3, 5)
        log.err_log_file_logger.set_log_file_cycle(3, 5)
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')
        log.clean()

    def test_write_debug(self):
        """This tests to write debug log.
        """
        log = Logger('mylog8')
        log.cons_logger.set_log_level(10)
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')
        log.clean()

    def test_set_log_file_with_deleting_dir(self):
        """This tests to write debug log.
        """
        log = Logger('mylog9')
        log.set_dir('foo_log')
        log_dir = os.getcwd() + '/foo_log'
        for file in glob.glob(log_dir + '/**', recursive=True):
            if os.path.isfile(file):
                os.remove(file)
        if os.path.exists(log_dir):
            os.removedirs(log_dir)
        log.log_file_logger.set_log_file(
            log.log_file_logger.log_level
            ,'log.log'
            ,log.log_file_logger.out_dir
        )
        log.initialize()
        log.clean()
        log.critical('critical log test')
        log.err('error log test')
        log.warn('warn log test')
        log.info('info log test ')
        log.debug('debug log test')
        log.clean()
