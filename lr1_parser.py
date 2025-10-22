# -*- coding: utf-8 -*-
"""
Parser LR(1) - Punto de Entrada Principal
Este archivo utiliza la estructura modular del paquete lr1_parser/
"""

from lr1_parser import (
    Grammar,
    LR1Parser,
    create_example_grammar_1,
    create_example_grammar_2,
    create_example_grammar_3,
)


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print(" PARSER LR(1) - Análisis Sintáctico Ascendente")
    print("=" * 60)

    print("\nSeleccione una gramática de ejemplo:")
    print("1. Expresiones aritméticas")
    print("2. Gramática S -> A a | b A c | d c | b d a")
    print("3. Gramática simple S -> S + A | A")

    choice = input("\nIngrese su opción (1-3) [1]: ").strip() or "1"

    if choice == "2":
        grammar = create_example_grammar_2()
    elif choice == "3":
        grammar = create_example_grammar_3()
    else:
        grammar = create_example_grammar_1()

    grammar.print_grammar()

    print("\n[...] Construyendo parser LR(1)...")
    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_sets(parser.first, parser.follow)
    parser.print_automaton()
    parser.print_parsing_table()
    parser.print_closure_table()

    print("\n" + "=" * 60)
    print("GENERACIÓN DE GRÁFICOS")
    print("=" * 60)
    parser.visualize_automaton()
    parser.visualize_simplified_automaton()

    print("\n" + "=" * 60)
    print("[OK] PARSER LR(1) COMPLETADO EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()
