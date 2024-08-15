"""Commands for use in the development environment."""

import sys

import click
import IPython
import sqlalchemy

from golfdb.cli import ALEMBIC, ALEMBIC_LATEST, cli, pass_db


@cli.command()
@pass_db
@click.pass_context
def repl(
    ctx: click.Context,  # noqa: ARG001 (want ctx in scope in REPL)
    db: sqlalchemy.orm.Session,  # noqa: ARG001 (want db in scope in REPL)
) -> None:
    """Start an IPython REPL with  ``ctx`` and ``db`` in scope."""
    IPython.embed()


@cli.group()
def db() -> None:
    """Perform "low-level" database operations."""


@db.command(name="upgrade")
@click.argument("target", default=ALEMBIC_LATEST)
@click.pass_context
def db_upgrade(ctx: click.Context, target: str) -> None:
    """Upgrade the database to ``target`` (default latest)."""
    ctx.obj[ALEMBIC].upgrade(target)


@db.command(name="downgrade")
@click.argument("target", default="-1")
@click.pass_context
def db_downgrade(ctx: click.Context, target: str) -> None:
    """Downgrade the database to ``target`` (default previous)."""
    ctx.obj[ALEMBIC].downgrade(target)


@db.command(name="revision")
@click.argument("version")
@click.option(
    "-e",
    "--empty",
    default=False,
    help="Allow generation of empty revision.",
    is_flag=True,
)
@click.pass_context
def db_revision(ctx: click.Context, version: str, *, empty: bool) -> None:
    """
    Generate a new migration file if there are model changes.

    The VERSION argument is the release version with which the migration should
    be associated.

    This command requires that the database is on the latest revision,
    otherwise it will bail out. By default (i.e. if ``--empty`` is not
    specified), this will generate a new file only if there are differences
    between :mod:`golfdb.model` and the current database. ``--empty`` overrides
    that and will allow an no-op migration file to be generated.
    """
    if not ctx.obj[ALEMBIC].is_current:
        msg = "error: database not up to date, run `golf db upgrade`"
        print(msg, file=sys.stderr)
        sys.exit(1)
    ctx.obj[ALEMBIC].revision(version, allow_empty=empty)
