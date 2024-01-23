from .config import config


def dispatch_event(name: str):
    event_listeners = config("event_listeners")
    if name in event_listeners:
        function = event_listeners[name]
        return function()
