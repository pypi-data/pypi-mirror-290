from pathlib import Path
from typing import (
    Dict,
    Optional
)

import motor.motor_asyncio
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

from keystone_database.models import DbConnectionOptions


class DbSettings(BaseSettings):
    host: str = "localhost"
    replica_set: Optional[str] = None
    name: str
    tls_pem_path: Optional[str] = None
    tls_ca_path: Optional[str] = None
    password: Optional[str] = None
    user: Optional[str] = None
    connection_options: DbConnectionOptions = DbConnectionOptions()

    __client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore", env_nested_delimiter="__", env_prefix="db_")

    def get_uri(self) -> str:
        if not self.connection_options.tls:
            return f"mongodb://{self.user}:{self.password}@{self.host}"

        options = [
                "authMechanism=MONGODB-X509"
        ]
        uri = f'mongodb://{self.host}/{self.name}?{"&".join(options)}'
        return uri

    def get_db(self) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        return self.get_client()[self.name]

    def get_client(self) -> motor.motor_asyncio.AsyncIOMotorClient:
        def __get_common_options() -> Dict[str, str]:
            return {
                    "replicaSet": self.replica_set,
                    "uuidRepresentation": "standard"
            }

        if not self.connection_options.tls:
            if self.password is None or self.user is None:
                msg = "db_pass and/or db_user have not been set"
                raise Exception(msg)

            if self.__client is None:
                self.__client = motor.motor_asyncio.AsyncIOMotorClient(
                        self.get_uri(),
                        **__get_common_options()
                )

            return self.__client

        if self.__client is None:
            self.__client = motor.motor_asyncio.AsyncIOMotorClient(
                    self.get_uri(),
                    tls=True,
                    tlsCertificateKeyFile=self.tls_pem_path,
                    tlsCAFile=self.tls_ca_path,
                    **__get_common_options()
            )

        return self.__client


class Context:
    settings: Optional[DbSettings] = None


__ctx = Context()


def init_settings(root: Path):
    __ctx.settings = DbSettings(_env_file=root / ".env")


def get_settings() -> DbSettings:
    if __ctx.settings is None:
        msg = "Settings are not initialized -- call init_settings()"
        raise Exception(msg)
    return __ctx.settings
