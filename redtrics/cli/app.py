# -*- coding: utf-8 -*-

import argparse
import os
import schedule
import logging
import logging.config
import sys
import time
from redtrics.core.runner import Runner

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '..', 'etc', 'logging.ini'))
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(prog='redtrics-generate', description='RedMart Github Metrics')
    parser.add_argument('--base', help='base/branch to run the metrics on', default='master')
    parser.add_argument('--run-now', help='run only one time. Otherwise will run as scheduler', action="store_true")

    args = parser.parse_args()

    try:
        runner = Runner(args.base)
        if args.run_now:
            runner.run()
        else:
            schedule.every().monday.at("00:30").do(runner.run)
            while True:
                schedule.run_pending()
                time.sleep(1)
    except Exception as e:
        logger.error(e)
        sys.exit(1)
