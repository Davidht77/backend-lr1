# -*- coding: utf-8 -*-
"""
Módulo LR1Parser
Define la clase LR1Parser que implementa el análisis sintáctico LR(1).
"""

import graphviz
from collections import defaultdict, deque
from typing import Set, Dict, List, Tuple, FrozenSet

from .item import LR1Item


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
        # Estado inicial: [S' -> . S, $]
        initial_item = LR1Item(
            self.augmented_start,
            self.grammar.productions[0][1],
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

    def print_closure_table(self):
        """Imprime la tabla de clausura LR(1) (como en libros de texto)"""
        print("\n" + "=" * 120)
        print("TABLA DE CLAUSURA LR(1)")
        print("=" * 120)
        print(f"{'Goto':<20} | {'Kernel':<50} | {'State':<6} | {'Closure'}")
        print("-" * 120)

        for state_idx, state in enumerate(self.states):
            # Identificar items kernel
            kernel_items = []
            closure_items = []
            
            for item in state:
                if state_idx == 0:
                    # Estado inicial: solo el item aumentado
                    if item.non_terminal == self.augmented_start and item.dot_position == 0:
                        kernel_items.append(str(item))
                    else:
                        closure_items.append(str(item))
                else:
                    # Otros estados: items con punto > 0
                    if item.dot_position > 0:
                        kernel_items.append(str(item))
                    else:
                        closure_items.append(str(item))
            
            # Encontrar transiciones que llevan a este estado
            incoming_transitions = []
            for (src, symbol), dest in self.transitions.items():
                if dest == state_idx:
                    incoming_transitions.append((src, symbol))
            
            # Formatear goto
            if incoming_transitions:
                goto_str = ", ".join([f"goto({src}, {sym})" for src, sym in incoming_transitions])
            else:
                goto_str = "INITIAL" if state_idx == 0 else ""
            
            # Formatear kernel
            kernel_display = self._compact_items_notation(kernel_items)
            
            # Formatear clausura completa
            all_items = kernel_items + closure_items
            closure_display = self._compact_items_notation(all_items[:5])
            if len(all_items) > 5:
                closure_display += f"; ... (+{len(all_items) - 5})"
            
            # Imprimir fila
            print(f"{goto_str:<20} | {kernel_display:<50} | {state_idx:<6} | {closure_display}")
        
        print("=" * 120)

    def _compact_items_notation(self, items_list):
        """Intenta compactar items con la misma producción pero diferentes lookaheads"""
        if not items_list:
            return ""
        
        # Agrupar items por (producción, posición del punto)
        from collections import defaultdict
        groups = defaultdict(list)
        
        for item_str in items_list:
            # Extraer la parte antes de la coma (producción y punto)
            if ", " in item_str:
                prod_part, lookahead = item_str.rsplit(", ", 1)
                lookahead = lookahead.rstrip("]")
                groups[prod_part].append(lookahead)
            else:
                groups[item_str] = [""]
        
        # Reconstruir con notación compacta
        result = []
        for prod_part, lookaheads in list(groups.items())[:3]:
            if lookaheads and lookaheads[0]:
                if len(lookaheads) > 1:
                    # Notación compacta: usar / para separar lookaheads
                    la_str = "/".join(sorted(lookaheads))
                    result.append(f"{prod_part}, {la_str}]")
                else:
                    result.append(f"{prod_part}, {lookaheads[0]}]")
            else:
                result.append(prod_part)
        
        compact = "; ".join(result)
        if len(groups) > 3:
            compact += f"; ... (+{len(groups) - 3})"
        
        return compact

    def visualize_automaton(self, filename="automaton_lr1"):
        """Genera un gráfico completo del autómata LR(1) con todos los items"""
        dot = graphviz.Digraph(comment="Autómata LR(1) - Completo con Clausura")
        dot.attr(rankdir="LR")
        dot.attr("node", shape="rectangle", style="rounded", fontsize="8")

        # Añadir estados con TODOS los items (kernel + clausura)
        for idx, state in enumerate(self.states):
            # Separar items kernel de items de clausura
            kernel_items = []
            closure_items = []
            
            for item in state:
                # Items kernel: punto > 0, o items iniciales
                is_kernel = (
                    item.dot_position > 0 or 
                    (idx == 0 and item.non_terminal == self.augmented_start)
                )
                
                item_str = str(item).replace("→", "->").replace("·", ".")
                
                if is_kernel or item.non_terminal == self.augmented_start:
                    kernel_items.append(item_str)
                else:
                    closure_items.append(item_str)
            
            # Construir etiqueta: kernel primero, luego clausura
            all_items = sorted(kernel_items) + sorted(closure_items)
            
            # Mostrar hasta 10 items
            items_to_show = all_items[:10]
            label = "\\n".join(items_to_show)
            
            if len(all_items) > 10:
                label += f"\\n... (+{len(all_items) - 10} items)"

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

        # Añadir transiciones con el símbolo
        for (src, symbol), dest in self.transitions.items():
            dot.edge(str(src), str(dest), label=symbol, fontsize="9")

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
        """Genera un gráfico con items kernel del autómata LR(1)"""
        dot = graphviz.Digraph(comment="Autómata LR(1) - Items Kernel")
        dot.attr(rankdir="LR")
        dot.attr("node", shape="rectangle", style="rounded", fontsize="9")

        # Añadir estados con items kernel únicamente
        for idx in range(len(self.states)):
            state = self.states[idx]
            
            # Identificar items kernel correctamente
            kernel_items = []
            
            for item in state:
                is_kernel = False
                
                if idx == 0:
                    # Estado inicial: solo el item aumentado
                    if item.non_terminal == self.augmented_start and item.dot_position == 0:
                        is_kernel = True
                else:
                    # Otros estados: items con punto > 0
                    if item.dot_position > 0:
                        is_kernel = True
                
                if is_kernel:
                    # Construir representación completa con lookahead
                    prod_list = list(item.production)
                    prod_list.insert(item.dot_position, "•")
                    prod_str = " ".join(prod_list) if prod_list != ["•"] else "•"
                    rule = f"[{item.non_terminal}→{prod_str}, {item.lookahead}]"
                    kernel_items.append(rule)
            
            # Mostrar items kernel
            if kernel_items:
                label = "\\n".join(sorted(kernel_items)[:8])
                if len(kernel_items) > 8:
                    label += f"\\n... (+{len(kernel_items) - 8} items)"
            else:
                label = "VACÍO"
            
            # Marcar estado de aceptación
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
            dot.edge(str(src), str(dest), label=symbol, fontsize="9")

        # Guardar
        try:
            output_filename = f"{filename}_simplified"
            dot.render(output_filename, format="png", cleanup=True)
            print(
                f"[OK] Grafico con items kernel guardado como '{output_filename}.png'"
            )
        except Exception as e:
            print(f"[WARNING] No se pudo generar el grafico simplificado: {e}")
