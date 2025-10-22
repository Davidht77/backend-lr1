# -*- coding: utf-8 -*-
"""
Demo Interactiva del Parser LR(1)
Muestra todas las capacidades del analizador sintactico LR(1)
"""

from lr1_parser import Grammar, LR1Parser


def parsear_gramatica_desde_texto(texto):
    """
    Parsea una gramática desde texto.
    
    Args:
        texto: String con las producciones, una por línea
               Formato: "S -> C C" o "S : C C"
    
    Returns:
        Grammar object o None si hay error
    
    Ejemplo:
        texto = '''
        S -> C C
        C -> c C
        C -> d
        '''
        grammar = parsear_gramatica_desde_texto(texto)
    """
    grammar = Grammar()
    lineas = texto.strip().split('\n')
    
    for i, linea in enumerate(lineas, 1):
        linea = linea.strip()
        
        # Saltar líneas vacías o comentarios
        if not linea or linea.startswith('#'):
            continue
        
        # Detectar separador
        separador = None
        if '->' in linea:
            separador = '->'
        elif ':' in linea:
            separador = ':'
        else:
            print(f"[ERROR] Línea {i}: Formato inválido: {linea}")
            print(f"        Use: 'NoTerminal -> producción' o 'NoTerminal : producción'")
            return None
        
        # Parsear
        partes = linea.split(separador, 1)
        if len(partes) != 2:
            print(f"[ERROR] Línea {i}: No se pudo parsear: {linea}")
            return None
        
        no_terminal = partes[0].strip()
        produccion_str = partes[1].strip()
        
        if not no_terminal:
            print(f"[ERROR] Línea {i}: No terminal vacío")
            return None
        
        # Procesar producción
        if not produccion_str or produccion_str.lower() == 'epsilon' or produccion_str == 'ε':
            produccion = []
        else:
            produccion = produccion_str.split()
        
        grammar.add_production(no_terminal, produccion)
    
    if len(grammar.productions) == 0:
        print("[ERROR] No se encontraron producciones válidas")
        return None
    
    return grammar


def crear_gramatica_personalizada():
    """Permite al usuario crear su propia gramática interactivamente"""
    print_header("CREAR GRAMÁTICA PERSONALIZADA")
    
    print("\nSelecciona el modo de entrada:")
    print("  1. Línea por línea (ingresar una producción a la vez)")
    print("  2. Pegar todo de una vez (copiar/pegar toda la gramática)")
    
    modo = input("\nElige una opción (1-2) [1]: ").strip() or "1"
    
    if modo == "2":
        return crear_gramatica_bloque()
    else:
        return crear_gramatica_linea_por_linea()


def crear_gramatica_bloque():
    """Permite pegar toda la gramática de una vez"""
    print_header("PEGAR GRAMÁTICA COMPLETA")
    
    print("\nFormatos aceptados:")
    print("  • E -> E + T       (formato tradicional con ->)")
    print("  • E : E + T        (formato alternativo con :)")
    print("  • S -> epsilon     (producción vacía)")
    print("\nEjemplo:")
    print("  S -> C C")
    print("  C -> c C")
    print("  C -> d")
    print()
    print("=" * 80)
    print("Pega tu gramática completa (presiona Enter dos veces para terminar):")
    print("=" * 80)
    
    lineas = []
    lineas_vacias = 0
    
    while True:
        entrada = input()
        
        if not entrada.strip():
            lineas_vacias += 1
            if lineas_vacias >= 2:  # Dos Enters consecutivos = terminar
                break
        else:
            lineas_vacias = 0
            lineas.append(entrada)
    
    if not lineas:
        print("\n[ERROR] No se ingresó ninguna gramática.")
        return None
    
    # Unir todas las líneas
    texto_completo = '\n'.join(lineas)
    
    print("\n" + "=" * 80)
    print("Gramática ingresada:")
    print("=" * 80)
    print(texto_completo)
    print("=" * 80)
    
    confirmar = input("\n¿Proceder con el análisis? (s/n) [s]: ").strip().lower() or 's'
    if confirmar != 's':
        print("[INFO] Gramática descartada.")
        return None
    
    # Parsear usando la función existente
    grammar = parsear_gramatica_desde_texto(texto_completo)
    
    if grammar:
        print(f"\n[OK] Se parsearon {len(grammar.productions)} producciones.")
        print("\nGramática creada:")
        print("-" * 80)
        for i, (nt, prod) in enumerate(grammar.productions):
            prod_str = ' '.join(prod) if prod else 'ε'
            print(f"  {i + 1}. {nt} → {prod_str}")
    
    return grammar


