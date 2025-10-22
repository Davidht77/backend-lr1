# -*- coding: utf-8 -*-
"""
Módulo Grammar
Define la clase Grammar para representar gramáticas libres de contexto.
"""

from collections import defaultdict
from typing import Set, Dict, List, Tuple


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
