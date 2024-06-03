from app.core.sentry import sentry_init
from app.core.settings import conf
from app.workers.first_parser.worker import FirstParser

sentry_init(conf.sentry)


__all__ = ["FirstParser"]
