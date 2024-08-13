from mongomock_motor import AsyncMongoMockClient

from keystone_database.db_settings import DbSettings


class DbSettingsMock(DbSettings):
    def get_client(self) -> AsyncMongoMockClient:
        return AsyncMongoMockClient()


settings_mock = DbSettingsMock(
        name="test"
)
