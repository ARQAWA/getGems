from app.core.sentry import sentry_init
from app.core.settings import conf
from app.workers.first_parser.parser import FirstParser
from app.workers.runner import WorkerRunner

sentry_init(conf.sentry)

__all__ = (
    "FirstParser",
    "WorkerRunner",
)
