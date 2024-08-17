Configure logger to write logs into the ``%appdata%`` directory.

Usage:

    import logging
    import appdata_logging
    logger = logging.getLogger(__name__)

    if __name__ == '__main__':
        appdata_logging.config_with_stdout_and_file_handlers(application='myapp')
        appdata_logging.log_command_line()
        logger.info('Started')
