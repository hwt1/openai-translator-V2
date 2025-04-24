# 日志记录器
import os.path
import sys

from loguru import logger

LOG_FILE="translation.log"
ROTATION_TIME="2:00"

# 对 loguru 的记录器进行进一步的封装
class Logger:
    def __init__(self,log_dir = "logs",debug = False):
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_file_path = os.path.join(log_dir,LOG_FILE)

        # 移除默认的 loguru handler
        logger.remove()
        level = "DEBUG" if debug else "INFO"

        # 将日志输出到控制台
        logger.add(sys.stdout,level=level)
        # 将日志输出到指定文件中
        logger.add(log_file_path,rotation=ROTATION_TIME,level="DEBUG")
        self.logger = logger

LOG = Logger(debug=True).logger


# 通过直接执行当前文件进行日志输出测试
if __name__ == "__main__":
    log = Logger().logger

    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
