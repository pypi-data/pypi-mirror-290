"""Command-line interface to the database."""

from __future__ import annotations

import datetime
import functools
import os
import pathlib
import shutil
import sys
import typing

import click
import sqlalchemy
import sqlalchemy.orm

from golfdb import installed_editable
from golfdb.migration import Alembic

#: Context object key for the global :class:`golfdb.migration.Alembic` object.
ALEMBIC = "alembic"

#: String representing the "latest" / "head" Alembic target.
ALEMBIC_LATEST = "head"

#: Context object key for the global :class:`sqlalchemy.orm.Session` object.
DATABASE = "db"

#: Name of the environment variable that specifies the path to the database
#: file.
DATABASE_FILE_ENVVAR = "GOLFDB_FILE"


def pass_db(fn: typing.Callable) -> typing.Callable:
    """
    Pass the global :class:`sqlalchemy.orm.Session` object as an argument.

    This is a decorator::

        @pass_db
        def subcommand(db: sqlalchemy.orm.Session):
            pass  # Do stuff with db

    :param fn: :mod:`click` command / group function.
    """

    @click.pass_context
    def wrapper(
        ctx: click.Context,
        *args: typing.Sequence,
        **kwargs: typing.Mapping,
    ) -> typing.Any:  # noqa: ANN401 (decorated functions can return anything)
        return ctx.invoke(fn, ctx.obj[DATABASE], *args, **kwargs)

    return functools.update_wrapper(wrapper, fn)


@click.group()
@click.option(
    "-f",
    "--file",
    metavar="PATH",
    help=f"Path to database file (overrides envvar {DATABASE_FILE_ENVVAR}).",
)
@click.pass_context
def cli(ctx: click.Context, file: str | None) -> None:
    """Command-line interface to the database."""
    if file:
        db_path = pathlib.Path(file)
    elif DATABASE_FILE_ENVVAR in os.environ:
        db_path = pathlib.Path(os.environ[DATABASE_FILE_ENVVAR])
    else:
        msg = (
            "error: you must specify the argument -f/--file or the "
            f"environment variable {DATABASE_FILE_ENVVAR}"
        )
        print(msg, file=sys.stderr)
        sys.exit(1)

    db_path_existed = db_path.exists()

    engine = sqlalchemy.create_engine(f"sqlite+pysqlite:///{db_path}")

    ctx.ensure_object(dict)

    ctx.obj[ALEMBIC] = Alembic(engine)
    if ctx.invoked_subcommand != "db" and not ctx.obj[ALEMBIC].is_current:
        if db_path_existed:
            now = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
            backup_path_base = f"{db_path}_backup_{now}_"
            backup_path = pathlib.Path(backup_path_base + "0")
            n = 0
            while backup_path.exists():
                n += 1
                backup_path = pathlib.Path(backup_path_base + str(n))
            shutil.copy(db_path, backup_path)
        ctx.obj[ALEMBIC].upgrade(ALEMBIC_LATEST)

    ctx.obj[DATABASE] = sqlalchemy.orm.Session(engine)
    ctx.call_on_close(ctx.obj[DATABASE].close)


def main() -> None:
    """
    Entry point for the command-line interface.

    This imports modules that define the CLI and then invokes the root command
    group.
    """
    if installed_editable():
        import golfdb.cli.dev  # noqa: F401 (imported for side effects)
    cli(obj={})
