from app.core.sentry import sentry_init
from app.core.settings import conf
from app.workers.stats_fetcher.main import StatsFetcherMain

sentry_init(conf.sentry)


__all__ = ["StatsFetcherMain"]
