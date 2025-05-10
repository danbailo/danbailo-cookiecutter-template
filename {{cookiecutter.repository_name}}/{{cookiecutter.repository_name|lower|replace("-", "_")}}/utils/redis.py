from os import environ

from redis import Connection, ConnectionPool, SSLConnection, StrictRedis


class RedisConnectionFactory:
    _pool: ConnectionPool | None = None
    _ssl_environ: str = 'SSL_CERT_FILE'
    _ca_path: str = '/tmp/redis_ca.pem'

    @classmethod
    def save_certificate(
        cls,
        data: str,
    ):
        with open(cls._ca_path, 'w') as ca_file:
            ca_file.write(data)

    @classmethod
    def activate_certificate(cls, ca_path: str | None = None):
        if not ca_path:
            ca_path = cls._ca_path
        environ[cls._ssl_environ] = ca_path

    @classmethod
    def pool(cls, host: str = 'localhost', port: int = 6378, ssl: bool = False):
        if cls._pool:
            return cls._pool

        return ConnectionPool(
            connection_class=SSLConnection if ssl else Connection,
            host=host,
            port=port,
            decode_responses=True,
        )

    @classmethod
    def new(
        cls,
        host: str = 'localhost',
        port: int = 6378,
        ssl: bool = False,
        ca_data: str | None = None,
        ca_path: str | None = None,
    ):
        if ssl and not (ca_data or ca_path):
            raise ValueError(
                'Para usar SSL você deve passar o conteúdo ou caminho de um CA!'
            )

        elif ssl and ca_data:
            cls.save_certificate(ca_data)

        if ssl:
            cls.activate_certificate(ca_path)

        return StrictRedis(connection_pool=cls.pool(host, port, ssl))
