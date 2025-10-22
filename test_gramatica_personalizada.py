# -*- coding: utf-8 -*-
"""
Script de prueba para la funcionalidad de gramática personalizada
"""

from lr1_parser import Grammar, LR1Parser

print("=" * 80)
print("PRUEBA: Creación de gramática personalizada programáticamente")
print("=" * 80)

# Simular la creación de una gramática simple
grammar = Grammar()

# Gramática: S -> a S b | epsilon
grammar.add_production("S", ["a", "S", "b"])
grammar.add_production("S", [])  # epsilon

print("\n✓ Gramática creada:")
print("  S -> a S b")
print("  S -> ε")

# Construir parser
print("\n✓ Construyendo parser...")
parser = LR1Parser(grammar)
parser.build()

print("\n✓ Parser construido exitosamente")

# Mostrar información
grammar.print_grammar()
grammar.print_sets(parser.first, parser.follow)

print("\n" + "=" * 80)
print("[OK] Prueba completada exitosamente")
print("=" * 80)
print("\nLa funcionalidad de gramática personalizada está lista para usar.")
print("Ejecuta 'python demo.py' y selecciona la opción 7.")
