# -*- coding: utf-8 -*-
"""
Parser LR(1) Completo
Implementa el análisis sintáctico LR(1) con:
- Cálculo de terminales y no terminales
- Cálculo de FIRST y FOLLOW
- Construcción de items LR(1)
- AFD (Autómata de items LR(1))
- Tabla de parsing LR(1)
- Visualización con gráficos
"""

import graphviz
from collections import defaultdict, deque
from typing import Set, Dict, List, Tuple, FrozenSet
import copy


class Grammar:
    """Clase para representar una gramática libre de contexto"""

    def __init__(self):
        self.productions = []  # Lista de producciones (no_terminal, produccion)
        self.start_symbol = None
        self.terminals = set()
        self.non_terminals = set()
        self.epsilon = "epsilon"
        self.end_marker = "$"

    def add_production(self, non_terminal, production):
        """Añade una producción a la gramática"""
        if self.start_symbol is None:
            self.start_symbol = non_terminal
        self.productions.append((non_terminal, production))
        self.non_terminals.add(non_terminal)

    def compute_terminals_and_non_terminals(self):
        """Calcula los terminales y no terminales de la gramática"""
        self.non_terminals = set()
        all_symbols = set()

        # Extraer todos los no terminales (lado izquierdo de las producciones)
        for non_terminal, production in self.productions:
            self.non_terminals.add(non_terminal)

        # Extraer todos los símbolos que aparecen en las producciones
        for non_terminal, production in self.productions:
            for symbol in production:
                if symbol != self.epsilon:
                    all_symbols.add(symbol)

        # Los terminales son todos los símbolos que no son no terminales
        self.terminals = all_symbols - self.non_terminals
        self.terminals.add(self.end_marker)

        return self.terminals, self.non_terminals

    def compute_first(self):
        """Calcula el conjunto FIRST para cada símbolo"""
        first = {symbol: set() for symbol in self.non_terminals | self.terminals}

        # FIRST de terminales es el terminal mismo
        for terminal in self.terminals:
            first[terminal].add(terminal)

        # Añadir epsilon a FIRST si hay producción epsilon
        first[self.epsilon] = {self.epsilon}

        # Iterar hasta que no haya cambios
        changed = True
        while changed:
            changed = False
            for non_terminal, production in self.productions:
                old_size = len(first[non_terminal])

                if not production or production[0] == self.epsilon:
                    # Producción epsilon
                    first[non_terminal].add(self.epsilon)
                else:
                    # Procesar la producción
                    for i, symbol in enumerate(production):
                        # Añadir FIRST(symbol) - {epsilon} a FIRST(non_terminal)
                        first[non_terminal] |= first[symbol] - {self.epsilon}

                        # Si epsilon no está en FIRST(symbol), parar
                        if self.epsilon not in first[symbol]:
                            break

                        # Si llegamos al final y todos tenían epsilon
                        if i == len(production) - 1:
                            first[non_terminal].add(self.epsilon)

                if len(first[non_terminal]) > old_size:
                    changed = True

        return first

    def compute_follow(self, first):
        """Calcula el conjunto FOLLOW para cada no terminal"""
        follow = {non_terminal: set() for non_terminal in self.non_terminals}

        # FOLLOW del símbolo inicial contiene $
        follow[self.start_symbol].add(self.end_marker)

        # Iterar hasta que no haya cambios
        changed = True
        while changed:
            changed = False
            for non_terminal, production in self.productions:
                for i, symbol in enumerate(production):
                    if symbol in self.non_terminals:
                        old_size = len(follow[symbol])

                        # Calcular FIRST del resto de la producción
                        rest = production[i + 1 :]
                        if rest:
                            first_rest = self._first_of_sequence(rest, first)
                            follow[symbol] |= first_rest - {self.epsilon}

                            # Si epsilon está en FIRST(rest), añadir FOLLOW(non_terminal)
                            if self.epsilon in first_rest:
                                follow[symbol] |= follow[non_terminal]
                        else:
                            # Si no hay más símbolos, añadir FOLLOW(non_terminal)
                            follow[symbol] |= follow[non_terminal]

                        if len(follow[symbol]) > old_size:
                            changed = True

        return follow

    def _first_of_sequence(self, sequence, first):
        """Calcula FIRST de una secuencia de símbolos"""
        result = set()
        for symbol in sequence:
            result |= first[symbol] - {self.epsilon}
            if self.epsilon not in first[symbol]:
                break
        else:
            # Todos los símbolos pueden derivar epsilon
            result.add(self.epsilon)
        return result

    def print_grammar(self):
        """Imprime la gramática"""
        print("\n" + "=" * 60)
        print("GRAMÁTICA")
        print("=" * 60)
        productions_dict = defaultdict(list)
        for non_terminal, production in self.productions:
            prod_str = " ".join(production) if production else self.epsilon
            productions_dict[non_terminal].append(prod_str)

        for non_terminal in productions_dict:
            prods = " | ".join(productions_dict[non_terminal])
            print(f"{non_terminal} -> {prods}")

    def print_sets(self, first, follow):
        """Imprime los conjuntos FIRST y FOLLOW"""
        print("\n" + "=" * 60)
        print("TERMINALES Y NO TERMINALES")
        print("=" * 60)
        print(f"Terminales: {sorted(self.terminals)}")
        print(f"No Terminales: {sorted(self.non_terminals)}")

        print("\n" + "=" * 60)
        print("CONJUNTOS FIRST")
        print("=" * 60)
        for non_terminal in sorted(self.non_terminals):
            first_str = ", ".join(sorted(first[non_terminal]))
            print(f"FIRST({non_terminal}) = {{ {first_str} }}")

        print("\n" + "=" * 60)
        print("CONJUNTOS FOLLOW")
        print("=" * 60)
        for non_terminal in sorted(self.non_terminals):
            follow_str = ", ".join(sorted(follow[non_terminal]))
            print(f"FOLLOW({non_terminal}) = {{ {follow_str} }}")


