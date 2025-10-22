"""LR(1) item definitions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

Symbol = str


@dataclass(frozen=True)
class LR1Item:
    """Representation of a single LR(1) item [A -> alpha . beta, a]."""

    non_terminal: Symbol
    production: Tuple[Symbol, ...]
    dot_position: int
    lookahead: Symbol

    def next_symbol(self) -> Symbol | None:
        """Return the symbol immediately after the dot, if any."""
        if 0 <= self.dot_position < len(self.production):
            return self.production[self.dot_position]
        return None

    def advance(self) -> "LR1Item":
        """Return a new item with the dot advanced by one position."""
        if self.dot_position >= len(self.production):
            return self
        return LR1Item(
            self.non_terminal,
            self.production,
            self.dot_position + 1,
            self.lookahead,
        )

    def __repr__(self) -> str:
        symbols = list(self.production)
        symbols.insert(self.dot_position, ".")
        production_str = " ".join(symbols)
        return f"[{self.non_terminal} -> {production_str}, {self.lookahead}]"
