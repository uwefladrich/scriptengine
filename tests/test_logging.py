import logging

import scriptengine.logging


def test_configure_logger(caplog):
    test_string = "Hi, this is a test string!"

    loggers = (
        "se",
        "se.foo",
        "se.bar",
        "se.foo.bar",
    )
    levels = (
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    )
    for logger in loggers:
        for level in levels:
            caplog.clear()
            scriptengine.logging.configure(level)
            logging.getLogger(logger).log(level, test_string)
            assert caplog.record_tuples == [(logger, level, test_string)]


def test_task_loader_logger(caplog):
    test_string = "Hi, this is a test string!"

    levels = (
        #   logging.DEBUG,
        #   logging.INFO,
        #   logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    )
    for level in levels:
        caplog.clear()
        scriptengine.logging.configure(level)
        logger = logging.getLogger("se.task.loader")
        logger.propagate = True
        logging.getLogger("se.task").propagate = True
        logger.log(level, test_string)
        assert caplog.record_tuples == [("se.task.loader", level, test_string)]


def test_job_logger(caplog):
    test_string = "Hi, this is a test string!"
    test_id = 123456

    levels = (
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    )
    for level in levels:
        caplog.clear()
        scriptengine.logging.configure(level)
        logger = logging.getLogger("se.job")
        logger.propagate = True
        logger.log(level, test_string, extra={"id": test_id})
        assert caplog.record_tuples == [("se.job", level, test_string)]


def test_task_logger(caplog):
    test_string = "Hi, this is a test string!"
    test_id = 123456
    test_type = "foo.bar"

    levels = (
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    )
    for level in levels:
        caplog.clear()
        scriptengine.logging.configure(level)
        logger = logging.getLogger("se.task")
        logger.propagate = True
        logger.log(level, test_string, extra={"id": test_id, "type": test_type})
        assert caplog.record_tuples == [("se.task", level, test_string)]