def crear_gramatica_linea_por_linea():
    """Permite ingresar la gramática línea por línea (modo original)"""
    print_header("INGRESAR GRAMÁTICA LÍNEA POR LÍNEA")
    
    print("\n¿Cómo funciona?")
    print("  1. Ingresa cada producción en formato estándar")
    print("  2. Repite para agregar más producciones")
    print("  3. Escribe 'fin' cuando termines")
    print("\nFormatos aceptados:")
    print("  • E -> E + T       (formato tradicional con ->)")
    print("  • E : E + T        (formato alternativo con :)")
    print("  • S -> epsilon     (producción vacía)")
    print("  • S ->             (producción vacía, sin 'epsilon')")
    print("\nEjemplos:")
    print("  S -> C C")
    print("  C -> c C")
    print("  C -> d")
    print()
    
    grammar = Grammar()
    produccion_count = 0
    
    print("=" * 80)
    print("Ingresa las producciones (escribe 'fin' para terminar):")
    print("=" * 80)
    
    while True:
        entrada = input(f"\nProducción {produccion_count + 1}: ").strip()
        
        if entrada.lower() == 'fin':
            if produccion_count == 0:
                print("\n[ERROR] Debes ingresar al menos una producción.")
                continue
            break
        
        if not entrada:
            print("[ERROR] Entrada vacía. Intenta de nuevo.")
            continue
        
        # Parsear la entrada - soportar -> o :
        separador = None
        if '->' in entrada:
            separador = '->'
        elif ':' in entrada:
            separador = ':'
        else:
            print("[ERROR] Formato inválido. Usa: 'NoTerminal -> producción' o 'NoTerminal : producción'")
            print("        Ejemplo: S -> C C  o  S : C C")
            continue
        
        partes = entrada.split(separador, 1)
        no_terminal = partes[0].strip()
        produccion_str = partes[1].strip() if len(partes) > 1 else ""
        
        if not no_terminal:
            print("[ERROR] El no terminal no puede estar vacío.")
            continue
        
        # Procesar la producción
        if not produccion_str or produccion_str.lower() == 'epsilon' or produccion_str == 'ε':
            # Producción epsilon
            produccion = []
        else:
            # Dividir por espacios
            produccion = produccion_str.split()
        
        # Agregar la producción
        grammar.add_production(no_terminal, produccion)
        produccion_count += 1
        
        prod_display = ' '.join(produccion) if produccion else 'ε'
        print(f"  ✓ Agregada: {no_terminal} → {prod_display}")
    
    if produccion_count > 0:
        print(f"\n[OK] Se agregaron {produccion_count} producciones.")
        print("\nGramática creada:")
        print("-" * 80)
        
        # Mostrar la gramática creada
        for i, (nt, prod) in enumerate(grammar.productions):
            prod_str = ' '.join(prod) if prod else 'ε'
            print(f"  {i + 1}. {nt} → {prod_str}")
        
        return grammar
    else:
        return None


def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def print_section(title):
    """Imprime una seccion"""
    print("\n" + "-" * 80)
    print(f" {title}")
    print("-" * 80)


