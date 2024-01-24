from pathlib import Path

from alembic.config import Config
from alembic import command


ROOT_PATH = Path(__file__).parent.parent


def _create_alembic_config(sqlite_path):
    config = Config(ROOT_PATH / "alembic.ini")
    config.set_main_option("script_location", str(ROOT_PATH / "migrations"))
    config.set_main_option("sqlalchemy.url", f"sqlite:///{sqlite_path}")
    return config


def stamp(sqlite_path, revision="head"):
    alembic_config = _create_alembic_config(sqlite_path)
    command.stamp(alembic_config, revision)


def current(sqlite_path, verbose=False):
    alembic_config = _create_alembic_config(sqlite_path)
    command.current(alembic_config, verbose=verbose)


def upgrade(sqlite_path, revision="head"):
    alembic_config = _create_alembic_config(sqlite_path)
    command.upgrade(alembic_config, revision)


def downgrade(sqlite_path, revision):
    alembic_config = _create_alembic_config(sqlite_path)
    command.downgrade(alembic_config, revision)
