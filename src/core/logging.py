import logging
from logging import basicConfig, getLogger  # noqa
import sys
from pathlib import Path
from loguru import logger
from django.conf import settings


class InterceptHandler(logging.Handler):
    """
    Redirect standard logging → loguru
    """
    def emit(self, record) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller where the logged message originated
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_logging():
    # Remove default handler (the one with id=0)
    logger.remove()

    # ── Common format ────────────────────────────────────────────────────────
    log_format = (
        "<level>{level: <8}</level>"
        "<green>[{time:YYYY-MM-DD HH:mm:ss.SSS}]</green> "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level> "
        "{extra}"
    )

    # ── Development ──────────────────────────────────────────────────────────
    if settings.DEBUG:
        log_format = (
            "<level>{level: <8}</level>"
            "<green>[{time:YYYY-MM-DD HH:mm:ss.SSS}]</green> "
            # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level> "
        )
        logger.add(
            sys.stderr,
            format=log_format,
            level="DEBUG",
            colorize=True,
            enqueue=True,           # thread-safe
        )
        return

    # ── Production ───────────────────────────────────────────────────────────
    # File + rotation + retention + compression
    log_dir = Path(settings.BASE_DIR) / "logs"
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        format=log_format,
        rotation="00:00",           # new file every day at midnight
        retention="14 days",        # keep 2 weeks
        compression="zip",          # compress old files
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=False,             # set True only when really needed
    )

    # Optional: separate ERROR+ logs
    logger.add(
        log_dir / "errors_{time:YYYY-MM-DD}.log",
        format=log_format,
        level="ERROR",
        rotation="00:00",
        retention="90 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    # Console in production (usually for docker/kubernetes logs)
    logger.add(
        sys.stderr,
        format=log_format,
        level="INFO",
        colorize=False,             # most platforms don't like ANSI
        enqueue=True,
    )


# Call once at startup (see below)
configure_logging()
