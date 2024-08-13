#!/usr/bin/env python3
"""Structured logging demo with file config."""

import logging
import logging.config

import logstruct

logging.config.fileConfig("example_config.ini", disable_existing_loggers=False)

log = logstruct.getLogger(__name__)

log.info("An info message")
log.info("An info message with stack info", stack_info=True)
log.info("An info message with data (traditional)", extra={"struct": "log", "unrepresentable": logging})
log.info("An info message with data (kwargs)", struct="log", unrepresentable=logging)

try:
    print(1 / 0)
except Exception:
    log.exception("Division error")
