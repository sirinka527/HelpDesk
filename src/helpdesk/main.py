import logging

from helpdesk.config.logger import LOG_FILEMODE, LOG_FORMAT, LOG_LEVEL
from helpdesk.config.path import LOG_FILE

from helpdesk.cli import main


logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    filemode=LOG_FILEMODE,
    filename=LOG_FILE
)

if __name__ == "__main__":
    main()
