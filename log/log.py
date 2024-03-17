from loguru import logger
import sys


def log_init():
    format = (
        "[{time:YYYY-MM-DD at HH:mm:ss} {level}] {message} -{file}-({function}-{line})"
    )
    # init for stdout
    logger.add(
        sys.stdout,
        format=format,
        level="DEBUG",
    )
    # init for file
    logger.add(
        "log/file_{time:YYYYMMDD-HHmmss}.log",
        format=format,
        rotation="00:00",
        retention="7 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        level="DEBUG",
    )


def log_test():
    text = "hello world"
    logger.debug(text)
    logger.info(text)
    logger.success(text)
    logger.warning(text)
    logger.error(text)
    logger.critical(text)
    logger.trace(text)


def main():
    log_init()
    log_test()


if __name__ == "__main__":
    main()
