from dataclasses import dataclass

@dataclass
class RedisKeysConfig:
    prefix: str = ''
    separator: str = ':'
    ttl_seconds: int = 180
