import logging
from pathlib import Path

from morebuiltins.functools import SizedTimedRotatingFileHandler


class Config:
    LOG_STREAM = True
    LOG_DIR = None
    LOG_LEVEL = logging.DEBUG

    @classmethod
    def init_logger(cls):
        logger = logging.getLogger("taska")
        if not logger.hasHandlers():
            logger.setLevel(cls.LOG_LEVEL)
            fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            if cls.LOG_STREAM:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(cls.LOG_LEVEL)
                stream_handler.setFormatter(fmt)
                logger.addHandler(stream_handler)
            if cls.LOG_DIR:
                path = Path(cls.LOG_DIR).joinpath("app.log").resolve()
                path.parent.mkdir(parents=True, exist_ok=True)
                file_handler = SizedTimedRotatingFileHandler(
                    path.as_posix(),
                    when="midnight",
                    interval=1,
                    backupCount=7,
                    maxBytes=50 * 1024 * 1024,
                )
                file_handler.setLevel(cls.LOG_LEVEL)
                file_handler.setFormatter(fmt)
                logger.addHandler(file_handler)
        return logger
