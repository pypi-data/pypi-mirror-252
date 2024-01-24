from alembic import command
from alembic.config import Config
from pathlib import Path
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from sqlmodel import SQLModel, create_engine

from . import models  # noqa
from .version import __version__  # noqa


def create_sqlite_engine(path, echo: bool = False, upgrade: bool = True):
    engine = create_engine(f"sqlite:///{Path(path).absolute()}", echo=echo)

    connection = engine.connect()

    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", str(engine.url))

    # Check if the database is new or existing:
    is_new = len(engine.dialect.get_table_names(connection)) == 0

    # If existing database, upgrade to the latest revision:
    if not is_new:
        # Check if the alembic_version table exists:
        has_alembic_table = "alembic_version" in engine.dialect.get_table_names(
            connection
        )

        # Create the alembic_version table if it doesn't exist and assume
        # the database is at the base version (3067faed075e):
        if not has_alembic_table:
            command.stamp(config, "3067faed075e")

    # Create/reflect tables:
    SQLModel.metadata.create_all(engine)

    # If new database, stamp the latest revision:
    if is_new:
        command.stamp(config, "head")

    # Run upgrade if requested:
    if upgrade:
        command.upgrade(config, "head")

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, SQLite3Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine
