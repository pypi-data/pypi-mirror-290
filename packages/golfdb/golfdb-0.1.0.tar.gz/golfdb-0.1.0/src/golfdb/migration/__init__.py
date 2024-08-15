"""API for performing Alembic migrations."""

from __future__ import annotations

import pathlib
import typing

import alembic.autogenerate
import alembic.config
import alembic.operations
import alembic.runtime.environment
import alembic.runtime.migration
import alembic.script

from golfdb.model import Base

if typing.TYPE_CHECKING:
    import sqlalchemy


#: Template used for generating migration filenames. For GolfDB, the local
#: style is to make sure the resulting names are valid Python module names.
FILENAME_TEMPLATE: str = (
    "migration_"
    "%%(year)d_%%(month).2d_%%(day).2d_"
    "%%(hour).2d_%%(minute).2d_%%(second).2d_"
    "%%(rev)s_%%(slug)s"
)


class Alembic:
    """
    Perform migration operations on/against a database.

    :param engine: SQLAlchemy engine for the database.
    """

    def __init__(self, engine: sqlalchemy.Engine) -> None:
        self._path = str(pathlib.Path(__file__).parents[1] / "migration")

        self._config = alembic.config.Config()
        self._config.set_main_option("file_template", FILENAME_TEMPLATE)
        self._config.set_main_option("script_location", self._path)
        self._config.set_main_option("version_locations", self._path)

        self._script_directory = alembic.script.ScriptDirectory.from_config(
            self._config,
        )

        env = alembic.runtime.environment.EnvironmentContext(
            self._config,
            self._script_directory,
        )
        env.configure(
            connection=engine.connect(),
            target_metadata=Base.metadata,
            compare_server_default=True,
        )
        self._context = env.get_context()

    @property
    def is_current(self) -> bool:
        """Indicates whether the database is updated to the latest revision."""
        head = self._script_directory.get_revision("head")
        if head is None:
            return False
        return head.revision == self._context.get_current_revision()

    def _run(
        self,
        fn: typing.Callable[
            [str, alembic.runtime.environment.MigrationContext],
            list[alembic.runtime.migration.RevisionStep],
        ],
    ) -> None:
        """
        Perform migration operations in the proper context(s).

        :param fn: Function to run that returns the Alembic
                   :class:`alembic.runtime.migration.RevisionStep`-s to be
                   executed.
        """
        # SLF001: Cribbed from flask-alembic.
        self._context._migrations_fn = fn  # noqa: SLF001
        with (
            self._context.begin_transaction(),
            alembic.operations.Operations.context(self._context),
        ):
            self._context.run_migrations()

    def upgrade(self, target: str) -> None:
        """
        Upgrade the database to ``target``.

        :param target: Version to upgrade to. Examples include ``head``,
                       ``head-1``, and ``+3``. See the Alembic documentation
                       for more information.
        """

        def do_upgrade(
            revision: str,
            _: alembic.runtime.environment.MigrationContext,
        ) -> list[alembic.runtime.migration.RevisionStep]:
            # SLF001: Cribbed from flask-alembic.
            fn = self._script_directory._upgrade_revs  # noqa: SLF001
            return fn(target, revision)

        self._run(do_upgrade)

    def downgrade(self, target: str) -> None:
        """
        Downgrade the database to ``target``.

        :param target: Version to downgrade to. Examples include ``head-1`` and
                       ``-3``. See the Alembic documentation for more
                       information.
        """

        def do_downgrade(
            revision: str,
            _: alembic.runtime.environment.MigrationContext,
        ) -> list[alembic.runtime.migration.RevisionStep]:
            # SLF001: Cribbed from flask-alembic.
            fn = self._script_directory._downgrade_revs  # noqa: SLF001
            return fn(target, revision)

        self._run(do_downgrade)

    def revision(self, version: str, *, allow_empty: bool = False) -> None:
        """
        Generate a migration file in the migrations directory in the codebase.

        Note that the caller is responsible for checking :attr:`is_current`;
        if the database is not current, an exception will be raised out of
        Alembic.

        :param version: Alembic slug. For GolfDB, this should be the release
                        version with which the migration is associated (e.g.
                        ``0.1.0`` or ``1.3.7``).
        :param allow_empty: If ``False`` (the default), then no file will be
                            generated if there are no differences between the
                            model definition and the database. If ``True``,
                            this will generate an empty migration file if there
                            are no differences.
        """
        migration = alembic.autogenerate.produce_migrations(
            self._context,
            Base.metadata,
        )
        has_migration = False
        if migration is not None:
            ops = migration.upgrade_ops
            # Item "None" of "UpgradeOps | None" has no attribute "as_diffs"
            # Ignore this error as we explicitly check for not None above.
            diffs = ops.as_diffs()  # type: ignore[union-attr]
            has_migration = len(diffs) > 0
        if has_migration or allow_empty:
            revision_context = alembic.autogenerate.RevisionContext(
                self._config,
                self._script_directory,
                {
                    "branch_label": None,
                    "depends_on": None,
                    "head": "head",
                    "message": version,
                    "rev_id": None,
                    "splice": False,
                    "sql": False,
                    "version_path": self._path,
                },
            )

            def do_revision(
                revision: str,
                context: alembic.runtime.environment.MigrationContext,
            ) -> list[alembic.runtime.migration.RevisionStep]:
                revision_context.run_autogenerate(revision, context)
                return []

            self._run(do_revision)

            # :meth:`alembic.autogenerate.RevisionContext.generate_scripts`
            # returns a generator, so we use list() to force it to execute.
            list(revision_context.generate_scripts())
