"""Sample grammars for demonstrations and tests."""
from __future__ import annotations

from .grammar import Grammar


def create_example_grammar_1() -> Grammar:
    grammar = Grammar()
    grammar.add_production("E", ["E", "+", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["T", "*", "F"])
    grammar.add_production("T", ["F"])
    grammar.add_production("F", ["(", "E", ")"])
    grammar.add_production("F", ["id"])
    return grammar


def create_example_grammar_2() -> Grammar:
    grammar = Grammar()
    grammar.add_production("S", ["A", "a"])
    grammar.add_production("S", ["b", "A", "c"])
    grammar.add_production("S", ["d", "c"])
    grammar.add_production("S", ["b", "d", "a"])
    grammar.add_production("A", ["d"])
    return grammar


def create_example_grammar_3() -> Grammar:
    grammar = Grammar()
    grammar.add_production("S", ["S", "+", "A"])
    grammar.add_production("S", ["A"])
    grammar.add_production("A", ["(", "S", ")"])
    grammar.add_production("A", ["a"])
    return grammar
