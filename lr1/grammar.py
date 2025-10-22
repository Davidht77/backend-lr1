"""Grammar utilities for LR(1) parser construction."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

Symbol = str
Production = List[Symbol]
ProductionRule = Tuple[Symbol, Production]


class Grammar:
    """Context-free grammar with helpers for LR(1) parsing."""

    def __init__(self, epsilon: str = "epsilon", end_marker: str = "$") -> None:
        self.productions: List[ProductionRule] = []
        self.start_symbol: Optional[Symbol] = None
        self.terminals: Set[Symbol] = set()
        self.non_terminals: Set[Symbol] = set()
        self.epsilon = epsilon
        self.end_marker = end_marker

    # ------------------------------------------------------------------
    # Grammar definition helpers
    # ------------------------------------------------------------------
    def add_production(self, non_terminal: Symbol, production: Iterable[Symbol]) -> None:
        """Register a new production rule A -> alpha."""
        symbols = list(production)
        if self.start_symbol is None:
            self.start_symbol = non_terminal
        self.productions.append((non_terminal, symbols))
        self.non_terminals.add(non_terminal)

    # ------------------------------------------------------------------
    # Grammar analysis helpers
    # ------------------------------------------------------------------
    def compute_terminals_and_non_terminals(self) -> Tuple[Set[Symbol], Set[Symbol]]:
        """Return the sets of terminals and non-terminals detected in the grammar."""
        self.non_terminals = {lhs for lhs, _ in self.productions}

        all_symbols: Set[Symbol] = set()
        for _, production in self.productions:
            for symbol in production:
                if symbol != self.epsilon:
                    all_symbols.add(symbol)

        self.terminals = all_symbols - self.non_terminals
        self.terminals.add(self.end_marker)
        return self.terminals, self.non_terminals

    def compute_first(self) -> Dict[Symbol, Set[Symbol]]:
        """Compute FIRST sets for every grammar symbol."""
        first: Dict[Symbol, Set[Symbol]] = {
            symbol: set() for symbol in self.non_terminals | self.terminals
        }

        # Terminals: FIRST(a) = {a}
        for terminal in self.terminals:
            first[terminal].add(terminal)

        # Provide FIRST(epsilon) so it can be queried safely
        first[self.epsilon] = {self.epsilon}

        changed = True
        while changed:
            changed = False
            for non_terminal, production in self.productions:
                current_first = first[non_terminal]
                before = len(current_first)

                if not production or production[0] == self.epsilon:
                    current_first.add(self.epsilon)
                else:
                    for index, symbol in enumerate(production):
                        symbol_first = first.setdefault(symbol, {symbol})
                        current_first |= symbol_first - {self.epsilon}
                        if self.epsilon not in symbol_first:
                            break
                        if index == len(production) - 1:
                            current_first.add(self.epsilon)

                if len(current_first) != before:
                    changed = True

        return first

    def compute_follow(self, first: Dict[Symbol, Set[Symbol]]) -> Dict[Symbol, Set[Symbol]]:
        """Compute FOLLOW sets for every non-terminal."""
        follow: Dict[Symbol, Set[Symbol]] = {
            non_terminal: set() for non_terminal in self.non_terminals
        }

        if self.start_symbol is not None:
            follow[self.start_symbol].add(self.end_marker)

        changed = True
        while changed:
            changed = False
            for non_terminal, production in self.productions:
                for index, symbol in enumerate(production):
                    if symbol in self.non_terminals:
                        target_follow = follow[symbol]
                        before = len(target_follow)

                        rest = production[index + 1 :]
                        if rest:
                            first_rest = self._first_of_sequence(rest, first)
                            target_follow |= first_rest - {self.epsilon}
                            if self.epsilon in first_rest:
                                target_follow |= follow[non_terminal]
                        else:
                            target_follow |= follow[non_terminal]

                        if len(target_follow) != before:
                            changed = True

        return follow

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    def _first_of_sequence(
        self, sequence: Sequence[Symbol], first: Dict[Symbol, Set[Symbol]]
    ) -> Set[Symbol]:
        """Compute FIRST for a sequence of symbols."""
        result: Set[Symbol] = set()
        for symbol in sequence:
            symbol_first = first.setdefault(symbol, {symbol})
            result |= symbol_first - {self.epsilon}
            if self.epsilon not in symbol_first:
                break
        else:
            result.add(self.epsilon)
        return result

    # ------------------------------------------------------------------
    # Debug printing helpers
    # ------------------------------------------------------------------
    def print_grammar(self) -> None:
        """Pretty-print the grammar productions."""
        print("\n" + "=" * 60)
        print("GRAMATICA")
        print("=" * 60)

        grouped: Dict[Symbol, List[str]] = defaultdict(list)
        for non_terminal, production in self.productions:
            grouped[non_terminal].append(" ".join(production) if production else self.epsilon)

        for non_terminal, alternatives in grouped.items():
            joined = " | ".join(alternatives)
            print(f"{non_terminal} -> {joined}")

    def print_sets(
        self, first: Dict[Symbol, Set[Symbol]], follow: Dict[Symbol, Set[Symbol]]
    ) -> None:
        """Print FIRST and FOLLOW sets for debugging purposes."""
        print("\n" + "=" * 60)
        print("TERMINALES Y NO TERMINALES")
        print("=" * 60)
        print(f"Terminales: {sorted(self.terminals)}")
        print(f"No Terminales: {sorted(self.non_terminals)}")

        print("\n" + "=" * 60)
        print("CONJUNTOS FIRST")
        print("=" * 60)
        for non_terminal in sorted(self.non_terminals):
            first_str = ", ".join(sorted(first.get(non_terminal, set())))
            print(f"FIRST({non_terminal}) = {{ {first_str} }}")

        print("\n" + "=" * 60)
        print("CONJUNTOS FOLLOW")
        print("=" * 60)
        for non_terminal in sorted(self.non_terminals):
            follow_str = ", ".join(sorted(follow.get(non_terminal, set())))
            print(f"FOLLOW({non_terminal}) = {{ {follow_str} }}")
