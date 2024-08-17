Configure logger to write logs into the ``%appdata%`` directory.

Usage:

    import logging
    import appdata_logger
    logger = logging.getLogger(__name__)

    if __name__ == '__main__':
        appdata_logger.config_with_stdout_and_file_handlers(application='myapp')
        appdata_logger.log_command_line()
        logger.info('Started')
