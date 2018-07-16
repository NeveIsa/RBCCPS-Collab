import coloredlogs
#coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s'
coloredlogs.DEFAULT_LOG_FORMAT = '%(levelname)s %(message)s'
coloredlogs.install(level="INFO")
#coloredlogs.install(level="WARNING")


if __name__=="__main__":
    import logging
    logging.info("OK")
    logging.debug("OK")
    logging.warning("OK")
    logging.error("OK")
    logging.critical("OK")
