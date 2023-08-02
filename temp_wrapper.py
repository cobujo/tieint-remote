from dataclasses import dataclass
from functools import wraps


def work(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'whoops -> {e}')
            return

    return inner


@dataclass
class Car:
    specs: tuple

    @property
    def color(self):
        return self.specs[0]

    @property
    def year(self):
        return self.specs[1]

    @property
    @work
    def colortest(self):
        if self.color == 'red':
            raise ValueError('no red cars!!')

        return f'{self.color} is good'


def funcname(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print(func.__name__, args, kwargs)
        return func(*args, **kwargs)

    return inner


@funcname
def double(num):
    return num * 2
