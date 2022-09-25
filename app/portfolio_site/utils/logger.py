"""Wrapper of logging.
"""
import glob
import inspect
import logging
from logging import Formatter
from logging import getLogger
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import sys
import os

from utils.cprint import ColorPrint as CP

BASE_FORMAT = "%(asctime)s (%(process)6d/%(thread)8d):[%(levelname)s]%(message)s"
FILE_FORMAT = BASE_FORMAT

class ConsoleLogger:
    """Console Logger module to put out stdout.
    """
    def __init__(self):

        # Format
        self.format = Formatter(BASE_FORMAT)

        #Console
        self.log_level = logging.ERROR

    def set_log_level(self, level:int):
        """Set Log level.

        Args:
            level (int): Log Level.
            CRITICAL = 50
            FATAL = CRITICAL
            ERROR = 40
            WARNING = 30
            WARN = WARNING
            INFO = 20
            DEBUG = 10
            NOTSET = 0
        """
        self.log_level = level

    def set_format(self, formatter:Formatter):
        """Set format.

        %(name)s            Name of the logger (logging channel)
        %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                            WARNING, ERROR, CRITICAL)
        %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                            "WARNING", "ERROR", "CRITICAL")
        %(pathname)s        Full pathname of the source file where the logging
                            call was issued (if available)
        %(filename)s        Filename portion of pathname
        %(module)s          Module (name portion of filename)
        %(lineno)d          Source line number where the logging call was issued
                            (if available)
        %(funcName)s        Function name
        %(created)f         Time when the LogRecord was created (time.time()
                            return value)
        %(asctime)s         Textual time when the LogRecord was created
        %(msecs)d           Millisecond portion of the creation time
        %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                            relative to the time the logging module was loaded
                            (typically at application startup time)
        %(thread)d          Thread ID (if available)
        %(threadName)s      Thread name (if available)
        %(process)d         Process ID (if available)
        %(message)s         The result of record.getMessage(), computed just as
                            the record is emitted

        Args:
            console_format (Formatter): Format
        """
        self.format = formatter

class FileLogger(ConsoleLogger):
    """File Logger module to write out log file.
    """
    def __init__(self):
        super().__init__()

        self.out_dir = './log'

        # Format
        self.format = Formatter(FILE_FORMAT)

        # Log File
        self.log_level = logging.INFO
        self.file_path = os.path.join(self.out_dir, "log.log")
        self.max_size = 1048576
        self.backup = 3

    def set_dir(self, out_dir:str, clean:bool = False):
        """Set a directory to put out log files.

        The directory is created when it does not exist.

        Args:
            out_dir (str): Directory path to put out log files.
            clean (bool, optional): Cleanning Flag.
            If clean is set to True, all files are deleted under the out_dir.
            Defaults to False.
        """
        self.out_dir = out_dir

        if clean:
            for file in glob.glob(self.out_dir + '/**', recursive=True):
                if os.path.isfile(file):
                    os.remove(file)

        # フォルダ作成
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

        self.file_path = os.path.join(self.out_dir, os.path.basename(self.file_path))

    def set_log_file(self, level:int, name:str, out_dir:str):
        """Set log file configuration.

        Args:
            level (int): Log Level.
            CRITICAL = 50
            FATAL = CRITICAL
            ERROR = 40
            WARNING = 30
            WARN = WARNING
            INFO = 20
            DEBUG = 10
            NOTSET = 0
            name (str): File name with an extention.
            out_dir (str): Directory. It will be created.
        """
        self.log_level = level

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        self.file_path = os.path.join(out_dir, name)

    def set_log_file_cycle(self, size:int, backup:int):
        """Set log file rotation configuration.

        Args:
            size (int): Max size of a file.
            backup (int): Backup counts of files.
        """
        self.max_size = size
        self.backup = backup

