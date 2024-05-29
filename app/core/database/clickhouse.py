# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
#
# from app.core.settings import conf
#
# engine = create_engine(
#     url=conf.clickhouse.dsn,
#     pool_size=8,
#     max_overflow=8,
#     pool_pre_ping=True,
#     pool_recycle=1200,
#     echo=True,
# )
# Base = declarative_base()
