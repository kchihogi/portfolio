import logging
from logging import Formatter
from logging import getLogger
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import sys
import os

LOG_LEVEL = logging.INFO

CONSOLE_FORMAT = Formatter("%(asctime)s %(module)10s(%(process)6d/%(thread)8d):[%(levelname)s]%(message)s")
CONSOLE_LEVEL = logging.ERROR

LOG_DIR = "./log"

NORMAL_FILE_PATH = os.path.join(LOG_DIR, "log.log")
NORMAL_MAX_SIZE = 1048576
NORMAL_BACKUP_COUNT = 3
NORMAL_LEVEL = logging.INFO

ERR_FILE_PATH = os.path.join(LOG_DIR, "error_log.log")
ERR_MAX_SIZE = 1048576
ERR_BACKUP_COUNT = 3
ERR_LEVEL = logging.ERROR

FILE_FORMAT = Formatter("%(asctime)s %(module)10s(%(process)6d/%(thread)8d):[%(levelname)s]%(message)s(%(filename)s,%(lineno)d,%(funcName)s)")

class Logger:
    def __init__(self,name):
        # フォルダ作成
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
        # StreamHandler
        streamHandler = StreamHandler(sys.stdout)
        streamHandler.setFormatter(CONSOLE_FORMAT)
        streamHandler.setLevel(CONSOLE_LEVEL)
        # NormalFileHandler
        normalFileHandler = RotatingFileHandler(NORMAL_FILE_PATH, maxBytes=NORMAL_MAX_SIZE, backupCount=NORMAL_BACKUP_COUNT)
        normalFileHandler.setLevel(NORMAL_LEVEL)
        normalFileHandler.setFormatter(FILE_FORMAT)
        # ErrorFileHandler
        errorFileHandler = RotatingFileHandler(ERR_FILE_PATH, maxBytes=ERR_MAX_SIZE, backupCount=ERR_BACKUP_COUNT)
        errorFileHandler.setLevel(ERR_LEVEL)
        errorFileHandler.setFormatter(FILE_FORMAT)
        #loggerを設定
        self.name =  name
        self.logger = getLogger(self.name)
        self.logger.setLevel(LOG_LEVEL)
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(normalFileHandler)
        self.logger.addHandler(errorFileHandler)
