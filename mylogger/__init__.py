from mylogger.loggers import local_logger_catcher
from settings import auto_config as cfg
from tenacity import RetryCallState

cfg_space = cfg.__name__

if cfg_space == 'Local':
    logger, logcatch = local_logger_catcher()
else:
    print(f'config space: {cfg_space} is not accounted for in logger settings, please configure. In the meantime assuming local...')
    logger, logcatch = local_logger_catcher()


def args_kwargs_log(retry_state: RetryCallState):
    """
    Helper function to nicely show args or kwargs if/when present
    :param retry_state:
    :return:
    """
    if len(retry_state.args) > 0:
        args_msg = f' args: {retry_state.args}'
    else:
        args_msg = ''

    if len(retry_state.kwargs) > 0:
        kwargs_msg = f' kwargs: {retry_state.kwargs}'
    else:
        kwargs_msg = ''

    return f'{args_msg}{kwargs_msg}'


def my_before_sleep(retry_state: RetryCallState):
    """
    This is technically not a logger but a callback for tenacity retry.  However, this would be imported with a logger,
    and seems like overkill to create a package just for a simple retry callback
    https://tenacity.readthedocs.io/en/latest/#other-custom-callbacks
    :param retry_state:
    :return:
    """
    logger.info(f'retrying {retry_state.fn.__name__}, attempt #{retry_state.attempt_number},{args_kwargs_log(retry_state)}')
