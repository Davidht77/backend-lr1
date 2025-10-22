# -*- coding: utf-8 -*-
"""
Módulo Examples
Define funciones para crear gramáticas de ejemplo.
"""

from .grammar import Grammar


def create_example_grammar_1():
    """Crea una gramática de ejemplo simple"""
    grammar = Grammar()

    # Gramática: E → E + T | T
    #            T → T * F | F
    #            F → ( E ) | id

    grammar.add_production("E", ["E", "+", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["T", "*", "F"])
    grammar.add_production("T", ["F"])
    grammar.add_production("F", ["(", "E", ")"])
    grammar.add_production("F", ["id"])

    return grammar


def create_example_grammar_2():
    """Crea otra gramática de ejemplo"""
    grammar = Grammar()

    # Gramática: S → A a | b A c | d c | b d a
    #            A → d

    grammar.add_production("S", ["A", "a"])
    grammar.add_production("S", ["b", "A", "c"])
    grammar.add_production("S", ["d", "c"])
    grammar.add_production("S", ["b", "d", "a"])
    grammar.add_production("A", ["d"])

    return grammar


def create_example_grammar_3():
    """Crea una gramática con recursión a la izquierda"""
    grammar = Grammar()

    # Gramática simple con operadores
    # S → S + A | A
    # A → ( S ) | a

    grammar.add_production("S", ["S", "+", "A"])
    grammar.add_production("S", ["A"])
    grammar.add_production("A", ["(", "S", ")"])
    grammar.add_production("A", ["a"])

    return grammar
