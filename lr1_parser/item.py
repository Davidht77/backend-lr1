# -*- coding: utf-8 -*-
"""
Módulo LR1Item
Define la clase LR1Item para representar items LR(1).
"""


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
        return f"{self.non_terminal} → {prod_str}, {self.lookahead}"
    
    def __str__(self):
        """Representación en string sin corchetes para API/visualización"""
        return self.__repr__()

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
