from dataclasses import dataclass


@dataclass(frozen=True)
class SecretVersionItem:
    version: str
    status: int
