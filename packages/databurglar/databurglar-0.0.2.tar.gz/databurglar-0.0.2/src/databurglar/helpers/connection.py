from dataclasses import dataclass
from sqlalchemy import create_engine, Engine


@dataclass
class DatabaseConnection:
    user: str
    password: str
    host: str
    port: int
    database: str


def connect_to_pg(connection: DatabaseConnection) -> Engine:
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            connection.user,
            connection.password,
            connection.host,
            connection.port,
            connection.database
        )
    )
