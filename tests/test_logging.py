import logging

import scriptengine.logging


def test_configure_logger(caplog):
    test_string = 'Hi, this is a test string!'
    test_logger = (
        ('se.task', scriptengine.logging.task_log_formatter),
        ('se.cli', scriptengine.logging.cli_log_formatter),
    )
    levels = (
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    )
    for name, formatter in test_logger:
        for level in levels:
            caplog.clear()
            scriptengine.logging.configure_logger(
                name,
                level,
                formatter
            )
            logging.getLogger(name).log(level, test_string)
            assert caplog.record_tuples == [(name, level, test_string)]
