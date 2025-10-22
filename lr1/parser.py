"""Core LR(1) parser construction logic."""
from __future__ import annotations

import copy
from collections import deque
from typing import Deque, Dict, FrozenSet, Iterable, List, Optional, Sequence, Set, Tuple

from .grammar import Grammar, Symbol
from .items import LR1Item

Action = Tuple[str, Optional[int]]
TransitionKey = Tuple[int, Symbol]


class LR1Parser:
    """Builds LR(1) parsing tables and automaton for a grammar."""

    def __init__(self, grammar: Grammar) -> None:
        if grammar.start_symbol is None and not grammar.productions:
            raise ValueError("Grammar must contain at least one production.")

        self.source_grammar = grammar
        self.grammar = copy.deepcopy(grammar)
        self.original_start_symbol = self.grammar.start_symbol
        if self.original_start_symbol is None:
            # Should not happen if a production exists, but guard anyway.
            self.original_start_symbol = self.grammar.productions[0][0]
            self.grammar.start_symbol = self.original_start_symbol

        self.augmented_start = self._build_augmented_start_symbol()
        self._augment_grammar()

        self.first: Dict[Symbol, Set[Symbol]] = {}
        self.follow: Dict[Symbol, Set[Symbol]] = {}
        self.states: List[FrozenSet[LR1Item]] = []
        self.transitions: Dict[TransitionKey, int] = {}

        self.action_table: Dict[int, Dict[Symbol, Action]] = {}
        self.goto_table: Dict[int, Dict[Symbol, int]] = {}
        self.parsing_table = {"action": self.action_table, "goto": self.goto_table}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def build(self) -> None:
        """Compute FIRST/FOLLOW sets, automaton states and parsing table."""
        self.grammar.compute_terminals_and_non_terminals()
        self.first = self.grammar.compute_first()
        self.follow = self.grammar.compute_follow(self.first)
        self._build_automaton()
        self._build_parsing_table()
        self._sync_public_sets()

    def closure(self, items: Iterable[LR1Item]) -> FrozenSet[LR1Item]:
        """Compute the LR(1) closure of a set of items."""
        closure_set: Set[LR1Item] = set(items)
        queue: Deque[LR1Item] = deque(items)

        while queue:
            item = queue.popleft()
            next_symbol = item.next_symbol()
            if next_symbol and next_symbol in self.grammar.non_terminals:
                lookahead_sequence = list(item.production[item.dot_position + 1 :]) + [
                    item.lookahead
                ]
                first_rest = self.grammar._first_of_sequence(lookahead_sequence, self.first)

                for non_terminal, production in self.grammar.productions:
                    if non_terminal != next_symbol:
                        continue
                    for lookahead in first_rest:
                        if lookahead == self.grammar.epsilon:
                            continue
                        new_item = LR1Item(non_terminal, tuple(production), 0, lookahead)
                        if new_item not in closure_set:
                            closure_set.add(new_item)
                            queue.append(new_item)

        return frozenset(closure_set)

    def goto(self, items: FrozenSet[LR1Item], symbol: Symbol) -> FrozenSet[LR1Item]:
        """Compute the goto set from a state over a symbol."""
        moved: Set[LR1Item] = {
            item.advance() for item in items if item.next_symbol() == symbol
        }
        return self.closure(moved) if moved else frozenset()

    def visualize_automaton(self, filename: str = "automaton_lr1") -> None:
        """Render the full automaton graph if graphviz is available."""
        from .visualization import render_full_automaton

        render_full_automaton(
            states=self.states,
            transitions=self.transitions,
            augmented_start=self.augmented_start,
            grammar=self.grammar,
            filename=filename,
        )

    def visualize_simplified_automaton(
        self, filename: str = "automaton_lr1_simplified"
    ) -> None:
        """Render the automaton using only kernel items."""
        from .visualization import render_kernel_automaton

        render_kernel_automaton(
            states=self.states,
            transitions=self.transitions,
            augmented_start=self.augmented_start,
            grammar=self.grammar,
            filename=filename,
        )

    def print_automaton(self) -> None:
        """Print a textual representation of the LR(1) automaton."""
        print("\n" + "=" * 60)
        print("AUTOMATA LR(1)")
        print("=" * 60)

        for idx, state in enumerate(self.states):
            print(f"\nEstado I{idx}:")
            for item in sorted(state, key=str):
                print(f"  {item}")

            outgoing = [
                (symbol, dest)
                for (src, symbol), dest in self.transitions.items()
                if src == idx
            ]
            if outgoing:
                print("  Transiciones:")
                for symbol, dest in sorted(outgoing):
                    print(f"    {symbol} -> I{dest}")

    def print_parsing_table(self) -> None:
        """Print ACTION/GOTO tables in a compact layout."""
        print("\n" + "=" * 60)
        print("TABLA DE PARSING LR(1)")
        print("=" * 60)

        terminals = sorted(self.grammar.terminals - {self.grammar.epsilon})
        non_terminals = sorted(
            symbol for symbol in self.grammar.non_terminals if symbol != self.augmented_start
        )

        col_width = 12
        header = f"{'Estado':<8} |"
        header += " ACTION ".center(len(terminals) * col_width + max(len(terminals) - 1, 0)) + "|"
        header += " GOTO ".center(len(non_terminals) * col_width + max(len(non_terminals) - 1, 0))
        print(header)

        subheader = f"{'':<8} |"
        for term in terminals:
            subheader += f" {term:<{col_width - 1}}"
        subheader += "|"
        for symbol in non_terminals:
            subheader += f" {symbol:<{col_width - 1}}"
        print(subheader)
        print("-" * len(subheader))

        for state_idx in range(len(self.states)):
            row = f"{state_idx:<8} |"
            for term in terminals:
                cell = ""
                action = self.action_table.get(state_idx, {}).get(term)
                if action:
                    action_type, value = action
                    if action_type == "shift" and value is not None:
                        cell = f"s{value}"
                    elif action_type == "reduce" and value is not None:
                        cell = f"r{value}"
                    elif action_type == "accept":
                        cell = "acc"
                row += f" {cell:<{col_width - 1}}"

            row += "|"
            for symbol in non_terminals:
                target = self.goto_table.get(state_idx, {}).get(symbol, "")
                row += f" {target:<{col_width - 1}}"

            print(row)

        print("\n" + "=" * 60)
        print("PRODUCCIONES (para reduccion)")
        print("=" * 60)
        for idx, (lhs, rhs) in enumerate(self.grammar.productions):
            rhs_str = " ".join(rhs) if rhs else self.grammar.epsilon
            print(f"{idx}: {lhs} -> {rhs_str}")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _build_augmented_start_symbol(self) -> Symbol:
        assert self.original_start_symbol is not None
        candidate = f"{self.original_start_symbol}'"
        existing = self.grammar.non_terminals | self.grammar.terminals
        while candidate in existing:
            candidate += "'"
        return candidate

    def _augment_grammar(self) -> None:
        assert self.original_start_symbol is not None
        self.grammar.productions.insert(
            0, (self.augmented_start, [self.original_start_symbol])
        )
        self.grammar.non_terminals.add(self.augmented_start)
        self.grammar.start_symbol = self.augmented_start

    def _build_automaton(self) -> None:
        self.states = []
        self.transitions = {}

        initial_item = LR1Item(
            self.augmented_start,
            tuple(self.grammar.productions[0][1]),
            0,
            self.grammar.end_marker,
        )
        initial_state = self.closure([initial_item])

        self.states = [initial_state]
        unprocessed: Deque[FrozenSet[LR1Item]] = deque([initial_state])
        state_index = {initial_state: 0}

        while unprocessed:
            current_state = unprocessed.popleft()
            current_idx = state_index[current_state]

            symbols: Set[Symbol] = set()
            for item in current_state:
                symbol = item.next_symbol()
                if symbol:
                    symbols.add(symbol)

            for symbol in symbols:
                goto_state = self.goto(current_state, symbol)
                if not goto_state:
                    continue

                if goto_state not in state_index:
                    state_index[goto_state] = len(self.states)
                    self.states.append(goto_state)
                    unprocessed.append(goto_state)

                self.transitions[(current_idx, symbol)] = state_index[goto_state]

    def _build_parsing_table(self) -> None:
        self.action_table.clear()
        self.goto_table.clear()

        for state_idx, state in enumerate(self.states):
            for item in state:
                next_symbol = item.next_symbol()
                if next_symbol is None:
                    if item.non_terminal == self.augmented_start:
                        self._add_action(state_idx, self.grammar.end_marker, ("accept", None))
                    else:
                        production_index = self._find_production_number(
                            item.non_terminal, item.production
                        )
                        self._add_action(state_idx, item.lookahead, ("reduce", production_index))
                elif next_symbol in self.grammar.terminals:
                    next_state = self.transitions.get((state_idx, next_symbol))
                    if next_state is not None:
                        self._add_action(state_idx, next_symbol, ("shift", next_state))

            for non_terminal in self.grammar.non_terminals:
                target = self.transitions.get((state_idx, non_terminal))
                if target is None:
                    continue
                self.goto_table.setdefault(state_idx, {})[non_terminal] = target

    def _add_action(self, state: int, terminal: Symbol, action: Action) -> None:
        actions = self.action_table.setdefault(state, {})
        previous = actions.get(terminal)
        if previous and previous != action:
            print(f"[WARNING] Conflict in state {state}, terminal '{terminal}':")
            print(f"  Existing: {previous}")
            print(f"  New: {action}")
        else:
            actions[terminal] = action

    def _find_production_number(
        self, non_terminal: Symbol, production: Sequence[Symbol]
    ) -> int:
        for index, (lhs, rhs) in enumerate(self.grammar.productions):
            if lhs == non_terminal and tuple(rhs) == tuple(production):
                return index
        return -1

    def _sync_public_sets(self) -> None:
        if self.source_grammar is None:
            return
        self.source_grammar.terminals = set(self.grammar.terminals)
        filtered_non_terminals = set(self.grammar.non_terminals)
        filtered_non_terminals.discard(self.augmented_start)
        self.source_grammar.non_terminals = filtered_non_terminals
