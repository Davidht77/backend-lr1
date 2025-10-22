# -*- coding: utf-8 -*-
"""
Ejemplos de Uso - Parser LR(1) Modular
Muestra cómo usar la nueva estructura modular
"""

# ============================================================================
# EJEMPLO 1: Uso básico completo
# ============================================================================

from lr1_parser import Grammar, LR1Parser

# Crear gramática
grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])
grammar.add_production("T", ["id"])

# Crear y construir parser
parser = LR1Parser(grammar)
parser.build()

# Mostrar resultados
grammar.print_grammar()
parser.print_parsing_table()


# ============================================================================
# EJEMPLO 2: Usar gramáticas predefinidas
# ============================================================================

from lr1_parser import create_example_grammar_1, LR1Parser

# Obtener gramática de ejemplo
grammar = create_example_grammar_1()

# Crear parser
parser = LR1Parser(grammar)
parser.build()

# Generar visualización
parser.visualize_automaton("mi_automata_completo")
parser.visualize_simplified_automaton("mi_automata_kernel")


# ============================================================================
# EJEMPLO 3: Importación selectiva (solo lo que necesitas)
# ============================================================================

# Opción A: Importar clases específicas
from lr1_parser import Grammar, LR1Parser

# Opción B: Importar todo
from lr1_parser import *

# Opción C: Importar solo ejemplos
from lr1_parser.examples import create_example_grammar_2


# ============================================================================
# EJEMPLO 4: Análisis detallado de gramática
# ============================================================================

from lr1_parser import Grammar, LR1Parser

# Crear gramática
grammar = Grammar()
grammar.add_production("S", ["S", "+", "A"])
grammar.add_production("S", ["A"])
grammar.add_production("A", ["(", "S", ")"])
grammar.add_production("A", ["a"])

# Construir parser
parser = LR1Parser(grammar)
parser.build()

# Mostrar toda la información
grammar.print_grammar()
grammar.print_sets(parser.first, parser.follow)
parser.print_automaton()
parser.print_parsing_table()
parser.print_closure_table()


# ============================================================================
# EJEMPLO 5: Trabajar con items LR(1) directamente
# ============================================================================

from lr1_parser import LR1Item

# Crear item: [E → E · + T, $]
item = LR1Item("E", ["E", "+", "T"], 1, "$")

print(f"Item: {item}")
print(f"Siguiente símbolo: {item.next_symbol()}")

# Avanzar el punto
new_item = item.advance()
print(f"Item avanzado: {new_item}")


# ============================================================================
# EJEMPLO 6: Visualización de autómatas regulares
# ============================================================================

from lr1_parser import Grammar, RegularGrammarAFNVisualizer

# Crear gramática regular
grammar = Grammar()
grammar.add_production("S", ["a", "S"])
grammar.add_production("S", ["b", "T"])
grammar.add_production("T", ["a"])

# Crear visualizador
visualizer = RegularGrammarAFNVisualizer(grammar)

# Generar visualizaciones
visualizer.print_automaton_info()
visualizer.visualize_afn("afn_ejemplo")
visualizer.visualize_afd("afd_ejemplo")


# ============================================================================
# EJEMPLO 7: Acceso a componentes internos del parser
# ============================================================================

from lr1_parser import Grammar, LR1Parser

grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])
grammar.add_production("T", ["id"])

parser = LR1Parser(grammar)
parser.build()

# Acceder a estados
print(f"Número de estados: {len(parser.states)}")

# Acceder a transiciones
print(f"Transiciones: {parser.transitions}")

# Acceder a tabla de parsing
print(f"Tabla ACTION: {parser.parsing_table['action']}")
print(f"Tabla GOTO: {parser.parsing_table['goto']}")

# Acceder a FIRST y FOLLOW
print(f"FIRST: {parser.first}")
print(f"FOLLOW: {parser.follow}")


# ============================================================================
# EJEMPLO 8: Crear gramática compleja paso a paso
# ============================================================================

from lr1_parser import Grammar, LR1Parser

# Gramática para expresiones booleanas
grammar = Grammar()

# Reglas para expresiones
grammar.add_production("E", ["E", "or", "T"])
grammar.add_production("E", ["T"])

# Reglas para términos
grammar.add_production("T", ["T", "and", "F"])
grammar.add_production("T", ["F"])

# Reglas para factores
grammar.add_production("F", ["not", "F"])
grammar.add_production("F", ["(", "E", ")"])
grammar.add_production("F", ["true"])
grammar.add_production("F", ["false"])

# Construir y analizar
parser = LR1Parser(grammar)
parser.build()

# Generar salida completa
grammar.print_grammar()
parser.print_parsing_table()
parser.visualize_automaton("boolean_expression")


# ============================================================================
# EJEMPLO 9: Múltiples gramáticas en un programa
# ============================================================================

from lr1_parser import (
    create_example_grammar_1,
    create_example_grammar_2,
    create_example_grammar_3,
    LR1Parser,
)

# Analizar múltiples gramáticas
grammars = [
    ("Aritmética", create_example_grammar_1()),
    ("Ejemplo 2", create_example_grammar_2()),
    ("Recursiva", create_example_grammar_3()),
]

for name, grammar in grammars:
    print(f"\n{'='*60}")
    print(f"Analizando: {name}")
    print(f"{'='*60}")
    
    parser = LR1Parser(grammar)
    parser.build()
    
    grammar.print_grammar()
    parser.visualize_automaton(f"automaton_{name.lower()}")


# ============================================================================
# EJEMPLO 10: Verificar conflictos en la gramática
# ============================================================================

from lr1_parser import Grammar, LR1Parser

# Gramática con posibles conflictos
grammar = Grammar()
grammar.add_production("S", ["a", "A"])
grammar.add_production("S", ["b", "B"])
grammar.add_production("A", ["c"])
grammar.add_production("B", ["c"])

parser = LR1Parser(grammar)
parser.build()

# Los conflictos se mostrarán automáticamente durante build()
# Revisa la tabla de parsing para identificar conflictos shift/reduce o reduce/reduce

parser.print_parsing_table()


# ============================================================================
# NOTAS:
# ============================================================================
# 
# 1. Todos los ejemplos anteriores funcionan con la estructura modular
# 2. La importación es más flexible y específica
# 3. Cada módulo puede usarse independientemente
# 4. La documentación está en cada clase y método
# 5. Para más detalles, ver ESTRUCTURA.md y RESUMEN_MODULARIZACION.md
#
# ============================================================================
