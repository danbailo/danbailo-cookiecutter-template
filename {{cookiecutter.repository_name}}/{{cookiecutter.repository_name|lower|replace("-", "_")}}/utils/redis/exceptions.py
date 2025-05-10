class MaxWaitTimeExceeded(Exception):
    message: str = 'Tempo máximo de espera ({minutes} minutos) excedido!'

    def __init__(self, max_wait_minutes: int) -> None:
        super().__init__(self.message.format(minutes=max_wait_minutes))
