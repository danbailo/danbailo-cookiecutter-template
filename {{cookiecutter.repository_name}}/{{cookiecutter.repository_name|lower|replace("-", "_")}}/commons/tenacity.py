from tenacity import RetryCallState

from process_data_flow.commons.logger import Logger, LoggerFactory

_logger: Logger = LoggerFactory.new()


def warning_if_failed(retry_state: RetryCallState):
    """Should be passed in `before` parameter.

    Logger a warning after first call method attempt.
    """
    if retry_state.attempt_number > 1:
        _logger.warning(
            'Trying again...',
            attempt=retry_state.attempt_number,
            method=retry_state.fn.__qualname__,
        )
