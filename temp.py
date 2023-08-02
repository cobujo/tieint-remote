from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Wow:
    number: int
    triple: int = field(init=False)

    @property
    def double(self):
        return self.number * 2

    def __post_init__(self):
        self.triple = self.number * 3

    def saymyname(self):
        print(__name__)


@dataclass
class Other():
    num: int
    word: Optional[str] = None


@dataclass
class Whee(Wow):
    quad: int = field(init=False)
    other_obj: Other = field(init=False)

    def __post_init__(self):
        self.quad = self.number * 4


def one(x: Optional[int] = None) -> None:
    print(f'one is {x}')


def two(x: Optional[iter]) -> None:
    print(f'two is {x}')


def exc(num):
    try:
        num / 0
    except Exception as e:
        return e


def kws(this, that, *args, **kwargs):
    print(f'this is: {this}')
    print(f'that is: {that}')
    print(args)
    print(kwargs)


def err():
    try:
        3 / 0
    except Exception as e:
        return e


def one():
    return 1

def uno():
    return one()
