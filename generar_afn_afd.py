"""
Script para generar los autómatas AFN y AFD del parser LR(1)
Usa la gramática: A -> A ( A ) | A -> epsilon
"""

import sys
sys.path.insert(0, '.')

from lr1_parser import Grammar, LR1Parser

print("=" * 80)
print("GENERACIÓN DE AUTÓMATAS LR(1): AFN Y AFD")
print("=" * 80)

# Gramática exacta del ejemplo
grammar = Grammar()
grammar.add_production("A", ["A", "(", "A", ")"])
grammar.add_production("A", [])  # epsilon

print("\n📝 Gramática:")
print("  A -> A ( A )")
print("  A -> ε")
print()

# Construir parser
parser = LR1Parser(grammar)
parser.build()

print(f"✓ Parser construido")
print(f"  Estados generados: {len(parser.states)}")
print(f"  Transiciones: {len(parser.transitions)}")
print()

# Generar AFD (solo items kernel agrupados)
print("🔹 Generando AFD (Autómata solo kernel)...")
parser.visualize_automaton("lr1_afd_ejemplo")

# Generar AFN (clausura completa - todos los items)
print("🔹 Generando AFN (Autómata con clausura completa)...")
parser.visualize_simplified_automaton("lr1_afn_ejemplo")

print()
print("=" * 80)
print("✅ ARCHIVOS GENERADOS:")
print("  • lr1_afd_ejemplo.png - AFD (solo kernel)")
print("  • lr1_afn_ejemplo_kernel.png - AFN (todos los items)")
print("=" * 80)
print()
print("💡 Compara estos gráficos con las imágenes que proporcionaste.")
print("   El AFD debe mostrar SOLO los items kernel agrupados.")
print("   El AFN debe mostrar TODOS los items individuales.")
