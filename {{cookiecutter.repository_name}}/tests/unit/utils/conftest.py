import pytest
import structlog


class StructuredLogCapture(object):
    def __init__(self):
        self.events = []

    def process(self, logger, method_name, event_dict):
        event_dict['log_level'] = method_name
        self.events.append(event_dict)
        raise structlog.DropEvent


def no_op(*args, **kwargs):
    pass


@pytest.fixture
def log(monkeypatch):
    """Fixture providing access to captured structlog events. Interesting attributes:

        ``log.events`` a list of dicts, contains any events logged during the test
        ``log.has`` a helper method, return a bool for making simple assertions

    Example usage: ``assert log.has("some message", var1="extra context")``
    """
    # save settings for later
    processors = structlog.get_config().get('processors', [])
    configure = structlog.configure

    # redirect logging to log capture
    cap = StructuredLogCapture()
    structlog.reset_defaults()
    structlog.configure(processors=[cap.process])
    monkeypatch.setattr('structlog.configure', no_op)
    monkeypatch.setattr('structlog.configure_once', no_op)
    yield cap

    # back to normal behavior
    configure(processors=processors)
