# -*- coding: utf-8 -*-
"""
Comparación: Tabla LR(1) de la imagen vs generada por el programa
"""

from lr1_parser import Grammar, LR1Parser

print("=" * 80)
print("COMPARACIÓN: Tabla LR(1) - Gramática de Declaraciones")
print("=" * 80)

# Gramática: D -> type L ;
#            L -> L , id | id
grammar = Grammar()
grammar.add_production("D", ["type", "L", ";"])
grammar.add_production("L", ["L", ",", "id"])
grammar.add_production("L", ["id"])

parser = LR1Parser(grammar)
parser.build()

print("\n📖 Gramática:")
print("   D -> type L ;")
print("   L -> L , id")
print("   L -> id")

print("\n📊 AUTÓMATA - Estados y Items Kernel:")
print("=" * 80)

for idx, state in enumerate(parser.states):
    print(f"\n🔸 Estado {idx}:")
    
    # Items kernel
    kernel_items = []
    for item in state:
        if idx == 0:
            if item.non_terminal == parser.augmented_start and item.dot_position == 0:
                kernel_items.append(str(item))
        else:
            if item.dot_position > 0:
                kernel_items.append(str(item))
    
    for k in sorted(kernel_items):
        print(f"   {k}")
    
    # Clausura (para estado 0 y otros relevantes)
    if idx in [0, 2, 3]:
        closure_items = []
        for item in state:
            is_kernel = (idx == 0 and item.non_terminal == parser.augmented_start and item.dot_position == 0) or (idx != 0 and item.dot_position > 0)
            if not is_kernel:
                closure_items.append(str(item))
        if closure_items:
            print(f"   Clausura:")
            for c in sorted(closure_items)[:3]:
                print(f"     {c}")
    
    # Transiciones
    trans = [(sym, dest) for (src, sym), dest in parser.transitions.items() if src == idx]
    if trans:
        print(f"   Transiciones:")
        for sym, dest in sorted(trans):
            print(f"     {sym} → Estado {dest}")

print("\n" + "=" * 80)
print("📋 COMPARACIÓN CON LA IMAGEN")
print("=" * 80)

print("\n🔍 Imagen muestra:")
print("   Estado 0: [D' -> .D, $]")
print("   goto(0, D) → Estado 1")
print("   goto(0, type) → Estado 2")
print("   ...")

print("\n✅ VERIFICACIÓN:")
expected_states = 8
actual_states = len(parser.states)
print(f"   Estados esperados: {expected_states}")
print(f"   Estados generados: {actual_states}")

if actual_states == expected_states:
    print(f"\n   ✅ CORRECTO: El número de estados coincide!")
else:
    print(f"\n   ❌ DIFERENCIA: Esperados {expected_states}, generados {actual_states}")

print("\n" + "=" * 80)
