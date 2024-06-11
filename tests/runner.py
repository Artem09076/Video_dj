"""This module include test runner."""
from types import MethodType
from typing import Any

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner


def prepare_db(self):
    """Create schema.

    Args:
        self: object
    """
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS video_data;')


class PostgresSchemaRunner(DiscoverRunner):
    """Postgres schema runner.

    Args:
        DiscoverRunner: django discover runner
    """

    def setup_databases(
        self, **kwargs: Any,
    ) -> list[tuple[BaseDatabaseWrapper, str, bool]]:
        """Set up databases.

        Args:
            kwargs: keywords arguments fro function

        Returns:
            list[tuple[BaseDatabaseWrapper, str, bool]]: list of django BaseDatabaseWrapper
        """
        for conn_name in connections:
            connection = connections[conn_name]
            connection.prepare_database = MethodType(prepare_db, connection)
        return super().setup_databases(**kwargs)