class LR1Item:
    """Representa un item LR(1): [A → α·β, a]"""

    def __init__(self, non_terminal, production, dot_position, lookahead):
        self.non_terminal = non_terminal
        self.production = tuple(production)
        self.dot_position = dot_position
        self.lookahead = lookahead

    def __eq__(self, other):
        return (
            self.non_terminal == other.non_terminal
            and self.production == other.production
            and self.dot_position == other.dot_position
            and self.lookahead == other.lookahead
        )

    def __hash__(self):
        return hash(
            (self.non_terminal, self.production, self.dot_position, self.lookahead)
        )

    def __repr__(self):
        prod_list = list(self.production)
        prod_list.insert(self.dot_position, ".")
        prod_str = " ".join(prod_list)
        return f"[{self.non_terminal} -> {prod_str}, {self.lookahead}]"

    def next_symbol(self):
        """Retorna el símbolo después del punto, o None si está al final"""
        if self.dot_position < len(self.production):
            return self.production[self.dot_position]
        return None

    def advance(self):
        """Retorna un nuevo item con el punto avanzado una posición"""
        return LR1Item(
            self.non_terminal, self.production, self.dot_position + 1, self.lookahead
        )


class LR1Parser:
    """Parser LR(1) completo"""

    def __init__(self, grammar):
        self.grammar = grammar
        self.first = {}
        self.follow = {}
        self.states = []
        self.transitions = {}
        self.parsing_table = {"action": {}, "goto": {}}

        # Aumentar la gramática
        self.augmented_start = self.grammar.start_symbol + "'"
        self.grammar.productions.insert(
            0, (self.augmented_start, [self.grammar.start_symbol])
        )
        self.grammar.non_terminals.add(self.augmented_start)
        self.grammar.start_symbol = self.augmented_start

    def build(self):
        """Construye el parser LR(1) completo"""
        # Calcular terminales y no terminales
        self.grammar.compute_terminals_and_non_terminals()

        # Calcular FIRST y FOLLOW
        self.first = self.grammar.compute_first()
        self.follow = self.grammar.compute_follow(self.first)

        # Construir el autómata LR(1)
        self.build_automaton()

        # Construir la tabla de parsing
        self.build_parsing_table()

    def closure(self, items):
        """Calcula la clausura de un conjunto de items LR(1)"""
        closure_set = set(items)
        queue = deque(items)

        while queue:
            item = queue.popleft()
            next_sym = item.next_symbol()

            if next_sym and next_sym in self.grammar.non_terminals:
                # Calcular FIRST de la secuencia después del símbolo
                rest = list(item.production[item.dot_position + 1 :]) + [item.lookahead]
                first_rest = self.grammar._first_of_sequence(rest, self.first)

                # Para cada producción de next_sym
                for non_terminal, production in self.grammar.productions:
                    if non_terminal == next_sym:
                        for lookahead in first_rest:
                            if lookahead != self.grammar.epsilon:
                                new_item = LR1Item(
                                    non_terminal, production, 0, lookahead
                                )
                                if new_item not in closure_set:
                                    closure_set.add(new_item)
                                    queue.append(new_item)

        return frozenset(closure_set)

    def goto(self, items, symbol):
        """Calcula GOTO(items, symbol)"""
        goto_set = set()

        for item in items:
            if item.next_symbol() == symbol:
                goto_set.add(item.advance())

        if goto_set:
            return self.closure(goto_set)
        return frozenset()

    def build_automaton(self):
        """Construye el autómata LR(1)"""
        # Estado inicial
        initial_item = LR1Item(
            self.augmented_start,
            [self.grammar.productions[0][1][0]],
            0,
            self.grammar.end_marker,
        )
        initial_state = self.closure([initial_item])

        self.states = [initial_state]
        unmarked = [initial_state]
        state_map = {initial_state: 0}

        while unmarked:
            current_state = unmarked.pop(0)
            current_index = state_map[current_state]

            # Obtener todos los símbolos posibles después del punto
            symbols = set()
            for item in current_state:
                next_sym = item.next_symbol()
                if next_sym:
                    symbols.add(next_sym)

            # Para cada símbolo, calcular GOTO
            for symbol in symbols:
                goto_state = self.goto(current_state, symbol)

                if goto_state:
                    if goto_state not in state_map:
                        state_map[goto_state] = len(self.states)
                        self.states.append(goto_state)
                        unmarked.append(goto_state)

                    goto_index = state_map[goto_state]
                    self.transitions[(current_index, symbol)] = goto_index

    def build_parsing_table(self):
        """Construye la tabla de parsing LR(1)"""
        for state_idx, state in enumerate(self.states):
            for item in state:
                if item.next_symbol() is None:
                    # Item de reducción
                    if item.non_terminal == self.augmented_start:
                        # Aceptar
                        self._add_action(
                            state_idx, self.grammar.end_marker, ("accept", None)
                        )
                    else:
                        # Reducir
                        prod_num = self._find_production_number(
                            item.non_terminal, item.production
                        )
                        self._add_action(
                            state_idx, item.lookahead, ("reduce", prod_num)
                        )
                else:
                    next_sym = item.next_symbol()
                    if next_sym in self.grammar.terminals:
                        # Desplazar
                        if (state_idx, next_sym) in self.transitions:
                            next_state = self.transitions[(state_idx, next_sym)]
                            self._add_action(state_idx, next_sym, ("shift", next_state))

            # GOTO para no terminales
            for non_terminal in self.grammar.non_terminals:
                if (state_idx, non_terminal) in self.transitions:
                    next_state = self.transitions[(state_idx, non_terminal)]
                    if state_idx not in self.parsing_table["goto"]:
                        self.parsing_table["goto"][state_idx] = {}
                    self.parsing_table["goto"][state_idx][non_terminal] = next_state

    def _add_action(self, state, terminal, action):
        """Añade una acción a la tabla de parsing"""
        if state not in self.parsing_table["action"]:
            self.parsing_table["action"][state] = {}

        if terminal in self.parsing_table["action"][state]:
            existing = self.parsing_table["action"][state][terminal]
            if existing != action:
                print(f"[WARNING] CONFLICTO en estado {state}, terminal '{terminal}':")
                print(f"   Acción existente: {existing}")
                print(f"   Nueva acción: {action}")
        else:
            self.parsing_table["action"][state][terminal] = action

    def _find_production_number(self, non_terminal, production):
        """Encuentra el número de producción"""
        for idx, (nt, prod) in enumerate(self.grammar.productions):
            if nt == non_terminal and tuple(prod) == production:
                return idx
        return -1

    def print_automaton(self):
        """Imprime el autómata LR(1)"""
        print("\n" + "=" * 60)
        print("AUTÓMATA LR(1)")
        print("=" * 60)

        for idx, state in enumerate(self.states):
            print(f"\nEstado I{idx}:")
            for item in sorted(state, key=lambda x: str(x)):
                print(f"  {item}")

            # Mostrar transiciones
            transitions_from_state = [
                (sym, dest)
                for (src, sym), dest in self.transitions.items()
                if src == idx
            ]
            if transitions_from_state:
                print("  Transiciones:")
                for symbol, dest_state in sorted(transitions_from_state):
                    print(f"    {symbol} -> I{dest_state}")

    def print_parsing_table(self):
        """Imprime la tabla de parsing"""
        print("\n" + "=" * 60)
        print("TABLA DE PARSING LR(1)")
        print("=" * 60)

        # Encabezados
        terminals = sorted(self.grammar.terminals - {self.grammar.epsilon})
        non_terminals = sorted(self.grammar.non_terminals - {self.augmented_start})

        # Calcular anchos de columna
        col_width = 12

        # Imprimir encabezado
        header = f"{'Estado':<8} |"
        header += (
            " ACTION ".center(len(terminals) * col_width + len(terminals) - 1) + "|"
        )
        header += " GOTO ".center(
            len(non_terminals) * col_width + len(non_terminals) - 1
        )
        print(header)

        subheader = f"{'':<8} |"
        for term in terminals:
            subheader += f" {term:<{col_width - 1}}"
        subheader += "|"
        for nt in non_terminals:
            subheader += f" {nt:<{col_width - 1}}"
        print(subheader)
        print("-" * len(subheader))

        # Imprimir cada estado
        for state_idx in range(len(self.states)):
            row = f"{state_idx:<8} |"

            # ACTION
            for term in terminals:
                if (
                    state_idx in self.parsing_table["action"]
                    and term in self.parsing_table["action"][state_idx]
                ):
                    action_type, value = self.parsing_table["action"][state_idx][term]
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
                row += f" {cell:<{col_width - 1}}"

            row += "|"

            # GOTO
            for nt in non_terminals:
                if (
                    state_idx in self.parsing_table["goto"]
                    and nt in self.parsing_table["goto"][state_idx]
                ):
                    cell = str(self.parsing_table["goto"][state_idx][nt])
                else:
                    cell = ""
                row += f" {cell:<{col_width - 1}}"

            print(row)

        # Leyenda de producciones
        print("\n" + "=" * 60)
        print("PRODUCCIONES (para reducción)")
        print("=" * 60)
        for idx, (nt, prod) in enumerate(self.grammar.productions):
            prod_str = " ".join(prod) if prod else self.grammar.epsilon
            print(f"{idx}: {nt} -> {prod_str}")

    def visualize_automaton(self, filename="automaton_lr1"):
        """Genera un gráfico del autómata LR(1)"""
        dot = graphviz.Digraph(comment="Autómata LR(1)")
        dot.attr(rankdir="LR")
        dot.attr("node", shape="rectangle", style="rounded")

        # Añadir estados
        for idx, state in enumerate(self.states):
            label = f"I{idx}\\n"
            label += "\\n".join(
                [
                    str(item).replace("→", "->").replace("·", ".")
                    for item in sorted(state, key=lambda x: str(x))
                ][:5]
            )
            if len(state) > 5:
                label += f"\\n... (+{len(state) - 5} items)"

            # Estado de aceptación
            if any(
                item.non_terminal == self.augmented_start and item.next_symbol() is None
                for item in state
            ):
                dot.node(
                    str(idx),
                    label,
                    shape="doublecircle",
                    style="rounded,filled",
                    fillcolor="lightgreen",
                )
            else:
                dot.node(str(idx), label)

        # Añadir transiciones
        for (src, symbol), dest in self.transitions.items():
            dot.edge(str(src), str(dest), label=symbol)

        # Guardar
        try:
            dot.render(filename, format="png", cleanup=True)
            print(f"\n[OK] Grafico del automata guardado como '{filename}.png'")
        except Exception as e:
            print(f"\n[WARNING] No se pudo generar el grafico: {e}")
            print(
                "   Asegurate de tener Graphviz instalado: https://graphviz.org/download/"
            )

    def visualize_simplified_automaton(self, filename="automaton_lr1_simplified"):
        """Genera un gráfico simplificado del autómata LR(1)"""
        dot = graphviz.Digraph(comment="Autómata LR(1) Simplificado")
        dot.attr(rankdir="LR")
        dot.attr("node", shape="circle")

        # Añadir estados (solo números)
        for idx in range(len(self.states)):
            if any(
                item.non_terminal == self.augmented_start and item.next_symbol() is None
                for item in self.states[idx]
            ):
                dot.node(
                    str(idx),
                    f"I{idx}",
                    shape="doublecircle",
                    style="filled",
                    fillcolor="lightgreen",
                )
            else:
                dot.node(str(idx), f"I{idx}")

        # Añadir transiciones
        for (src, symbol), dest in self.transitions.items():
            dot.edge(str(src), str(dest), label=symbol)

        # Guardar
        try:
            dot.render(filename, format="png", cleanup=True)
            print(
                f"[OK] Grafico simplificado guardado como '{filename}_simplified.png'"
            )
        except Exception as e:
            print(f"[WARNING] No se pudo generar el grafico simplificado: {e}")


