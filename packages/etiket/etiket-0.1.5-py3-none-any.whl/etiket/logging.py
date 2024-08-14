from pythonjsonlogger import jsonlogger

from datetime import datetime, timezone
import logging

def set_up_logging():
    log_format = CustomJsonFormatter('%(timestamp)s %(levelname)s %(name)s %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(log_format)
    handler.setLevel(logging.DEBUG)
    
    loggers = [
        ("etiket", logging.DEBUG),
        ("uvicorn", logging.INFO),
        ("uvicorn.access", logging.INFO),
        ("gunicorn", logging.INFO),
        ("gunicorn.access", logging.INFO)
    ]
    
    for name, level in loggers:
        __set_up_logger(name, level, handler)

def __set_up_logger(name: str, level: int, handler: logging.Handler) -> logging.Logger:
    logger = logging.getLogger(name)
    # logger.handlers.clear()
    # logger.setLevel(level)
    # logger.addHandler(handler)
    return logger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        log_record.update(message_dict)

        if not log_record.get('timestamp'):
            now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now

        log_record['level'] = record.levelname

        if log_record.get('name') in ['uvicorn.access', 'gunicorn.access']:
            try:
                client_addr, method, full_path, http_version, status_code = record.args
                log_record['client_addr'] = client_addr
                log_record['method'] = method
                log_record['full_path'] = full_path
                log_record['http_version'] = http_version
                log_record['status_code'] = status_code
            except:
                pass