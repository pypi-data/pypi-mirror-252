from enum import Enum
from dataclasses import dataclass

import re
import functools

from .config import ZERO_PADDING_DIGITS, NODE_MATCHER



@dataclass(frozen=True)
class Sheet:
    name: str
    transpose: bool

class Kind(Enum):
    HAZARD = 'H'
    CAUSE = 'CA'
    CONTROL = 'CO'


@functools.total_ordering
@dataclass(frozen=True)
class Node:
    kind: Kind
    number: int

    def to_str(self) -> str:
        return f'{self.kind.value}-{str(self.number).zfill(ZERO_PADDING_DIGITS)}'

    @classmethod
    def from_str(cls, string: str):
        match = re.match(NODE_MATCHER, string)
        if not match: raise Exception(f'{string} couldn\'t be parsed as a node')

        return cls(
            KIND_STR_DICT[match['kind']],
            int(match['number']),
        )

    def __lt__(self, other) -> bool:
        self.number < other.number

        
KIND_STR_DICT = {
    'H': Kind.HAZARD,
    'CA': Kind.CAUSE,
    'CO': Kind.CONTROL,
}

KIND_COLOURS = {
    Kind.HAZARD: '#d2476b',
    Kind.CAUSE: '#7d5594',
    Kind.CONTROL: '#2762bc',
}
