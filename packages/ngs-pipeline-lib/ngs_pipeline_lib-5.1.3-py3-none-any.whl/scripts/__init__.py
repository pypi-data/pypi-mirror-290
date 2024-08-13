import logging
import logging.config
import logging.handlers
from pathlib import Path

import colorama
import structlog


def configure_logging(
    verbose: bool = False, json: bool = False, log_file_path: Path = None
):
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    columns = [
        # Render the timestamp without the key name in yellow.
        structlog.dev.Column(
            "timestamp",
            structlog.dev.KeyValueColumnFormatter(
                key_style=None,
                value_style=colorama.Fore.YELLOW,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
        structlog.dev.Column(
            "level",
            structlog.dev.LogLevelColumnFormatter(
                level_styles={
                    "critical": colorama.Fore.RED + colorama.Back.WHITE,
                    "exception": colorama.Fore.RED,
                    "error": colorama.Fore.RED,
                    "warn": colorama.Fore.YELLOW,
                    "warning": colorama.Fore.YELLOW,
                    "info": colorama.Fore.GREEN,
                    "debug": colorama.Fore.CYAN,
                    "notset": colorama.Fore.LIGHTBLACK_EX,
                },
                reset_style="\x1b[0m",
            ),
        ),
        # Render the event without the key name in bright magenta.
        structlog.dev.Column(
            "logger",
            structlog.dev.KeyValueColumnFormatter(
                key_style=None,
                value_style=colorama.Style.BRIGHT + colorama.Fore.MAGENTA,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
        # Render the event without the key name in bright magenta.
        structlog.dev.Column(
            "event",
            structlog.dev.KeyValueColumnFormatter(
                key_style=None,
                value_style=colorama.Style.BRIGHT + colorama.Fore.WHITE,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
        # Default formatter for all keys not explicitly mentioned. The key is
        # cyan, the value is green.
        structlog.dev.Column(
            "",
            structlog.dev.KeyValueColumnFormatter(
                key_style=colorama.Fore.CYAN,
                value_style=colorama.Fore.GREEN,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
    ]
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", key="timestamp", utc=False),
    ]

    if json:
        processors.append(structlog.processors.dict_tracebacks)
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.processors.StackInfoRenderer())
        processors.append(structlog.dev.set_exc_info)
        processors.append(structlog.dev.ConsoleRenderer(columns=columns))

    structlog.reset_defaults()

    handlers = {
        "default": {
            "level": log_level,
            "class": "logging.StreamHandler",
        }
    }
    if log_file_path:
        handlers["file"] = {
            "level": log_level,
            "class": "logging.handlers.WatchedFileHandler",
            "filename": str(log_file_path),
        }

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": handlers,
            "loggers": {
                "": {
                    "handlers": list(handlers.keys()),
                    "level": log_level,
                    "propagate": True,
                },
            },
        }
    )

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
    )
