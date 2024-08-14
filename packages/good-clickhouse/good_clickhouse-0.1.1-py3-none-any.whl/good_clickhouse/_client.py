import os
import typing
from fast_depends import inject
from clickhouse_driver import connect
from clickhouse_driver.dbapi.connection import Connection
from clickhouse_driver.dbapi.extras import NamedTupleCursor
from aioch import Client as AsyncClient
from loguru import logger

from good_common.dependencies import BaseProvider, AsyncBaseProvider

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, field_serializer


class ConnectionProfile(BaseSettings):
    host: str = "localhost"
    port: int = 9000
    database: str = "default"
    user: str
    password: SecretStr
    secure: bool = False
    compression: bool = False
    
    @field_serializer('password', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()
    
    @classmethod
    def load_by_prefix(cls, prefix: str, config: typing.MutableMapping):
        return cls(
            host=config.get(f"{prefix}_HOST", "localhost"),
            port=config.get(f"{prefix}_PORT", 9000),
            database=config.get(f"{prefix}_DATABASE", "default"),
            user=config.get(f"{prefix}_USER", "default"),
            password=config.get(f"{prefix}_PASSWORD", "default"),
            secure=config.get(f"{prefix}_SECURE", False),
            compression=config.get(f"{prefix}_COMPRESSION", False),
        )



class Clickhouse:
    def __init__(self, connection: Connection):
        self.connection = connection

    def __enter__(self):
        self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()


class ClickhouseProvider(BaseProvider[Clickhouse], Clickhouse):
    def __init__(self, profile: str | None = None, _debug: bool = False):
        super().__init__(_debug=_debug, profile=profile)
        

    def initializer(self, cls_args, cls_kwargs, fn_kwargs):
        # mode = {**cls_kwargs, **fn_kwargs}.get("profile", "cloud").upper()
        kwargs = {}
        
        profile_name = {**cls_kwargs, **fn_kwargs}.get("profile")
        
        profile = 'CLICKHOUSE' if profile_name is None else 'CLICKHOUSE_' + profile_name.upper()
        
        if profile:
            kwargs = {
                **ConnectionProfile.load_by_prefix(profile, os.environ).model_dump(),
            }

        return cls_args, kwargs

    @classmethod
    def provide(cls, *args, **kwargs) -> Clickhouse:
        return Clickhouse(connection=connect(**kwargs))


class ClickhouseAsync:
    @inject
    def __init__(self, sync_client: Clickhouse = ClickhouseProvider(), mode="local"):
        # logger.debug(sync_client)
        # logger.debug(sync_client.connection)
        self.connection = AsyncClient(_client=sync_client.connection._make_client())
        # logger.debug(self.connection)

    async def __aenter__(self):
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
        # await self.cursor.close()
        # await self.connection.close()


class ClickhouseAsyncProvider(AsyncBaseProvider[ClickhouseAsync], ClickhouseAsync):
    pass
