import config
import hashlib
import logging

logging.basicConfig(
    level=config.LOGGING_LEVEL,
    format=config.LOGGING_FORMAT,
    datefmt=config.LOGGING_DATE_FORMAT
)
logger = logging.getLogger('leaderboard')


def hash_password(password: str) -> str:
    salted = password + config.PASSWORD_SALT
    return hashlib.sha512(salted.encode("utf8")).hexdigest()
