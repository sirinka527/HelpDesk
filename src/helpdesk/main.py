import logging

from helpdesk.config.logger import LOG_FILEMODE, LOG_FORMAT, LOG_LEVEL, LOG_STREAM
from helpdesk.config.path import LOG_FILE

from helpdesk.cli import main

handlers = [
        logging.FileHandler(
            LOG_FILE,
            mode=LOG_FILEMODE,
            encoding="utf-8",
        )
    ]

if LOG_STREAM:
    handlers.append(logging.StreamHandler())

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=handlers,
)

if __name__ == "__main__":
    main()