def demo_paso_a_paso():
    """Demo paso a paso mostrando cada componente del parser"""
    print_header("DEMO PASO A PASO: PARSER LR(1)")

    print("\nEste demo muestra como el parser LR(1) analiza una gramatica completa.")
    print("Usaremos la gramatica clasica de expresiones aritmeticas:")
    print()
    print("  E -> E + T | T")
    print("  T -> T * F | F")
    print("  F -> ( E ) | id")
    print()
    print("Esta gramatica permite expresiones como: id + id * id, (id + id), etc.")

    input("\nPresiona Enter para continuar...")

    # Paso 1: Crear la gramatica
    print_section("PASO 1: Definir la Gramatica")
    print("\nCreando la gramatica con Grammar()...")

    grammar = Grammar()
    grammar.add_production("E", ["E", "+", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["T", "*", "F"])
    grammar.add_production("T", ["F"])
    grammar.add_production("F", ["(", "E", ")"])
    grammar.add_production("F", ["id"])

    print("Producciones anadidas:")
    print("  1. E -> E + T")
    print("  2. E -> T")
    print("  3. T -> T * F")
    print("  4. T -> F")
    print("  5. F -> ( E )")
    print("  6. F -> id")

    input("\nPresiona Enter para continuar...")

    # Paso 2: Crear el parser
    print_section("PASO 2: Crear el Parser LR(1)")
    print("\nCreando el parser y construyendo el automata...")

    parser = LR1Parser(grammar)
    parser.build()

    print("[OK] Parser construido exitosamente!")
    print("\nEl parser ha calculado automaticamente:")
    print("  - Terminales y No Terminales")
    print("  - Conjuntos FIRST")
    print("  - Conjuntos FOLLOW")
    print("  - Automata LR(1) (AFD)")
    print("  - Tabla de Parsing (ACTION y GOTO)")

    input("\nPresiona Enter para ver los terminales y no terminales...")

    # Paso 3: Mostrar terminales y no terminales
    print_section("PASO 3: Terminales y No Terminales")

    print("\nTerminales (simbolos de la entrada):")
    print(f"  {sorted(grammar.terminals)}")

    print("\nNo Terminales (simbolos derivables):")
    print(f"  {sorted(grammar.non_terminals)}")

    input("\nPresiona Enter para ver los conjuntos FIRST...")

    # Paso 4: Mostrar FIRST
    print_section("PASO 4: Conjuntos FIRST")
    print("\nFIRST(X) = conjunto de terminales que pueden aparecer al inicio")
    print("           de cualquier cadena derivada de X")
    print()

    for non_terminal in sorted(grammar.non_terminals):
        if non_terminal != parser.augmented_start:
            first_str = ", ".join(sorted(parser.first[non_terminal]))
            print(f"  FIRST({non_terminal}) = {{ {first_str} }}")

    input("\nPresiona Enter para ver los conjuntos FOLLOW...")

    # Paso 5: Mostrar FOLLOW
    print_section("PASO 5: Conjuntos FOLLOW")
    print("\nFOLLOW(X) = conjunto de terminales que pueden aparecer inmediatamente")
    print("            despues de X en alguna forma sentencial")
    print()

    for non_terminal in sorted(grammar.non_terminals):
        if non_terminal != parser.augmented_start:
            follow_str = ", ".join(sorted(parser.follow[non_terminal]))
            print(f"  FOLLOW({non_terminal}) = {{ {follow_str} }}")

    input("\nPresiona Enter para ver el automata LR(1)...")

    # Paso 6: Mostrar automata (solo primeros estados)
    print_section("PASO 6: Automata LR(1) (Estados e Items)")
    print("\nEl automata tiene", len(parser.states), "estados.")
    print("Cada estado contiene items LR(1) de la forma: [A -> alfa . beta, a]")
    print("\nMostrando los primeros 3 estados como ejemplo:")

    for idx in range(min(3, len(parser.states))):
        state = parser.states[idx]
        print(f"\nEstado I{idx}:")
        for item in list(state)[:5]:  # Mostrar solo 5 items por estado
            print(f"  {item}")
        if len(state) > 5:
            print(f"  ... ({len(state) - 5} items mas)")

    print("\n(Para ver todos los estados, ejecuta parser.print_automaton())")

    input("\nPresiona Enter para ver la tabla de parsing...")

    # Paso 7: Mostrar tabla de parsing (resumida)
    print_section("PASO 7: Tabla de Parsing LR(1)")
    print("\nLa tabla tiene dos partes:")
    print("  - ACTION: que hacer cuando se lee un terminal (shift/reduce/accept)")
    print("  - GOTO: a que estado ir despues de reducir a un no terminal")
    print()
    print("Ejemplo de entradas en la tabla:")
    print("  s5  = shift (desplazar) e ir al estado 5")
    print("  r3  = reduce (reducir) usando la produccion 3")
    print("  acc = accept (aceptar la entrada)")
    print()

    # Mostrar primeras filas de la tabla
    terminals = sorted(grammar.terminals - {grammar.epsilon})[:4]
    print(f"Primeras columnas de ACTION: {terminals}")
    print()

    for state_idx in range(min(5, len(parser.states))):
        row = f"Estado {state_idx}: "
        for term in terminals:
            if (
                state_idx in parser.parsing_table["action"]
                and term in parser.parsing_table["action"][state_idx]
            ):
                action_type, value = parser.parsing_table["action"][state_idx][term]
                if action_type == "shift":
                    cell = f"s{value}"
                elif action_type == "reduce":
                    cell = f"r{value}"
                elif action_type == "accept":
                    cell = "acc"
                else:
                    cell = ""
            else:
                cell = ""
            row += f"{cell:<8} "
        print(row)

    print("\n(Para ver la tabla completa, ejecuta parser.print_parsing_table())")

    input("\nPresiona Enter para generar graficos...")

    # Paso 8: Generar graficos
    print_section("PASO 8: Visualizacion Grafica")
    print("\nGenerando graficos del automata...")

    try:
        parser.visualize_automaton("demo_automaton")
        parser.visualize_simplified_automaton("demo_automaton")
        print("\n[OK] Graficos generados:")
        print("  - demo_automaton.png (detallado con items)")
        print("  - demo_automaton_simplified.png (simplificado)")
    except Exception as e:
        print(f"\n[WARNING] No se pudieron generar graficos: {e}")
        print("  Instala Graphviz para habilitar esta funcionalidad")

    input("\nPresiona Enter para continuar...")

    print_header("RESUMEN")
    print("\nEl Parser LR(1) ha procesado exitosamente la gramatica!")
    print("\nComponentes generados:")
    print("  [OK] Gramatica aumentada con simbolo inicial S'")
    print("  [OK] Conjuntos FIRST y FOLLOW calculados")
    print(f"  [OK] Automata con {len(parser.states)} estados")
    print("  [OK] Tabla de parsing completa (ACTION y GOTO)")
    print("  [OK] Graficos del automata (si Graphviz esta disponible)")
    print("\nEl parser esta listo para analizar cadenas de entrada!")


def demo_ejemplos_rapidos():
    """Muestra varios ejemplos rapidos de diferentes gramaticas"""
    print_header("EJEMPLOS RAPIDOS DE DIFERENTES GRAMATICAS")

    ejemplos = [
        {
            "nombre": "Lista de elementos",
            "descripcion": "L -> L , E | E\n            E -> id",
            "producciones": [("L", ["L", ",", "E"]), ("L", ["E"]), ("E", ["id"])],
        },
        {
            "nombre": "Declaraciones",
            "descripcion": "D -> type L ;\n            L -> L , id | id",
            "producciones": [
                ("D", ["type", "L", ";"]),
                ("L", ["L", ",", "id"]),
                ("L", ["id"]),
            ],
        },
        {
            "nombre": "Parentesis balanceados",
            "descripcion": "S -> ( S ) | epsilon",
            "producciones": [("S", ["(", "S", ")"]), ("S", [])],
        },
    ]

    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n{i}. {ejemplo['nombre']}")
        print("-" * 40)
        print(f"Gramatica:\n  {ejemplo['descripcion']}")

        grammar = Grammar()
        for nt, prod in ejemplo["producciones"]:
            grammar.add_production(nt, prod)

        parser = LR1Parser(grammar)
        parser.build()

        print(f"\nResultado:")
        print(f"  - Terminales: {sorted(grammar.terminals)}")
        print(
            f"  - No Terminales: {sorted(grammar.non_terminals - {parser.augmented_start})}"
        )
        print(f"  - Estados en el automata: {len(parser.states)}")

        # Mostrar un estado de ejemplo
        if len(parser.states) > 1:
            print(f"\n  Estado inicial (I0):")
            for item in list(parser.states[0])[:3]:
                print(f"    {item}")
            if len(parser.states[0]) > 3:
                print(f"    ... ({len(parser.states[0]) - 3} items mas)")


def demo_comparacion_gramaticas():
    """Compara diferentes tipos de gramaticas"""
    print_header("COMPARACION DE GRAMATICAS")

    print("\nComparemos como diferentes gramaticas generan diferentes automatas:")

    gramaticas = {
        "Simple": [("S", ["a"])],
        "Recursiva Derecha": [("S", ["a", "S"]), ("S", ["b"])],
        "Recursiva Izquierda": [("S", ["S", "a"]), ("S", ["b"])],
        "Ambigua": [("E", ["E", "+", "E"]), ("E", ["id"])],
    }

    print("\n" + "-" * 80)
    print(f"{'Tipo':<25} {'Producciones':<15} {'Estados':<12} {'Complejidad'}")
    print("-" * 80)

    for nombre, prods in gramaticas.items():
        grammar = Grammar()
        for nt, prod in prods:
            grammar.add_production(nt, prod)

        parser = LR1Parser(grammar)
        parser.build()

        complejidad = (
            "Baja"
            if len(parser.states) < 5
            else "Media"
            if len(parser.states) < 10
            else "Alta"
        )

        print(f"{nombre:<25} {len(prods):<15} {len(parser.states):<12} {complejidad}")

    print("-" * 80)
    print("\nObservaciones:")
    print("  - Gramaticas simples generan pocos estados")
    print("  - Recursion (izquierda o derecha) aumenta el numero de estados")
    print("  - Gramaticas ambiguas pueden generar conflictos")


def demo_interactivo():
    """Menu interactivo para explorar diferentes gramaticas"""
    print_header("PARSER LR(1) - DEMO COMPLETA")

    gramaticas = {
        "1": {
            "nombre": "Expresiones Aritmeticas",
            "descripcion": "Gramatica clasica para expresiones con + y *",
            "producciones": [
                ("E", ["E", "+", "T"]),
                ("E", ["T"]),
                ("T", ["T", "*", "F"]),
                ("T", ["F"]),
                ("F", ["(", "E", ")"]),
                ("F", ["id"])
            ]
        },
        "2": {
            "nombre": "Lista de elementos",
            "descripcion": "Gramatica para listas separadas por comas",
            "producciones": [
                ("L", ["L", ",", "E"]),
                ("L", ["E"]),
                ("E", ["id"])
            ]
        },
        "3": {
            "nombre": "Declaraciones",
            "descripcion": "Gramatica para declaraciones de variables",
            "producciones": [
                ("D", ["type", "L", ";"]),
                ("L", ["L", ",", "id"]),
                ("L", ["id"])
            ]
        },
        "4": {
            "nombre": "Parentesis balanceados",
            "descripcion": "Gramatica para validar parentesis balanceados",
            "producciones": [
                ("S", ["(", "S", ")"]),
                ("S", [])
            ]
        },
        "5": {
            "nombre": "Expresiones booleanas",
            "descripcion": "Gramatica para expresiones con AND y OR",
            "producciones": [
                ("E", ["E", "or", "T"]),
                ("E", ["T"]),
                ("T", ["T", "and", "F"]),
                ("T", ["F"]),
                ("F", ["not", "F"]),
                ("F", ["(", "E", ")"]),
                ("F", ["true"]),
                ("F", ["false"])
            ]
        },
        "6": {
            "nombre": "Asignaciones",
            "descripcion": "Gramatica para statements de asignacion",
            "producciones": [
                ("S", ["id", "=", "E"]),
                ("E", ["E", "+", "T"]),
                ("E", ["T"]),
                ("T", ["id"]),
                ("T", ["num"])
            ]
        }
    }

    while True:
        print("\n" + "=" * 80)
        print("MENU PRINCIPAL - SELECCIONA UNA GRAMATICA")
        print("=" * 80)
        
        for key, info in gramaticas.items():
            print(f"\n{key}. {info['nombre']}")
            print(f"   {info['descripcion']}")
        
        print(f"\n7. Crear tu propia gramática")
        print(f"   Ingresa una gramática personalizada de forma interactiva")
        
        print(f"\n8. Salir")

        opcion = input(f"\nSelecciona una opcion (1-8): ").strip()

        if opcion == "7":
            # Crear gramática personalizada
            grammar = crear_gramatica_personalizada()
            
            if grammar is None:
                print("\n[ERROR] No se pudo crear la gramática.")
                continue
            
            print_section("Análisis de Gramática Personalizada")
            
            # Confirmar antes de procesar
            confirmar = input("\n¿Proceder con el análisis? (s/n): ").strip().lower()
            if confirmar != 's':
                print("[INFO] Análisis cancelado.")
                continue
            
            try:
                parser = LR1Parser(grammar)
                parser.build()

                grammar.print_grammar()
                grammar.print_sets(parser.first, parser.follow)
                parser.print_parsing_table()
                parser.print_closure_table()
                
                # Generar gráficos
                print("\nGenerando gráficos del autómata...")
                filename = "automaton_personalizada"
                graficos_generados = []
                
                # Intentar generar autómata completo
                try:
                    print(f"  [+] Generando autómata completo...")
                    parser.visualize_automaton(filename)
                    graficos_generados.append(f"{filename}.png (detallado con reglas)")
                    print(f"      ✓ {filename}.png creado")
                except Exception as e:
                    print(f"      ✗ Error: {e}")
                
                # Intentar generar autómata simplificado
                try:
                    print(f"  [+] Generando autómata simplificado...")
                    parser.visualize_simplified_automaton(filename)
                    graficos_generados.append(f"{filename}_simplified.png (solo kernel)")
                    print(f"      ✓ {filename}_simplified.png creado")
                except Exception as e:
                    print(f"      ✗ Error: {e}")
                
                if graficos_generados:
                    print(f"\n[OK] Gráficos generados:")
                    for g in graficos_generados:
                        print(f"  - {g}")
                else:
                    print(f"\n[WARNING] No se pudieron generar gráficos.")
                    print("  Verifica que Graphviz esté instalado correctamente.")

                input("\nPresiona Enter para continuar...")
            except Exception as e:
                print(f"\n[ERROR] Error al construir el parser: {e}")
                print("Verifica que la gramática sea válida.")
                input("\nPresiona Enter para continuar...")
        
        elif opcion in gramaticas:
            gram_info = gramaticas[opcion]
            print_section(f"Analisis: {gram_info['nombre']}")
            print(f"\n{gram_info['descripcion']}")
            
            grammar = Grammar()
            for nt, prod in gram_info["producciones"]:
                grammar.add_production(nt, prod)

            parser = LR1Parser(grammar)
            parser.build()

            print("\nProducciones:")
            for i, (nt, prod) in enumerate(grammar.productions):
                prod_str = " ".join(prod) if prod else "epsilon"
                print(f"  {i}. {nt} -> {prod_str}")

            grammar.print_grammar()
            grammar.print_sets(parser.first, parser.follow)
            parser.print_parsing_table()
            
            # Generar graficos
            print("\nGenerando graficos del automata...")
            try:
                filename = f"automaton_{gram_info['nombre'].lower().replace(' ', '_')}"
                parser.visualize_automaton(filename)
                parser.visualize_simplified_automaton(filename)
                print(f"\n[OK] Graficos generados:")
                print(f"  - {filename}.png (detallado con reglas)")
                print(f"  - {filename}_simplified.png (simplificado)")
            except Exception as e:
                print(f"\n[WARNING] No se pudieron generar graficos: {e}")
                print("  Instala Graphviz para habilitar esta funcionalidad")

            input("\nPresiona Enter para continuar...")
        elif opcion == "8":
            print("\n" + "=" * 80)
            print("Gracias por usar el Parser LR(1)!")
            print("=" * 80)
            break
        else:
            print("\n[ERROR] Opcion invalida. Intenta de nuevo.")


def main():
    """Funcion principal"""
    print("""
    ========================================================================
                        PARSER LR(1) - DEMO INTERACTIVA
    ========================================================================

    Bienvenido a la demo del Parser LR(1)!

    Este parser implementa analisis sintactico ascendente LR(1):
      - L: Left-to-right (lee entrada de izquierda a derecha)
      - R: Rightmost derivation (derivacion por la derecha)
      - 1: Un simbolo de lookahead

    Caracteristicas:
      * Calculo automatico de FIRST y FOLLOW
      * Construccion del automata LR(1) (AFD)
      * Generacion de tabla de parsing
      * Visualizacion grafica del automata
      * Deteccion de conflictos

    ========================================================================
    """)

    input("Presiona Enter para comenzar...")

    demo_interactivo()


if __name__ == "__main__":
    main()
