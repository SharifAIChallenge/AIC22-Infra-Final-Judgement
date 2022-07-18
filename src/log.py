import logging

LOG_DIR = '/var/log/final-judgment'
loggers = ["judge", "match_queue", "events", "main", "kafka", "minio"]
MAIN_LOG_FILE = "judge.log"


class LoggerFormatter(logging.Formatter):
    name_just = 50
    level_just = 15

    def format(self, record):
        time = self.formatTime(record, self.datefmt)
        return f'===[{time}]===[{record.name}]'.ljust(self.name_just, "=") + \
            f'===[{record.levelname}]==='.ljust(self.level_just, "=") + \
            f' {record.getMessage()} :: ({record.filename}:{record.lineno})'


default_format = LoggerFormatter()


def init():

    # setting logger
    stdout_h = logging.StreamHandler()
    filelg_h = logging.FileHandler(f"{LOG_DIR}/{MAIN_LOG_FILE}")

    stdout_h.setLevel(logging.INFO)
    filelg_h.setLevel(logging.INFO)
    stdout_h.setFormatter(default_format)
    filelg_h.setFormatter(default_format)

    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(stdout_h)
        # file logger is commented due to disk consuming issues (but you can uncomment it for debbuging purpocess)
        # logger.addHandler(filelg_h)


def new_token_logger(token):

    filelg_h = logging.FileHandler(f"{LOG_DIR}/{token}.log")
    filelg_h.setLevel(logging.INFO)

    filelg_h.setFormatter(default_format)

    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.addHandler(filelg_h)


def remove_token_logger(token):
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        filelg_h = [h for h in logger.handlers if isinstance(h, logging.FileHandler) and h.baseFilename ==
                    f"{LOG_DIR}/{token}.log"]
        if filelg_h:
            logger.removeHandler(filelg_h[0])
