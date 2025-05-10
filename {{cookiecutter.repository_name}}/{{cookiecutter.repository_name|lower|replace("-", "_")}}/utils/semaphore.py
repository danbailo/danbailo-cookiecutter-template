from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from time import sleep

from redis import StrictRedis

from legalops_commons.exceptions import MaxWaitTimeExceeded
from legalops_commons.factories.logger import Logger, LoggerFactory


@dataclass
class RedisKeysConfig:
    prefix: str = ''
    separator: str = ':'
    ttl_seconds: int = 180


class RedisSemaphore:
    def __init__(
        self,
        redis: StrictRedis,
        keys_config: RedisKeysConfig = RedisKeysConfig(),
        lock_content: str = 'LOCKED',
        max_wait_minutes: int = 5,
        try_wait_seconds: int = 10,
        logger: Logger = LoggerFactory.new(),
    ):
        self.redis = redis
        self.keys_config = keys_config
        self.lock_content = lock_content
        self.max_wait_minutes = max_wait_minutes
        self.max_wait_time = timedelta(minutes=self.max_wait_minutes)
        self.try_wait_seconds = try_wait_seconds
        self.logger = logger

    def get_redis_key(self, key: str) -> str:
        return self.keys_config.separator.join([self.keys_config.prefix, key])

    def acquire_lock(self, key: str) -> bool:
        self.logger.debug(f'Tentando obter chave "{key}"...')
        redis_key = self.get_redis_key(key)
        locked = self.redis.set(
            name=redis_key,
            value=self.lock_content,
            ex=self.keys_config.ttl_seconds,
            nx=True,
        )
        if locked:
            self.logger.info(
                f'Chave "{key}" trancada com sucesso!',
                redis_key=redis_key,
                lock_content=self.lock_content,
                ttl_seconds=self.keys_config.ttl_seconds,
            )
        return bool(locked)

    def unlock(self, key: str):
        self.logger.debug(f'Destravando chave "{key}"...')
        redis_key = self.get_redis_key(key)
        self.redis.delete(redis_key)
        self.logger.info(f'Chave "{key}" destravada com sucesso!', redis_key=redis_key)

    def ready(self, keys: list[str]) -> str:
        """
        Recebe uma lista de chaves e retorna a primeira a ser liberada.
        """
        self.logger.debug('Procurando chave desbloqueada...', keys=keys)
        start_time = datetime.now()
        while True:
            if (datetime.now() - start_time) >= self.max_wait_time:
                raise MaxWaitTimeExceeded(self.max_wait_minutes)

            for key in keys:
                if self.acquire_lock(key):
                    return key

            self.logger.debug(
                f'Nenhuma chave desbloqueada. Tentando novamente em {self.try_wait_seconds} segundos...'
            )
            sleep(self.try_wait_seconds)

    @contextmanager
    def context(self, keys: list[str]):
        """Gerencia o contexto das chaves passadas no atributo `keys`, retornando a
        primeira chave a ser liberada. Ao realizar todas as ações, a chave é destravada.

        Exemplo:
        ```python
            semaphore = RedisSemaphore(...)
            with semaphore.context(['foo', 'bar']) as key:
                print(key)
        ```
        """
        key = None
        try:
            key = self.ready(keys)
            yield key
        except Exception as e:
            raise e
        finally:
            if key:
                self.unlock(key)
