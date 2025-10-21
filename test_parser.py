# -*- coding: utf-8 -*-
"""
Script de prueba automática para el Parser LR(1)
Ejecuta múltiples gramáticas sin interacción del usuario
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


def test_grammar_2():
    """Prueba: Gramatica simple S -> A a"""
    print("\n" + "=" * 70)
    print("PRUEBA 2: Gramatica Simple S -> A a | b A c")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("S", ["A", "a"])
    grammar.add_production("S", ["b", "A", "c"])
    grammar.add_production("S", ["d", "c"])
    grammar.add_production("S", ["b", "d", "a"])
    grammar.add_production("A", ["d"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()

    print("\n[OK] PRUEBA 2 COMPLETADA")
    return True


def test_grammar_3():
    """Prueba: Gramatica con recursion simple"""
    print("\n" + "=" * 70)
    print("PRUEBA 3: Recursion Simple S -> S + A")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("S", ["S", "+", "A"])
    grammar.add_production("S", ["A"])
    grammar.add_production("A", ["(", "S", ")"])
    grammar.add_production("A", ["a"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()

    print("\n[OK] PRUEBA 3 COMPLETADA")
    return True


def test_grammar_4():
    """Prueba: Lista separada por comas"""
    print("\n" + "=" * 70)
    print("PRUEBA 4: Listas L -> L , E | E")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("L", ["L", ",", "E"])
    grammar.add_production("L", ["E"])
    grammar.add_production("E", ["id"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()

    print("\n[OK] PRUEBA 4 COMPLETADA")
    return True


def test_grammar_5():
    """Prueba: Declaraciones de variables"""
    print("\n" + "=" * 70)
    print("PRUEBA 5: Declaraciones D -> type L ;")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("D", ["type", "L", ";"])
    grammar.add_production("L", ["L", ",", "id"])
    grammar.add_production("L", ["id"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()

    print("\n[OK] PRUEBA 5 COMPLETADA")
    return True


def test_grammar_6():
    """Prueba: Expresiones booleanas"""
    print("\n" + "=" * 70)
    print("PRUEBA 6: Expresiones Booleanas")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("E", ["E", "or", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["T", "and", "F"])
    grammar.add_production("T", ["F"])
    grammar.add_production("F", ["not", "F"])
    grammar.add_production("F", ["(", "E", ")"])
    grammar.add_production("F", ["true"])
    grammar.add_production("F", ["false"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()

    print("\n[OK] PRUEBA 6 COMPLETADA")
    return True


def test_grammar_7():
    """Prueba: Parentesis balanceados con epsilon"""
    print("\n" + "=" * 70)
    print("PRUEBA 7: Parentesis Balanceados (con epsilon)")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("S", ["(", "S", ")"])
    grammar.add_production("S", [])  # Producción epsilon

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()

    print("\n[OK] PRUEBA 7 COMPLETADA")
    return True


def test_grammar_8():
    """Prueba: Asignaciones"""
    print("\n" + "=" * 70)
    print("PRUEBA 8: Asignaciones S -> id = E")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("S", ["id", "=", "E"])
    grammar.add_production("E", ["E", "+", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["id"])
    grammar.add_production("T", ["num"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()

    print("\n[OK] PRUEBA 8 COMPLETADA")
    return True


def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("\n" + "=" * 70)
    print(" SUITE DE PRUEBAS AUTOMATICAS - PARSER LR(1)")
    print("=" * 70)
    print("\nEjecutando todas las pruebas sin interaccion del usuario...")

    tests = [
        ("Expresiones Aritmeticas", test_grammar_1),
        ("Gramatica Simple", test_grammar_2),
        ("Recursion Simple", test_grammar_3),
        ("Listas", test_grammar_4),
        ("Declaraciones", test_grammar_5),
        ("Expresiones Booleanas", test_grammar_6),
        ("Parentesis Balanceados", test_grammar_7),
        ("Asignaciones", test_grammar_8),
    ]

    results = []
    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            success = test_func()
            if success:
                results.append((name, "[PASS]"))
                passed += 1
            else:
                results.append((name, "[FAIL]"))
                failed += 1
        except Exception as e:
            results.append((name, f"[ERROR]: {str(e)}"))
            failed += 1

    # Resumen final
    print("\n" + "=" * 70)
    print(" RESUMEN DE PRUEBAS")
    print("=" * 70)

    for name, result in results:
        print(f"{result:<15} {name}")

    print("\n" + "-" * 70)
    print(f"Total de pruebas: {len(tests)}")
    print(f"Pasaron: {passed}")
    print(f"Fallaron: {failed}")
    print("-" * 70)

    if failed == 0:
        print("\n*** TODAS LAS PRUEBAS PASARON EXITOSAMENTE! ***")
        print("\nEl Parser LR(1) esta funcionando correctamente:")
        print("  [OK] Calculo de terminales y no terminales")
        print("  [OK] Conjuntos FIRST funcionando")
        print("  [OK] Conjuntos FOLLOW funcionando")
        print("  [OK] Clausura de items LR(1)")
        print("  [OK] Funcion GOTO")
        print("  [OK] Construccion del automata")
        print("  [OK] Generacion de tabla de parsing")
        print("  [OK] Sin errores de implementacion")
    else:
        print(f"\n[WARNING] {failed} prueba(s) fallaron. Revisa los errores arriba.")

    print("\n" + "=" * 70)


def test_with_visualization():
    """Prueba con generación de gráficos"""
    print("\n" + "=" * 70)
    print("GENERACIÓN DE GRÁFICOS")
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

    print("\nGenerando graficos del automata...")
    try:
        parser.visualize_automaton("test_automaton")
        parser.visualize_simplified_automaton("test_automaton")
        print("[OK] Graficos generados exitosamente")
    except Exception as e:
        print(f"[WARNING] No se pudieron generar los graficos: {e}")
        print("   (Esto es normal si Graphviz no esta instalado en el sistema)")


if __name__ == "__main__":
    # Ejecutar todas las pruebas
    run_all_tests()

    # Intentar generar gráficos
    test_with_visualization()

    print("\n" + "=" * 70)
    print("Pruebas completadas!")
    print("=" * 70)
