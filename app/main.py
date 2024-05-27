from app.core.sentry import sentry_init
from app.core.settings import conf
from app.modules.workers import run_worker
from app.modules.workers.first_parser.container import get_first_parser

sentry_init(conf.sentry)


__all__ = (
    "get_first_parser",
    "run_worker",
)
