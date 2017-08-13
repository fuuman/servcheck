"""
Script to monitor a web service
"""

import socket
import schedule
import logging
from time import sleep
from configparser import ConfigParser

__author__ = "Marco Schanz"
__version__ = "0.1.0"
__license__ = "MIT"

# Configuration
config = ConfigParser()
config.read('config.ini')

# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('<p>%(asctime)s - {} - %(levelname)s - %(message)s</p>'.
                              format(config['SOCKET']['SERVICE']))
handler = logging.FileHandler(filename='timer.html')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

# 'disable' logging messages of the schedule package
logging.getLogger('schedule').setLevel(logging.CRITICAL)

ONLINE, OFFLINE = range(2)
CURRENT = None


def check():
    global CURRENT
    sock = socket.socket()
    result = sock.connect_ex((config['SOCKET']['HOST'], int(config['SOCKET']['PORT'])))

    if CURRENT is None:
        if result == 0:
            CURRENT = ONLINE
            logger.info('CURRENT STATE - ONLINE')
        else:
            CURRENT = OFFLINE
            logger.info('CURRENT STATE - OFFLINE')

    if result == 0 and CURRENT == OFFLINE:
        logger.info("NEW STATE - ONLINE")
        CURRENT = ONLINE
    if result != 0 and CURRENT == ONLINE:
        logger.info('NEW STATE - OFFLINE')
        CURRENT = OFFLINE


def main():
    logger.info("Starting..")
    check()
    schedule.every(10).seconds.do(check)
    while True:
        schedule.run_pending()
        sleep(1)
    

if __name__ == "__main__":
    main()
