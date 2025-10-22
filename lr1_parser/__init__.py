# -*- coding: utf-8 -*-
"""
Parser LR(1) - Paquete Modular
Implementa el análisis sintáctico LR(1) con arquitectura modular.
"""

from .grammar import Grammar
from .item import LR1Item
from .parser import LR1Parser
from .visualizer import RegularGrammarAFNVisualizer
from .examples import (
    create_example_grammar_1,
    create_example_grammar_2,
    create_example_grammar_3,
)

__version__ = "1.0.0"
__all__ = [
    "Grammar",
    "LR1Item",
    "LR1Parser",
    "RegularGrammarAFNVisualizer",
    "create_example_grammar_1",
    "create_example_grammar_2",
    "create_example_grammar_3",
]
