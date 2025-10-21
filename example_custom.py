# -*- coding: utf-8 -*-
"""
Ejemplo de uso del Parser LR(1) con gramáticas personalizadas
Este archivo muestra cómo crear y usar gramáticas propias
"""

from lr1_parser import Grammar, LR1Parser


def ejemplo_1_declaraciones():
    """
    Gramática para declaraciones simples de variables
    S → type id ;
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Declaraciones de Variables")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("S", ["type", "id", ";"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_automaton()
    parser.print_parsing_table()


def ejemplo_2_asignaciones():
    """
    Gramática para asignaciones
    S → id = E
    E → E + E | id | num
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Asignaciones con Expresiones")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("S", ["id", "=", "E"])
    grammar.add_production("E", ["E", "+", "E"])
    grammar.add_production("E", ["id"])
    grammar.add_production("E", ["num"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()


def ejemplo_3_if_statement():
    """
    Gramática para sentencias if
    S → if ( E ) B
    E → id | num
    B → { S } | S
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Sentencias IF")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("S", ["if", "(", "E", ")", "B"])
    grammar.add_production("E", ["id"])
    grammar.add_production("E", ["num"])
    grammar.add_production("B", ["{", "S", "}"])
    grammar.add_production("B", ["S"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_automaton()


def ejemplo_4_listas():
    """
    Gramática para listas
    L → L , E | E
    E → id | num
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Listas de Elementos")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("L", ["L", ",", "E"])
    grammar.add_production("L", ["E"])
    grammar.add_production("E", ["id"])
    grammar.add_production("E", ["num"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()


def ejemplo_5_parentesis_balanceados():
    """
    Gramática para paréntesis balanceados
    S → ( S ) | S S | ε
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Paréntesis Balanceados")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("S", ["(", "S", ")"])
    grammar.add_production("S", ["S", "S"])
    grammar.add_production("S", [])  # Producción epsilon

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_automaton()


def ejemplo_6_expresiones_booleanas():
    """
    Gramática para expresiones booleanas
    E → E and T | E or T | T
    T → not T | ( E ) | true | false | id
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 6: Expresiones Booleanas")
    print("=" * 70)

    grammar = Grammar()
    grammar.add_production("E", ["E", "and", "T"])
    grammar.add_production("E", ["E", "or", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["not", "T"])
    grammar.add_production("T", ["(", "E", ")"])
    grammar.add_production("T", ["true"])
    grammar.add_production("T", ["false"])
    grammar.add_production("T", ["id"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()


def ejemplo_7_json_simple():
    """
    Gramática simplificada para JSON
    J → { P } | [ A ]
    P → S : V | P , S : V
    A → V | A , V
    V → S | N | J
    S → string
    N → number
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 7: JSON Simplificado")
    print("=" * 70)

    grammar = Grammar()
    # Objeto
    grammar.add_production("J", ["{", "P", "}"])
    grammar.add_production("J", ["[", "A", "]"])

    # Pares clave-valor
    grammar.add_production("P", ["S", ":", "V"])
    grammar.add_production("P", ["P", ",", "S", ":", "V"])

    # Array
    grammar.add_production("A", ["V"])
    grammar.add_production("A", ["A", ",", "V"])

    # Valores
    grammar.add_production("V", ["S"])
    grammar.add_production("V", ["N"])
    grammar.add_production("V", ["J"])

    # Primitivos
    grammar.add_production("S", ["string"])
    grammar.add_production("N", ["number"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()


def ejemplo_8_calculadora():
    """
    Gramática completa para calculadora con precedencia
    E → E + T | E - T | T
    T → T * F | T / F | F
    F → F ^ P | P
    P → ( E ) | - P | num
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 8: Calculadora con Precedencia y Potencia")
    print("=" * 70)

    grammar = Grammar()
    # Expresiones (menor precedencia)
    grammar.add_production("E", ["E", "+", "T"])
    grammar.add_production("E", ["E", "-", "T"])
    grammar.add_production("E", ["T"])

    # Términos
    grammar.add_production("T", ["T", "*", "F"])
    grammar.add_production("T", ["T", "/", "F"])
    grammar.add_production("T", ["F"])

    # Factores
    grammar.add_production("F", ["F", "^", "P"])
    grammar.add_production("F", ["P"])

    # Primarios (mayor precedencia)
    grammar.add_production("P", ["(", "E", ")"])
    grammar.add_production("P", ["-", "P"])
    grammar.add_production("P", ["num"])

    parser = LR1Parser(grammar)
    parser.build()

    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_parsing_table()

    # Generar gráficos
    parser.visualize_automaton("calculadora_automaton")
    parser.visualize_simplified_automaton("calculadora_automaton")


def menu_interactivo():
    """Menú interactivo para seleccionar ejemplos"""
    ejemplos = {
        "1": ("Declaraciones de Variables", ejemplo_1_declaraciones),
        "2": ("Asignaciones con Expresiones", ejemplo_2_asignaciones),
        "3": ("Sentencias IF", ejemplo_3_if_statement),
        "4": ("Listas de Elementos", ejemplo_4_listas),
        "5": ("Paréntesis Balanceados", ejemplo_5_parentesis_balanceados),
        "6": ("Expresiones Booleanas", ejemplo_6_expresiones_booleanas),
        "7": ("JSON Simplificado", ejemplo_7_json_simple),
        "8": ("Calculadora Completa", ejemplo_8_calculadora),
        "9": ("Todos los ejemplos", None),
    }

    print("\n" + "=" * 70)
    print(" EJEMPLOS DE GRAMÁTICAS PERSONALIZADAS - PARSER LR(1)")
    print("=" * 70)
    print("\nSeleccione un ejemplo:")

    for key, (nombre, _) in ejemplos.items():
        print(f"{key}. {nombre}")

    seleccion = input("\nIngrese su opción (1-9) [8]: ").strip() or "8"

    if seleccion == "9":
        # Ejecutar todos los ejemplos
        for key, (nombre, funcion) in ejemplos.items():
            if key != "9" and funcion:
                try:
                    funcion()
                except Exception as e:
                    print(f"\n[WARNING] Error en ejemplo {key}: {e}")
    elif seleccion in ejemplos:
        nombre, funcion = ejemplos[seleccion]
        if funcion:
            try:
                funcion()
                print("\n" + "=" * 70)
                print(f"[OK] Ejemplo '{nombre}' completado exitosamente")
                print("=" * 70)
            except Exception as e:
                print(f"\n[WARNING] Error: {e}")
    else:
        print("\n[WARNING] Opcion invalida. Ejecutando ejemplo 8...")
        ejemplo_8_calculadora()


def crear_gramatica_desde_texto():
    """
    Función para crear una gramática interactivamente
    """
    print("\n" + "=" * 70)
    print(" CREAR GRAMÁTICA PERSONALIZADA")
    print("=" * 70)
    print("\nFormato de entrada:")
    print("  - Una producción por línea")
    print("  - Formato: NoTerminal -> simbolo1 simbolo2 ...")
    print("  - Para epsilon (producción vacía), usa: NoTerminal -> epsilon")
    print("  - Escribe 'FIN' para terminar")
    print("\nEjemplo:")
    print("  E -> E + T")
    print("  E -> T")
    print("  T -> id")
    print("  FIN")

    grammar = Grammar()

    print("\nIngresa las producciones:")
    while True:
        linea = input("> ").strip()

        if linea.upper() == "FIN":
            break

        if "->" not in linea:
            print("[WARNING] Formato incorrecto. Usa: NoTerminal -> produccion")
            continue

        partes = linea.split("->")
        if len(partes) != 2:
            print("[WARNING] Formato incorrecto.")
            continue

        no_terminal = partes[0].strip()
        produccion_str = partes[1].strip()

        if (
            produccion_str.lower() == "epsilon"
            or produccion_str == "ε"
            or not produccion_str
        ):
            produccion = []
        else:
            produccion = produccion_str.split()

        grammar.add_production(no_terminal, produccion)
        print(
            f"[OK] Anadida: {no_terminal} -> {' '.join(produccion) if produccion else 'epsilon'}"
        )

    if not grammar.productions:
        print("\n[WARNING] No se ingresaron producciones.")
        return

    # Construir parser
    print("\n[...] Construyendo parser LR(1)...")
    parser = LR1Parser(grammar)
    parser.build()

    # Mostrar resultados
    grammar.print_grammar()
    grammar.print_sets(parser.first, parser.follow)
    parser.print_automaton()
    parser.print_parsing_table()

    # Preguntar si generar gráficos
    generar = (
        input("\nGenerar graficos del automata? (s/n) [s]: ").strip().lower() or "s"
    )
    if generar == "s":
        parser.visualize_automaton("custom_automaton")
        parser.visualize_simplified_automaton("custom_automaton")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print(" PARSER LR(1) - EJEMPLOS PERSONALIZADOS")
    print("=" * 70)
    print("\nQue deseas hacer?")
    print("1. Ver ejemplos predefinidos")
    print("2. Crear tu propia gramatica")

    opcion = input("\nOpcion (1-2) [1]: ").strip() or "1"

    if opcion == "2":
        crear_gramatica_desde_texto()
    else:
        menu_interactivo()

    print("\n" + "=" * 70)
    print("Gracias por usar el Parser LR(1)!")
    print("=" * 70)


if __name__ == "__main__":
    main()
