# Copyright 2014,2021 Adobe. All rights reserved.

"""
Auto-hinting program for PostScript, OpenType/CFF and UFO fonts.
"""

import logging
import logging.handlers
from typing import Any, Protocol, cast

log_glyph = ""
log_instance = ""
log_dimension = ""


class OtfautohintLogRecord(Protocol):
    """Protocol for log records with custom otfautohint attributes."""

    # Standard LogRecord attributes we use
    name: str
    module: str
    levelno: int
    filename: str
    lineno: int
    # Custom otfautohint attributes added by record factory
    glyph: str
    instance: str
    dimension: str

    def getMessage(self) -> str: ...


class DuplicateMessageFilter(logging.Filter):
    """
    Suppresses any log message that was reported before in the same module and
    for the same logging level. We check for module and level number in
    addition to the message just in case, though checking the message only is
    probably enough.
    """

    def __init__(self) -> None:
        super(DuplicateMessageFilter, self).__init__()
        self.logs: set[tuple[str, int, str]] = set()

    def filter(self, record: logging.LogRecord) -> bool:
        rec = cast(OtfautohintLogRecord, record)
        current = (rec.module, rec.levelno, rec.getMessage())
        if current in self.logs:
            return False
        self.logs.add(current)
        return True


class otfautoLogFormatter(logging.Formatter):
    def __init__(
        self, fmt: str | None, datefmt: str | None = None, verbose: bool = False
    ) -> None:
        super().__init__(fmt, datefmt)
        self.verbose = verbose

    def format(self, record: logging.LogRecord) -> str:
        rec = cast(OtfautohintLogRecord, record)
        if self.verbose:
            verbose_field = "[%s:%d] " % (rec.filename, rec.lineno)
        else:
            verbose_field = ""
        if rec.dimension != "":
            dim_field = rec.dimension + " "
        else:
            dim_field = ""
        if rec.instance != "" and rec.glyph != "":
            glyph_field = '(%s, "%s") ' % (rec.glyph, rec.instance)
        elif rec.glyph != "":
            glyph_field = "(%s) " % (rec.glyph)
        else:
            glyph_field = ""
        return verbose_field + glyph_field + dim_field + super().format(record)


def set_log_parameters(
    dimension: str | None = None, glyph: str | None = None, instance: str | None = None
) -> None:
    global log_glyph, log_dimension, log_instance
    if glyph is not None:
        log_glyph = glyph
    if dimension is not None:
        log_dimension = dimension
    if instance is not None:
        log_instance = instance


def logging_conf(
    verbose: int,
    logfile: str | None = None,
    handlers: list[logging.Handler] | None = None,
) -> None:
    if verbose == 0:
        log_level = logging.WARNING
    else:
        if verbose == 1:
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG

    if handlers is not None:
        logging.basicConfig(level=log_level, handlers=handlers)
    else:
        logging.basicConfig(level=log_level, filename=logfile)

    old_factory = logging.getLogRecordFactory()

    def otfautohint_record_factory(*args, **kwargs) -> logging.LogRecord:
        record = old_factory(*args, **kwargs)
        record.glyph = log_glyph
        record.instance = log_instance
        record.dimension = log_dimension
        return record

    logging.setLogRecordFactory(otfautohint_record_factory)

    fmt = otfautoLogFormatter("%(levelname)s: %(message)s", verbose=verbose > 1)

    for handler in logging.root.handlers:
        handler.setFormatter(fmt)
        if log_level == logging.WARNING:
            handler.addFilter(DuplicateMessageFilter())


def log_receiver(logQueue: Any) -> None:
    while True:
        record = logQueue.get()
        if record is None:
            break
        logger = logging.getLogger(record.name)
        logger.handle(record)


def logging_reconfig(logQueue: Any, verbose: int = 0) -> None:
    qh = logging.handlers.QueueHandler(logQueue)
    root = logging.getLogger()
    if root.handlers:
        # Already configured logging to just swap out handlers
        for h in root.handlers:
            root.removeHandler(h)
        root.addHandler(qh)
    else:
        logging_conf(verbose, None, [qh])