class Logger:
    """Logger module to write out console, log file , and error log file at the same time.

    Wrapper of logging class, which is the standard library.
    """
    def __init__(self, name:str):
        self.cons_logger = ConsoleLogger()
        self.log_file_logger = FileLogger()
        self.err_log_file_logger = FileLogger()
        self.err_log_file_logger.set_log_file(
            logging.ERROR
            , 'error_log.log'
            , self.err_log_file_logger.out_dir
            )

        self.__init = False
        self.__logger = getLogger(name)
        self.__c_logger = getLogger('c_'+name)

    def initialize(self, root_log_level:int=logging.INFO):
        """Initialize Logger. Initialize must be called to use Logger.

        Args:
            root_log_level (int, optional): Top log level. Defaults to logging.INFO.
        """
        if self.log_file_logger is not None:
            self.set_dir(self.log_file_logger.out_dir)
        elif self.err_log_file_logger is not None:
            self.set_dir(self.err_log_file_logger.out_dir)

        #loggerを設定
        self.__logger.setLevel(root_log_level)
        self.__c_logger.setLevel(root_log_level)
        # StreamHandler
        if self.cons_logger is not None:
            sth = StreamHandler(stream=sys.stdout)
            sth.setFormatter(self.cons_logger.format)
            sth.setLevel(self.cons_logger.log_level)
            self.__c_logger.addHandler(sth)
        # NormalFileHandler
        if self.log_file_logger is not None:
            nfh = RotatingFileHandler(
                self.log_file_logger.file_path
                , maxBytes=self.log_file_logger.max_size
                , backupCount=self.log_file_logger.backup
                )
            nfh.setLevel(self.log_file_logger.log_level)
            nfh.setFormatter(self.log_file_logger.format)
            self.__logger.addHandler(nfh)
        # ErrorFileHandler
        if self.err_log_file_logger is not None:
            efh = RotatingFileHandler(
                self.err_log_file_logger.file_path
                , maxBytes=self.err_log_file_logger.max_size
                , backupCount=self.err_log_file_logger.backup
                )
            efh.setLevel(self.err_log_file_logger.log_level)
            efh.setFormatter(self.err_log_file_logger.format)
            self.__logger.addHandler(efh)
        self.__init = True

    def set_dir(self, out_dir:str, clean:bool = False):
        """Set a directory to put out log files.

        The directory is created when it does not exist.

        Args:
            out_dir (str): Directory path to put out log files.
            clean (bool, optional): Cleanning Flag.
            If clean is set to True, all files are deleted under the out_dir.
            Defaults to False.
        """
        if self.log_file_logger is not None:
            self.log_file_logger.set_dir(out_dir,clean)
        if self.err_log_file_logger is not None:
            self.err_log_file_logger.set_dir(out_dir,clean)

    def set_log_file(self, enable:bool):
        """Set log file configuration.

        Args:
            enable (bool): Enable. If set False, no log file to wrtie out.
        """
        if not enable:
            self.log_file_logger = None

    def set_err_log_file(self, enable:bool):
        """Set error log file configuration.

        Args:
            enable (bool): Enable. If set False, no error log file to wrtie out.
        """
        if not enable:
            self.err_log_file_logger = None

    def set_console(self, enable:bool):
        """Set Console Log.

        Args:
            enable (bool): Enable. If set False, no console log to put out.
        """
        if not enable:
            self.cons_logger = None

    def critical(self, msg:str):
        """Write log with critical level.

        Args:
            msg (str): Message.

        Raises:
            TypeError: It raises TypeError when initialize is not called.
        """
        self._is_init()
        msg += f'({inspect.currentframe().f_back.f_code.co_filename}'
        msg += f', {inspect.currentframe().f_back.f_lineno}'
        msg += f', {inspect.currentframe().f_back.f_code.co_name})'
        self.__logger.critical(msg)
        self.__c_logger.critical(CP.raw(msg, CP.RED))

    def err(self, msg):
        """Write log with error level.

        Args:
            msg (str): Message.

        Raises:
            TypeError: It raises TypeError when initialize is not called.
        """
        self._is_init()
        msg += f'({inspect.currentframe().f_back.f_code.co_filename}'
        msg += f', {inspect.currentframe().f_back.f_lineno}'
        msg += f', {inspect.currentframe().f_back.f_code.co_name})'
        self.__logger.error(msg)
        self.__c_logger.error(CP.raw(msg, CP.RED))

    def warn(self, msg):
        """Write log with warn level.

        Args:
            msg (str): Message.

        Raises:
            TypeError: It raises TypeError when initialize is not called.
        """
        self._is_init()
        msg += f'({inspect.currentframe().f_back.f_code.co_filename}'
        msg += f', {inspect.currentframe().f_back.f_lineno}'
        msg += f', {inspect.currentframe().f_back.f_code.co_name})'
        self.__logger.warning(msg)
        self.__c_logger.warning(CP.raw(msg, CP.YELLOW))

    def info(self, msg):
        """Write log with info level.

        Args:
            msg (str): Message.

        Raises:
            TypeError: It raises TypeError when initialize is not called.
        """
        self._is_init()
        msg += f'({inspect.currentframe().f_back.f_code.co_filename}'
        msg += f', {inspect.currentframe().f_back.f_lineno}'
        msg += f', {inspect.currentframe().f_back.f_code.co_name})'
        self.__logger.info(msg)
        self.__c_logger.info(CP.raw(msg, CP.GREEN))

    def debug(self, msg):
        """Write log with debug level.

        Args:
            msg (str): Message.

        Raises:
            TypeError: It raises TypeError when initialize is not called.
        """
        self._is_init()
        msg += f'({inspect.currentframe().f_back.f_code.co_filename}'
        msg += f', {inspect.currentframe().f_back.f_lineno}'
        msg += f', {inspect.currentframe().f_back.f_code.co_name})'
        self.__logger.debug(msg)
        self.__c_logger.debug(CP.raw(msg, CP.GREEN))

    def clean(self):
        """Cleaning all log files
        """
        if self.log_file_logger is not None:
            self.log_file_logger.set_dir(self.log_file_logger.out_dir, True)
        if self.err_log_file_logger is not None:
            self.err_log_file_logger.set_dir(self.err_log_file_logger.out_dir, True)
        self.initialize()

    def _is_init(self):
        """Check initialize flag.

        Raises:
            TypeError: If init is false, It raises TypeError.
        """
        if not self.__init:
            raise TypeError('Logger module must be initialize first. Please call initialize.')
