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
        """
        Genera el AFD: solo items kernel agrupados por estado.
        """
        dot = graphviz.Digraph(comment="Autómata LR(1) - AFD (Items Kernel)")
        dot.attr(rankdir="LR")  # Left to Right
        dot.attr("node", shape="ellipse", fontsize="11", fontname="Arial")
        dot.attr("edge", fontsize="11", fontname="Arial")
        
        # Layout más espaciado y claro
        dot.attr(ranksep="1.0")
        dot.attr(nodesep="0.8")
        
        # Crear estados con items kernel agrupados
        for idx, state in enumerate(self.states):
            # Recolectar solo items kernel
            kernel_items = []
            
            for item in state:
                # Solo items kernel
                is_kernel = (
                    item.dot_position > 0 or 
                    (idx == 0 and item.non_terminal == self.augmented_start)
                )
                
                if is_kernel:
                    # Construir el item SIN corchetes
                    prod_list = list(item.production)
                    prod_list.insert(item.dot_position, ".")
                    
                    # Formatear producción
                    prod_str = " ".join(prod_list) if prod_list != ["."] else "."
                    prod_str = prod_str.replace("ε", "").replace("  ", " ").strip()
                    if prod_str == ".":
                        prod_str = "."
                    
                    # Formatear como: A → α . β, a (SIN corchetes)
                    item_formatted = f"{item.non_terminal} → {prod_str}, {item.lookahead}"
                    kernel_items.append(item_formatted)
            
            # Si hay items kernel, crear el nodo
            if kernel_items:
                label = "\\n".join(kernel_items)
                # Usar forma elíptica para estados
                dot.node(str(idx), label, shape="ellipse", style="solid", penwidth="1.5")
        
        # Añadir transiciones entre estados
        for (src, symbol), dest in self.transitions.items():
            dot.edge(str(src), str(dest), label=f" {symbol} ", fontsize="11", penwidth="1.2")

        # Guardar
        try:
            dot.render(filename, format="png", cleanup=True)
            print(f"\n[OK] AFD (Items kernel agrupados) guardado como '{filename}.png'")
        except Exception as e:
            print(f"\n[WARNING] No se pudo generar el grafico: {e}")
            print(
                "   Asegurate de tener Graphviz instalado: https://graphviz.org/download/"
            )

    def visualize_simplified_automaton(self, filename="automaton_lr1_simplified"):
        """
        Genera el AFN: todos los items (kernel + clausura) con transiciones item a item.
        """
        dot = graphviz.Digraph(comment="Autómata LR(1) - AFN (Clausura Completa)")
        dot.attr(rankdir="LR")  # Left to Right para mejor visualización
        dot.attr("node", shape="ellipse", fontsize="10", fontname="Arial")
        dot.attr("edge", fontsize="10", fontname="Arial")
        
        # Layout más espaciado
        dot.attr(ranksep="0.8")
        dot.attr(nodesep="0.5")
        
        # Mapeo de item_str -> node_id (sin distinguir por estado para evitar duplicados)
        node_map = {}
        node_counter = 0

        # Primero, recolectar todos los items únicos
        all_items_set = set()
        for idx, state in enumerate(self.states):
            for item in state:
                # Construir el item sin corchetes
                prod_list = list(item.production)
                prod_list.insert(item.dot_position, ".")
                
                # Formatear producción
                prod_str = " ".join(prod_list) if prod_list != ["."] else "."
                prod_str = prod_str.replace("ε", "").replace("  ", " ").strip()
                if prod_str == ".":
                    prod_str = "."
                
                # Formatear como: A → α . β, a (SIN corchetes)
                item_str = f"{item.non_terminal} → {prod_str}, {item.lookahead}"
                all_items_set.add(item_str)
        
        # Crear nodos para cada item único
        for item_str in sorted(all_items_set):
            node_id = f"n{node_counter}"
            node_map[item_str] = node_id
            node_counter += 1
            # Label sin corchetes
            dot.node(node_id, item_str, shape="ellipse")

        # Crear transiciones entre items basadas en las transiciones del autómata
        edges_added = set()  # Para evitar aristas duplicadas
        
        for (src_state, symbol), dest_state in self.transitions.items():
            # Para cada item en el estado origen
            for src_item in self.states[src_state]:
                # Solo si el item tiene el símbolo después del punto
                if src_item.next_symbol() == symbol:
                    # El item avanzado
                    advanced_item = src_item.advance()
                    
                    # Construir representaciones sin corchetes
                    prod_list_src = list(src_item.production)
                    prod_list_src.insert(src_item.dot_position, ".")
                    prod_str_src = " ".join(prod_list_src) if prod_list_src != ["."] else "."
                    prod_str_src = prod_str_src.replace("ε", "").replace("  ", " ").strip()
                    src_item_str = f"{src_item.non_terminal} → {prod_str_src}, {src_item.lookahead}"
                    
                    prod_list_adv = list(advanced_item.production)
                    prod_list_adv.insert(advanced_item.dot_position, ".")
                    prod_str_adv = " ".join(prod_list_adv) if prod_list_adv != ["."] else "."
                    prod_str_adv = prod_str_adv.replace("ε", "").replace("  ", " ").strip()
                    adv_item_str = f"{advanced_item.non_terminal} → {prod_str_adv}, {advanced_item.lookahead}"
                    
                    # Crear arista si ambos items existen
                    if src_item_str in node_map and adv_item_str in node_map:
                        edge_key = (src_item_str, adv_item_str, symbol)
                        if edge_key not in edges_added:
                            dot.edge(node_map[src_item_str], node_map[adv_item_str], 
                                   label=symbol, fontsize="10")
                            edges_added.add(edge_key)
        
        # Añadir transiciones epsilon (clausura) dentro de cada estado
        for idx, state in enumerate(self.states):
            items_list = list(state)
            # Identificar items kernel en este estado
            kernel_items = []
            for item in items_list:
                is_kernel = (
                    item.dot_position > 0 or 
                    (idx == 0 and item.non_terminal == self.augmented_start)
                )
                if is_kernel:
                    kernel_items.append(item)
            
            # Desde cada item kernel, crear aristas epsilon a items de clausura
            for kernel_item in kernel_items:
                # Formatear kernel item
                prod_list_k = list(kernel_item.production)
                prod_list_k.insert(kernel_item.dot_position, ".")
                prod_str_k = " ".join(prod_list_k) if prod_list_k != ["."] else "."
                prod_str_k = prod_str_k.replace("ε", "").replace("  ", " ").strip()
                kernel_str = f"{kernel_item.non_terminal} → {prod_str_k}, {kernel_item.lookahead}"
                
                # Para cada item de clausura en este estado
                for closure_item in items_list:
                    if closure_item.dot_position == 0 and closure_item != kernel_item:
                        # Este es un item de clausura
                        prod_list_c = list(closure_item.production)
                        prod_list_c.insert(closure_item.dot_position, ".")
                        prod_str_c = " ".join(prod_list_c) if prod_list_c != ["."] else "."
                        prod_str_c = prod_str_c.replace("ε", "").replace("  ", " ").strip()
                        closure_str = f"{closure_item.non_terminal} → {prod_str_c}, {closure_item.lookahead}"
                        
                        # Verificar si debe haber una transición epsilon
                        next_sym = kernel_item.next_symbol()
                        if next_sym and next_sym in self.grammar.non_terminals:
                            if closure_item.non_terminal == next_sym:
                                # Hay una relación de clausura
                                edge_key = (kernel_str, closure_str, "ε")
                                if edge_key not in edges_added:
                                    if kernel_str in node_map and closure_str in node_map:
                                        dot.edge(node_map[kernel_str], node_map[closure_str], 
                                               label="ε", fontsize="9", style="dashed", color="gray")
                                        edges_added.add(edge_key)

        # Guardar
        try:
            output_filename = f"{filename}_kernel"
            dot.render(output_filename, format="png", cleanup=True)
            print(f"[OK] AFN (Clausura completa) guardado como '{output_filename}.png'")
        except Exception as e:
            print(f"[WARNING] No se pudo generar el grafico: {e}")
