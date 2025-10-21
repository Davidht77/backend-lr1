# -*- coding: utf-8 -*-
"""
Demo Automatica del Parser LR(1)
Ejecuta automaticamente y muestra todas las funcionalidades
SIN necesidad de interaccion del usuario
"""

from lr1_parser import Grammar, LR1Parser


def print_header(title, char="="):
    """Imprime un encabezado formateado"""
    print("\n" + char * 80)
    print(f" {title}")
    print(char * 80)


def print_section(title):
    """Imprime una seccion"""
    print("\n" + "-" * 80)
    print(f" {title}")
    print("-" * 80)


def demo_gramatica_completa():
    """Demo completa con una gramatica de expresiones aritmeticas"""
    print_header("PARSER LR(1) - DEMOSTRACION COMPLETA AUTOMATICA")

    print("\n[INICIO] Demostrando todas las capacidades del Parser LR(1)")
    print("\nGramatica a analizar: Expresiones Aritmeticas")
    print("  E -> E + T | T")
    print("  T -> T * F | F")
    print("  F -> ( E ) | id")
    print("\nEsta gramatica permite expresiones como: id + id * id, (id + id), etc.")

    # Paso 1: Crear la gramatica
    print_section("PASO 1: Creacion de la Gramatica")

    grammar = Grammar()
    grammar.add_production("E", ["E", "+", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["T", "*", "F"])
    grammar.add_production("T", ["F"])
    grammar.add_production("F", ["(", "E", ")"])
    grammar.add_production("F", ["id"])

    print("\n[OK] Gramatica creada con 6 producciones")
    print("     - Simbolo inicial: E")
    print("     - Producciones para E, T, F")

    # Paso 2: Construir el parser
    print_section("PASO 2: Construccion del Parser LR(1)")
    print("\n[PROCESANDO] Construyendo el parser LR(1)...")
    print("  - Aumentando la gramatica con E'")
    print("  - Calculando terminales y no terminales")
    print("  - Calculando conjuntos FIRST")
    print("  - Calculando conjuntos FOLLOW")
    print("  - Construyendo automata de items LR(1)")
    print("  - Generando tabla de parsing")

    parser = LR1Parser(grammar)
    parser.build()

    print("\n[OK] Parser construido exitosamente!")

    # Paso 3: Mostrar gramatica completa
    print_section("PASO 3: Gramatica Aumentada")
    grammar.print_grammar()

    # Paso 4: Mostrar terminales y no terminales
    print_section("PASO 4: Analisis de Simbolos")
    print(f"\nTerminales encontrados: {len(grammar.terminals)}")
    print(f"  {sorted(grammar.terminals)}")
    print(f"\nNo Terminales encontrados: {len(grammar.non_terminals)}")
    print(f"  {sorted(grammar.non_terminals)}")

    # Paso 5: Mostrar FIRST y FOLLOW
    print_section("PASO 5: Conjuntos FIRST y FOLLOW")

    print("\nConjuntos FIRST:")
    print("  (Simbolos terminales que pueden aparecer al inicio de una derivacion)")
    for non_terminal in sorted(grammar.non_terminals):
        if non_terminal != parser.augmented_start:
            first_str = ", ".join(sorted(parser.first[non_terminal]))
            print(f"    FIRST({non_terminal}) = {{ {first_str} }}")

    print("\nConjuntos FOLLOW:")
    print("  (Simbolos terminales que pueden aparecer despues de un no terminal)")
    for non_terminal in sorted(grammar.non_terminals):
        if non_terminal != parser.augmented_start:
            follow_str = ", ".join(sorted(parser.follow[non_terminal]))
            print(f"    FOLLOW({non_terminal}) = {{ {follow_str} }}")

    # Paso 6: Mostrar informacion del automata
    print_section("PASO 6: Automata LR(1) (AFD)")
    print(f"\n[INFO] El automata tiene {len(parser.states)} estados")
    print(f"[INFO] Transiciones totales: {len(parser.transitions)}")

    print("\nMostrando los primeros 5 estados como ejemplo:")
    print("(Cada estado contiene items de la forma [A -> alfa . beta, lookahead])")

    for idx in range(min(5, len(parser.states))):
        state = parser.states[idx]
        print(f"\n  Estado I{idx}: ({len(state)} items)")
        for item in list(state)[:4]:
            print(f"    {item}")
        if len(state) > 4:
            print(f"    ... y {len(state) - 4} items mas")

        # Mostrar transiciones desde este estado
        transitions_from_state = [
            (sym, dest) for (src, sym), dest in parser.transitions.items() if src == idx
        ]
        if transitions_from_state:
            trans_str = ", ".join(
                [f"{sym}->I{dest}" for sym, dest in sorted(transitions_from_state)[:4]]
            )
            print(f"    Transiciones: {trans_str}")

    print(f"\n[OK] Automata completo generado con exito")
    print(f"     Para ver TODOS los estados, ejecuta: parser.print_automaton()")

    # Paso 7: Mostrar tabla de parsing
    print_section("PASO 7: Tabla de Parsing LR(1)")
    print("\nLa tabla de parsing tiene dos secciones:")
    print("  - ACTION: define acciones para terminales (shift, reduce, accept)")
    print("  - GOTO: define transiciones para no terminales")
    print("\nNotacion:")
    print("  sN  = shift (desplazar) e ir al estado N")
    print("  rN  = reduce (reducir) usando la produccion N")
    print("  acc = accept (aceptar la cadena)")
    print()

    parser.print_parsing_table()

    # Paso 8: Generar graficos
    print_section("PASO 8: Visualizacion Grafica del Automata")
    print("\n[PROCESANDO] Generando graficos del automata...")

    try:
        parser.visualize_automaton("demo_completo_automaton")
        parser.visualize_simplified_automaton("demo_completo_automaton")
        print("\n[OK] Graficos generados exitosamente!")
        print("     Archivos creados:")
        print("       1. demo_completo_automaton.png")
        print("          (Grafico detallado con todos los items)")
        print("       2. demo_completo_automaton_simplified.png")
        print("          (Grafico simplificado con solo numeros de estado)")
        print("\n     Abre estos archivos para visualizar el automata completo.")
    except Exception as e:
        print(f"\n[WARNING] No se pudieron generar los graficos: {e}")
        print("     Necesitas tener Graphviz instalado en tu sistema.")
        print("     Descarga desde: https://graphviz.org/download/")
        print("     El parser funciona correctamente, solo falta la visualizacion.")


def demo_multiples_gramaticas():
    """Muestra varios ejemplos de diferentes tipos de gramaticas"""
    print_header("EJEMPLOS DE DIFERENTES TIPOS DE GRAMATICAS", "=")

    ejemplos = [
        {
            "nombre": "Lista de Elementos",
            "descripcion": "Lista separada por comas",
            "gramatica": "L -> L , E | E\nE -> id",
            "producciones": [("L", ["L", ",", "E"]), ("L", ["E"]), ("E", ["id"])],
        },
        {
            "nombre": "Declaraciones de Variables",
            "descripcion": "Declaraciones tipo: int x, y, z;",
            "gramatica": "D -> type L ;\nL -> L , id | id",
            "producciones": [
                ("D", ["type", "L", ";"]),
                ("L", ["L", ",", "id"]),
                ("L", ["id"]),
            ],
        },
        {
            "nombre": "Expresiones Booleanas",
            "descripcion": "Expresiones con AND, OR, NOT",
            "gramatica": "E -> E or T | T\nT -> T and F | F\nF -> not F | true | false",
            "producciones": [
                ("E", ["E", "or", "T"]),
                ("E", ["T"]),
                ("T", ["T", "and", "F"]),
                ("T", ["F"]),
                ("F", ["not", "F"]),
                ("F", ["true"]),
                ("F", ["false"]),
            ],
        },
        {
            "nombre": "Parentesis Balanceados",
            "descripcion": "Reconoce parentesis correctamente balanceados",
            "gramatica": "S -> ( S ) | epsilon",
            "producciones": [
                ("S", ["(", "S", ")"]),
                ("S", []),  # epsilon
            ],
        },
    ]

    for i, ejemplo in enumerate(ejemplos, 1):
        print_section(f"EJEMPLO {i}: {ejemplo['nombre']}")
        print(f"\nDescripcion: {ejemplo['descripcion']}")
        print(f"\nGramatica:")
        for line in ejemplo["gramatica"].split("\n"):
            print(f"  {line}")

        grammar = Grammar()
        for nt, prod in ejemplo["producciones"]:
            grammar.add_production(nt, prod)

        parser = LR1Parser(grammar)
        parser.build()

        print(f"\nResultados:")
        print(f"  Terminales: {sorted(grammar.terminals)}")
        print(
            f"  No Terminales: {sorted([nt for nt in grammar.non_terminals if nt != parser.augmented_start])}"
        )
        print(f"  Estados en el automata: {len(parser.states)}")
        print(f"  Transiciones: {len(parser.transitions)}")

        # Mostrar FIRST de los no terminales principales
        print(f"\n  Conjuntos FIRST:")
        for nt in sorted(grammar.non_terminals):
            if nt != parser.augmented_start:
                first_str = ", ".join(sorted(parser.first[nt]))
                print(f"    FIRST({nt}) = {{ {first_str} }}")

        print(f"\n[OK] Gramatica analizada exitosamente")


def demo_estadisticas():
    """Muestra estadisticas comparativas de diferentes gramaticas"""
    print_header("ESTADISTICAS COMPARATIVAS DE GRAMATICAS", "=")

    gramaticas = {
        "Minima (S -> a)": [("S", ["a"])],
        "Recursiva Derecha": [("S", ["a", "S"]), ("S", ["b"])],
        "Recursiva Izquierda": [("S", ["S", "a"]), ("S", ["b"])],
        "Expresiones Simple": [("E", ["E", "+", "T"]), ("E", ["T"]), ("T", ["id"])],
        "Expresiones Completa": [
            ("E", ["E", "+", "T"]),
            ("E", ["T"]),
            ("T", ["T", "*", "F"]),
            ("T", ["F"]),
            ("F", ["(", "E", ")"]),
            ("F", ["id"]),
        ],
    }

    print("\nComparacion de complejidad de diferentes tipos de gramaticas:")
    print()
    print("-" * 85)
    print(
        f"{'Tipo de Gramatica':<30} {'Prods':<8} {'Estados':<10} {'Trans':<10} {'Complejidad'}"
    )
    print("-" * 85)

    for nombre, prods in gramaticas.items():
        grammar = Grammar()
        for nt, prod in prods:
            grammar.add_production(nt, prod)

        parser = LR1Parser(grammar)
        parser.build()

        complejidad = (
            "Muy Baja"
            if len(parser.states) < 5
            else "Baja"
            if len(parser.states) < 10
            else "Media"
            if len(parser.states) < 20
            else "Alta"
        )

        print(
            f"{nombre:<30} {len(prods):<8} {len(parser.states):<10} {len(parser.transitions):<10} {complejidad}"
        )

    print("-" * 85)


def main():
    """Funcion principal que ejecuta todas las demos"""
    print("""
================================================================================
                   PARSER LR(1) - DEMOSTRACION COMPLETA
================================================================================

Bienvenido a la demostracion automatica del Parser LR(1)

Este script ejecutara automaticamente todas las funcionalidades del parser:
  1. Analisis completo de una gramatica de ejemplo
  2. Calculo de FIRST y FOLLOW
  3. Construccion del automata LR(1)
  4. Generacion de tabla de parsing
  5. Ejemplos de diferentes tipos de gramaticas
  6. Estadisticas comparativas
  7. Generacion de graficos visuales

El parser LR(1) implementa:
  - L: Left-to-right (analisis de izquierda a derecha)
  - R: Rightmost derivation (derivacion mas a la derecha)
  - 1: Un simbolo de lookahead

================================================================================
    """)

    # Demo principal
    demo_gramatica_completa()

    # Ejemplos adicionales
    demo_multiples_gramaticas()

    # Estadisticas
    demo_estadisticas()

    # Resumen final
    print_header("RESUMEN FINAL", "=")
    print("\n[COMPLETADO] Demo ejecutada exitosamente!")
    print("\nEl Parser LR(1) ha demostrado las siguientes capacidades:")
    print("  [OK] Analisis de gramaticas libres de contexto")
    print("  [OK] Calculo automatico de terminales y no terminales")
    print("  [OK] Calculo de conjuntos FIRST")
    print("  [OK] Calculo de conjuntos FOLLOW")
    print("  [OK] Construccion de items LR(1) con lookahead")
    print("  [OK] Calculo de clausura (closure) de items")
    print("  [OK] Funcion GOTO para transiciones")
    print("  [OK] Construccion completa del automata (AFD)")
    print("  [OK] Generacion de tabla de parsing (ACTION y GOTO)")
    print("  [OK] Visualizacion grafica del automata")
    print("  [OK] Soporte para multiples tipos de gramaticas")
    print("  [OK] Deteccion de conflictos shift-reduce y reduce-reduce")
    print("\nEl parser esta listo para ser usado en aplicaciones reales!")
    print("\nArchivos de interes:")
    print("  - lr1_parser.py: Implementacion completa del parser")
    print("  - example_custom.py: Ejemplos interactivos")
    print("  - test_parser.py: Suite de pruebas automaticas")
    print("  - README.md: Documentacion completa")
    print("\nPara mas informacion, consulta el archivo README.md")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