def create_example_grammar_1():
    """Crea una gramática de ejemplo simple"""
    grammar = Grammar()

    # Gramática: E → E + T | T
    #            T → T * F | F
    #            F → ( E ) | id

    grammar.add_production("E", ["E", "+", "T"])
    grammar.add_production("E", ["T"])
    grammar.add_production("T", ["T", "*", "F"])
    grammar.add_production("T", ["F"])
    grammar.add_production("F", ["(", "E", ")"])
    grammar.add_production("F", ["id"])

    return grammar


def create_example_grammar_2():
    """Crea otra gramática de ejemplo"""
    grammar = Grammar()

    # Gramática: S → A a | b A c | d c | b d a
    #            A → d

    grammar.add_production("S", ["A", "a"])
    grammar.add_production("S", ["b", "A", "c"])
    grammar.add_production("S", ["d", "c"])
    grammar.add_production("S", ["b", "d", "a"])
    grammar.add_production("A", ["d"])

    return grammar


def create_example_grammar_3():
    """Crea una gramática con recursión a la izquierda"""
    grammar = Grammar()

    # Gramática simple con operadores
    # S → S + A | A
    # A → ( S ) | a

    grammar.add_production("S", ["S", "+", "A"])
    grammar.add_production("S", ["A"])
    grammar.add_production("A", ["(", "S", ")"])
    grammar.add_production("A", ["a"])

    return grammar


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print(" PARSER LR(1) - Análisis Sintáctico Ascendente")
    print("=" * 60)

    # Seleccionar gramática
    print("\nSeleccione una gramática de ejemplo:")
    print("1. Expresiones aritméticas (E → E + T | T, etc.)")
    print("2. Gramática S → A a | b A c | d c | b d a")
    print("3. Gramática simple S → S + A | A")

    choice = input("\nIngrese su opción (1-3) [1]: ").strip() or "1"

    if choice == "2":
        grammar = create_example_grammar_2()
    elif choice == "3":
        grammar = create_example_grammar_3()
    else:
        grammar = create_example_grammar_1()

    # Imprimir gramática original
    grammar.print_grammar()

    # Crear parser
    print("\n[...] Construyendo parser LR(1)...")
    parser = LR1Parser(grammar)
    parser.build()

    # Imprimir resultados
    grammar.print_sets(parser.first, parser.follow)
    parser.print_automaton()
    parser.print_parsing_table()

    # Generar gráficos
    print("\n" + "=" * 60)
    print("GENERACIÓN DE GRÁFICOS")
    print("=" * 60)
    parser.visualize_automaton()
    parser.visualize_simplified_automaton()

    print("\n" + "=" * 60)
    print("[OK] PARSER LR(1) COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print("\nEl parser incluye:")
    print("  [OK] Calculo de terminales y no terminales")
    print("  [OK] Conjuntos FIRST")
    print("  [OK] Conjuntos FOLLOW")
    print("  [OK] Automata LR(1) con items")
    print("  [OK] Tabla de parsing (ACTION y GOTO)")
    print("  [OK] Graficos visuales del automata")
    print("\nArchivos generados:")
    print("  - automaton_lr1.png (grafico detallado)")
    print("  - automaton_lr1_simplified.png (grafico simplificado)")


if __name__ == "__main__":
    main()
