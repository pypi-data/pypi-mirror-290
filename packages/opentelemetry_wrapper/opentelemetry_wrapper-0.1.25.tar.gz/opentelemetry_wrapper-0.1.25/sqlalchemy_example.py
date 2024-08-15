from sqlalchemy import create_engine
from sqlalchemy import text

from opentelemetry_wrapper import instrument_sqlalchemy_engine
from opentelemetry_wrapper.v0.dependencies.sqlalchemy.engine_typedef import is_sqlalchemy_async_engine
from opentelemetry_wrapper.v0.dependencies.sqlalchemy.engine_typedef import is_sqlalchemy_engine
from opentelemetry_wrapper.v0.dependencies.sqlalchemy.engine_typedef import is_sqlalchemy_sync_engine

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')

    print('is_sqlalchemy_engine', is_sqlalchemy_engine(engine))
    print('is_sqlalchemy_sync_engine', is_sqlalchemy_sync_engine(engine))
    print('is_sqlalchemy_async_engine', is_sqlalchemy_async_engine(engine))

    instrument_sqlalchemy_engine(engine)

    conn = engine.connect()

    # noinspection SqlDialectInspection,SqlNoDataSourceInspection
    exe = conn.execute(text('SELECT * FROM sqlite_master'))
    assert exe.fetchmany() == []
