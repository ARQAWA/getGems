from app.core.sentry import sentry_init
from app.core.settings import conf
from app.workers.first_parser.container import get_first_parser
from app.workers.runner import WorkerRunner

sentry_init(conf.sentry)


__all__ = (
    "WorkerRunner",
    "get_first_parser",
)
