from requests import Response

from {{cookiecutter.repository_name|lower|replace("-", "_")}}.utils.logger import Logger, LoggerFactory


class SlackWebhookClient:
    def __init__(
        self,
        username: str,
        icon_url: str | None = None,
        logger: Logger = LoggerFactory.new(),
    ):
        self.username = username
        self.icon_url = icon_url
        self.logger = logger

    def get_message_request_body(self, message: str):
        payload = {
            'blocks': [
                {'type': 'section', 'text': {'type': 'mrkdwn', 'text': message}}
            ],
            'username': self.username,
            'icon_url': self.icon_url,
        }
        return payload

    def send_message(self, webhook_url: str, message: str) -> Response:
        data = self.get_message_request_body(message)

        response = requests.post(webhook_url, json=data)
        response.raise_for_status()

        self.logger.debug('Mensagem enviada com sucesso!', data=data)
        return response
