# -*- coding: utf-8 -*-
"""
Script simple para ejecutar solo la prueba 1
"""

from lr1_parser import Grammar, LR1Parser


def test_grammar_1():
    """Prueba: Expresiones aritmeticas clasicas"""
    print("\n" + "=" * 70)
    print("PRUEBA 1: Expresiones Aritmeticas (E + T * F)")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("E", ["E", "+", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["T", "*", "F"])
    grammar.add_production("T", ["F"])
    grammar.add_production("F", ["(", "E", ")"])
    grammar.add_production("F", ["id"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_automaton()
    parser.print_parsing_table()

    print("\n[OK] PRUEBA 1 COMPLETADA")
    return True


if __name__ == "__main__":
    try:
        result = test_grammar_1()
        if result:
            print("\n[SUCCESS] La prueba paso correctamente!")
        else:
            print("\n[FAIL] La prueba fallo")
    except Exception as e:
        print(f"\n[ERROR] Excepcion: {e}")
        import traceback

        traceback.print_exc()
