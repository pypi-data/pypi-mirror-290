from .streamlit_event_hook import *

__doc__ = streamlit_event_hook.__doc__
if hasattr(streamlit_event_hook, "__all__"):
    __all__ = streamlit_event_hook.__all__

import threading
from queue import Queue

from streamlit.runtime.state import get_session_state


que = Queue()


def before_render():
    print("-- before")
    with get_session_state().query_params() as qp:
        print(qp)
        if len(qp) == 0:
            qp.from_dict({"_aa": 12312})
            print("set")


def after_render():
    print("-- after")


def event_handler(sender, event, forward_msg):
    print(f"sender: {sender} \nevent: {event} \nforward_msg: {forward_msg}")
    print("---" * 10)


# def listen_to_channel(channel_name):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             r = redis.Redis()
#             pubsub = r.pubsub()
#             pubsub.subscribe(channel_name)
#             for message in pubsub.listen():
#                 if message['type'] == 'message':
#                     func(message['data'])
#         return wrapper
#     return decorator

# @listen_to_channel('my_channel')
def handle_message(message):
    print(f"Received message: {message}")


def run_once(func):
    lock = threading.Lock()
    has_run = [False]

    def wrapper(*args, **kwargs):
        with lock:
            if not has_run[0]:
                has_run[0] = True
                return func(*args, **kwargs)
    return wrapper


@run_once
def init():
    streamlit_event_hook.hook(
        before_render=f"{before_render.__module__}.{before_render.__name__}",
        after_render=f"{after_render.__module__}.{after_render.__name__}",
        event_handler=f"{event_handler.__module__}.{event_handler.__name__}"
    )
