import logging
from logging.handlers import RotatingFileHandler

def setup_logger(module_name, log_dir="logs"):
    """
    根据模块名称配置日志记录器，并自动生成日志文件名。

    :param module_name: 模块名称，用于生成日志文件名
    :param log_dir: 日志文件存储目录，默认为 "logs"
    :return: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # 设置全局日志级别为 DEBUG

    # 配置日志格式化
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s-%(module)s:%(lineno)d - %(message)s")

    # 配置控制台处理器（输出到终端）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 控制台日志级别为 INFO
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 配置文件处理器（根据模块名称生成日志文件名）
    log_file = f"{log_dir}/{module_name}.log"
    file_handler = RotatingFileHandler(
        log_file,  # 日志文件路径
        maxBytes=1024 * 1024,  # 每个日志文件的最大大小（1MB）
        backupCount=5  # 保留的旧日志文件数量
    )
    file_handler.setLevel(logging.DEBUG)  # 文件日志级别为 DEBUG
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

log = setup_logger("my_app_log")

if __name__ == "__main__":
    # 测试日志记录器

    log.debug("这是一个调试信息。")
    log.info("这是一个普通信息。")
    log.warning("这是一个警告信息。")
    log.error("这是一个错误信息。")
    log.critical("这是一个严重错误信息。")