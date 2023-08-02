import win32com.client as client
from pywintypes import com_error
import time
from mylogger import logger
import settings.constants as cn

# most code below taken from: https://stackoverflow.com/a/55892457/3089019
CALLEE_ERROR = 'Call was rejected by callee.'


def _com_call_wrapper(f, *args, **kwargs):
    """
    ComWrapper support function
    :param f: function or method
    :param args: args
    :param kwargs: kwargs
    :return:
    """
    result = None
    # unwrap inputs
    args = [arg._wrapped_object if isinstance(arg, ComWrapper) else arg for arg in args]
    kwargs = dict([(key, value._wrapped_object)
                   if isinstance(value, ComWrapper)
                   else (key, value)
                   for key, value in dict(kwargs).items()])

    start_time = None
    # TODO: Medium -> should we rewrite this to use tenacity?
    while True:
        try:
            result = f(*args, **kwargs)
        except com_error as e:
            if e.strerror == CALLEE_ERROR:
                if start_time is None:
                    start_time = time.time()
                    logger.warning(f'{CALLEE_ERROR} -> detected, trying again...')

                elif time.time() - start_time >= cn.COM_TIMEOUT:
                    raise

                time.sleep(cn.COM_DELAY)
                continue

            raise

        break

    if isinstance(result, client.CDispatch) or callable(result):
        return ComWrapper(result)
    return result


class ComWrapper(object):
    """
    Class to wrap COM objects to repeat calls when 'Call was rejected by callee.' exception occurs.
    """

    def __init__(self, wrapped_object):
        assert isinstance(wrapped_object, client.CDispatch) or callable(wrapped_object)
        self.__dict__['_wrapped_object'] = wrapped_object

    def __getattr__(self, item):
        return _com_call_wrapper(self._wrapped_object.__getattr__, item)

    def __getitem__(self, item):
        return _com_call_wrapper(self._wrapped_object.__getitem__, item)

    def __setattr__(self, key, value):
        _com_call_wrapper(self._wrapped_object.__setattr__, key, value)

    def __setitem__(self, key, value):
        _com_call_wrapper(self._wrapped_object.__setitem__, key, value)

    def __call__(self, *args, **kwargs):
        return _com_call_wrapper(self._wrapped_object.__call__, *args, **kwargs)

    def __repr__(self):
        return f'ComWrapper <{repr(self._wrapped_object)}>'
