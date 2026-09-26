import dataclasses
from typing import Final

from dlt.common.configuration import configspec
from dlt.destinations.impl.postgres.configuration import (
    PostgresClientConfiguration,
    PostgresCredentials,
)


@configspec(init=False)
class CrateDbCredentials(PostgresCredentials):
    drivername: Final[str] = dataclasses.field(  # type: ignore[misc]
        default="postgres", init=False, repr=False, compare=False
    )


# CrateDB does not support databases, just schemas.
# In dlt, schemas are conveyed by `dataset_name`?
del CrateDbCredentials.__dataclass_fields__["database"]


@configspec
class CrateDbClientConfiguration(PostgresClientConfiguration):
    destination_type: Final[str] = dataclasses.field(  # type: ignore[misc]
        default="cratedb", init=False, repr=False, compare=False
    )
    credentials: CrateDbCredentials

    def data_location(self) -> str:
        """Returns host:port. CrateDB has no databases, so the address identifies the data."""
        if not self.credentials or not self.credentials.host:
            self._no_data_location("the configuration has no host")
        port = self.credentials.port or self.DEFAULT_PORT
        return f"{self.credentials.host}:{port}"
