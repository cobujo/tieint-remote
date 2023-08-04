from dataclasses import dataclass, field
from typing import Optional
import re


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


def unformat_mtext(s, exclude_list=('P', 'S')):
    """Returns string with removed format information

    :param s: string with multitext
    :param exclude_list: don't touch tags from this list. Default ('P', 'S') for
                         newline and fractions

    ::

        >>> text = ur'{\\fGOST type A|b0|i0|c204|p34;TEST\\fGOST type A|b0|i0|c0|p34;123}'
        >>> unformat_mtext(text)
        u'TEST123'

    """
    s = re.sub(r'\{?\\[^%s][^;]+;' % ''.join(exclude_list), '', s)
    s = re.sub(r'\}', '', s)
    return s


def mtext_to_string(s):
    """
    Returns string with removed format innformation as :func:`unformat_mtext` and
    `\\P` (paragraphs) replaced with newlines

    ::

        >>> text = ur'{\\fGOST type A|b0|i0|c204|p34;TEST\\fGOST type A|b0|i0|c0|p34;123}\\Ptest321'
        >>> mtext_to_string(text)
        u'TEST123\\ntest321'

    """

    return unformat_mtext(s).replace(u'\\P', u'\n')
