'''Compatibility wrapper exposing the LR(1) parser toolkit.'''
from __future__ import annotations

from lr1 import (
    Grammar,
    LR1Item,
    LR1Parser,
    create_example_grammar_1,
    create_example_grammar_2,
    create_example_grammar_3,
)
from lr1.cli import main

__all__ = [
    'Grammar',
    'LR1Item',
    'LR1Parser',
    'create_example_grammar_1',
    'create_example_grammar_2',
    'create_example_grammar_3',
    'main',
]


if __name__ == '__main__':
    main()
