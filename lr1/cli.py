"""Simple command-line demo for the LR(1) parser."""
from __future__ import annotations

from .examples import (
    create_example_grammar_1,
    create_example_grammar_2,
    create_example_grammar_3,
)
from .parser import LR1Parser


def _build_grammar(choice: str):
    examples = {
        "1": ("Expresiones aritmeticas", create_example_grammar_1),
        "2": ("Gramatica S -> A a | b A c", create_example_grammar_2),
        "3": ("Gramatica S -> S + A | A", create_example_grammar_3),
    }
    return examples.get(choice, examples["1"])


def main() -> None:
    print("\n" + "=" * 60)
    print(" PARSER LR(1) - Analisis Sintactico Ascendente")
    print("=" * 60)

    print("\nSeleccione una gramatica de ejemplo:")
    print("1. Expresiones aritmeticas (E -> E + T | T, etc.)")
    print("2. Gramatica S -> A a | b A c | d c | b d a")
    print("3. Gramatica simple S -> S + A | A")

    choice = input("\nIngrese su opcion (1-3) [1]: ").strip() or "1"
    description, factory = _build_grammar(choice)
    grammar = factory()

    print(f"\nSeleccionaste: {description}")
    grammar.print_grammar()

    print("\n[...] Construyendo parser LR(1)...")
    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_sets(parser.first, parser.follow)
    parser.print_automaton()
    parser.print_parsing_table()

    print("\n" + "=" * 60)
    print("GENERACION DE GRAFICOS")
    print("=" * 60)
    parser.visualize_automaton()
    parser.visualize_simplified_automaton()

    print("\n" + "=" * 60)
    print("[OK] PARSER LR(1) COMPLETADO EXITOSAMENTE")
    print("=" * 60)

    print("\nEl parser incluye:")
    print("  [OK] Calculo de terminales y no terminales")
    print("  [OK] Conjuntos FIRST")
    print("  [OK] Conjuntos FOLLOW")
    print("  [OK] Automata LR(1) con items")
    print("  [OK] Tabla de parsing (ACTION y GOTO)")
    print("  [OK] Graficos visuales del automata")

    print("\nArchivos generados:")
    print("  - automaton_lr1.png (grafico detallado)")
    print("  - automaton_lr1_simplified.png (grafico simplificado)")
