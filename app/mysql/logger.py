import time, datetime
import os, sys
import loguru

class Logger:

    def __init__(self, dir_name: str):
        self.logger = loguru.logger

        log_dir = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'logs')
        log_dir = os.path.join(log_dir, dir_name)
        os.makedirs(log_dir, exist_ok=True)

        log_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S_%f")
        log_path = os.path.join(log_dir, f'{log_time}.log')
        self.logger.add(log_path, encoding='utf-8', rotation="00:00", retention='3 days')

mysql_logger = Logger('mysql').logger

if __name__ == '__main__':
    mysql_logger.info('info')
    mysql_logger.error('error')