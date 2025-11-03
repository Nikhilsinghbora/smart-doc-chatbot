import datetime
import json
import logging
from enum import StrEnum
from dotenv import load_dotenv
import os

load_dotenv()


log_format = os.get_env("LOG_FORMAT_DEBUG")


class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"

def configure_logging(log_level: str = LogLevels.error):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return
    
    if log_level == LogLevels.debug:
        logging.basicConfig(level=logging.DEBUG, format=log_format)
        return
    
    logging.basicConfig(level=log_level)


class JSONLogFormatter(logging.Formatter):
    def __init__(self,pretty = False):
        super().__init__()
        self.pretty = pretty

    def format(self, record):
        log_data = {
            "timestamp": datetime.now(datetime.timezone.utc),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        exclude_fields = {
            'pathname', 'filename', 'module', 'funcName', 'lineno',
            'processName', 'process', 'threadName', 'thread',
            'exc_info', 'exc_text', 'stack_info',
            'levelno', 'created', 'msecs', 'relativeCreated',
            'args', 'msg', 'name', 'levelname'
        }

        for key,value in record.__dict__.items():

            # Add all custom fields from the record
            if(
                key not in log_data and
                key not in exclude_fields and
                not key.startswith("_") and 
                not key.startswith('real_') and 
                isinstance(value, (str, int, float,bool,list,dict,type(None))) and
                value is not None
            ):
                log_data[key] = value

            if record.exc_info:
                log_data['exception'] = {
                    'type': type(record.exc_info[0]).__name__,
                    'message': str(record.exc_info[1])
                }

            if self.pretty:
                return json.dumps(log_data, indent = 4)
            else:
                return json.dumps(log_data) 
    