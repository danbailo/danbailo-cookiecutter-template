class SecretDisabledException(Exception):
    message: str = (
        'O secret está desabilitado! Verifique se existe alguma versão do secret ativa '
        'e tente novamente!'
    )

    def __init__(
        self,
        secret: str,
        version: str | None = None,
        project: str | None = None,
    ) -> None:
        message = self.message

        if secret:
            message += f' Secret: "{secret}"'
        if version:
            message += f' - Versão: "{version}"'
        if project:
            message += f' - Projeto: "{project}"'

        super().__init__(message)
