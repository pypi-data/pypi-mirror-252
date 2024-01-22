from __future__ import annotations

import abc
import pathlib

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


def get_op(engine: AsyncEngine, connection_url: sqlalchemy.URL) -> Op:
    match engine.dialect.name:
        case "postgresql":
            return PostgresOp(engine, connection_url)
        case "sqlite":
            return SqliteOp(engine, connection_url)
        case _:
            raise NotImplementedError


class Op(abc.ABC):
    def __init__(self, engine: AsyncEngine, connection_url: sqlalchemy.URL) -> None:
        self._engine = engine
        self._connection_url = connection_url

    @property
    def _db_name(self) -> str:
        if not self._connection_url.database:
            msg = "Connection URL should have a database"
            raise ValueError(msg)

        return self._connection_url.database

    @abc.abstractmethod
    async def create_db_if_not_exists(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def drop_db(self, *, reuse_db: bool) -> None:
        raise NotImplementedError


class PostgresOp(Op):
    async def create_db_if_not_exists(self) -> None:
        async with self._engine.connect() as conn:
            exists = await conn.scalar(
                text(
                    f"SELECT 1 FROM pg_database WHERE datname='{self._db_name}'",  # noqa: S608
                ),
            )
            if not exists:
                await conn.execute(text(f'create database "{self._db_name}";'))

    async def drop_db(self, *, reuse_db: bool) -> None:
        async with self._engine.connect() as conn:
            if reuse_db:
                return
            await conn.execute(
                text(
                    f"""
                    select pg_terminate_backend(pg_stat_activity.pid)
                    from pg_stat_activity
                    where pg_stat_activity.datname = '{self._db_name}'
                    and pid <> pg_backend_pid();
                    """,  # noqa: S608
                ),
            )
            await conn.execute(text(f'drop database "{self._db_name}";'))


class SqliteOp(Op):
    async def create_db_if_not_exists(self) -> None:
        if pathlib.Path(self._db_name).exists():
            return

        async with self._engine.connect():
            pass

    async def drop_db(self, *, reuse_db: bool) -> None:
        if reuse_db:
            return
        pathlib.Path(self._db_name).unlink(missing_ok=True)
