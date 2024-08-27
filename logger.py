import logging


logging.basicConfig(
    level="INFO",
    format="{asctime} {msecs} | {levelname} | {process} | {thread} | {module} | {filename}:{lineno} | {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
