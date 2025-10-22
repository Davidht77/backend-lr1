"""Graphviz visualization helpers for LR(1) automata."""
from __future__ import annotations

from typing import Dict, Iterable, List

try:
    import graphviz  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    graphviz = None

from .grammar import Grammar
from .items import LR1Item


def _ensure_graphviz() -> None:
    if graphviz is None:
        print("[WARNING] Graphviz is not installed. Skipping graph generation.")
        raise RuntimeError("graphviz not available")


def render_full_automaton(
    *,
    states: Iterable[Iterable[LR1Item]],
    transitions: Dict[tuple[int, str], int],
    augmented_start: str,
    grammar: Grammar,
    filename: str,
) -> None:
    """Render the full LR(1) automaton showing kernel and closure items."""
    try:
        _ensure_graphviz()
    except RuntimeError:
        return

    dot = graphviz.Digraph(comment="Automa LR1 - Completo")
    dot.attr(rankdir="LR")
    dot.attr("node", shape="rectangle", style="rounded", fontsize="8")

    for idx, state in enumerate(states):
        kernel_items: List[str] = []
        closure_items: List[str] = []

        for item in state:
            is_kernel = item.dot_position > 0 or (
                idx == 0 and item.non_terminal == augmented_start
            )
            target_list = kernel_items if (is_kernel or item.non_terminal == augmented_start) else closure_items
            target_list.append(str(item))

        all_items = sorted(kernel_items) + sorted(closure_items)
        label_lines = all_items[:10]
        if len(all_items) > 10:
            label_lines.append(f"... (+{len(all_items) - 10} items)")
        label = "\\n".join(label_lines) if label_lines else "(vacio)"

        is_accepting = any(
            item.non_terminal == augmented_start and item.next_symbol() is None
            for item in state
        )
        if is_accepting:
            dot.node(
                str(idx),
                label,
                shape="doublecircle",
                style="rounded,filled",
                fillcolor="lightgreen",
            )
        else:
            dot.node(str(idx), label)

    for (src, symbol), dest in transitions.items():
        dot.edge(str(src), str(dest), label=symbol, fontsize="9")

    try:
        dot.render(filename, format="png", cleanup=True)
        print(f"[OK] Grafico del automata guardado como '{filename}.png'")
    except Exception as exc:  # pragma: no cover - graphviz runtime errors
        print(f"[WARNING] No se pudo generar el grafico: {exc}")
        print("   Revisa la instalacion de Graphviz: https://graphviz.org/download/")


def render_kernel_automaton(
    *,
    states: Iterable[Iterable[LR1Item]],
    transitions: Dict[tuple[int, str], int],
    augmented_start: str,
    grammar: Grammar,
    filename: str,
) -> None:
    """Render the automaton focusing on kernel items only."""
    try:
        _ensure_graphviz()
    except RuntimeError:
        return

    dot = graphviz.Digraph(comment="Automa LR1 - Items Kernel")
    dot.attr(rankdir="LR")
    dot.attr("node", shape="rectangle", style="rounded", fontsize="9")

    for idx, state in enumerate(states):
        kernel_items: List[str] = []
        for item in state:
            is_kernel_item = (
                (idx == 0 and item.non_terminal == augmented_start and item.dot_position == 0)
                or (idx != 0 and item.dot_position > 0)
            )
            if is_kernel_item:
                symbols = list(item.production)
                symbols.insert(item.dot_position, ".")
                production_str = " ".join(symbols) if symbols else "."
                kernel_items.append(f"[{item.non_terminal} -> {production_str}, {item.lookahead}]")

        kernel_items.sort()
        lines = kernel_items[:8]
        if len(kernel_items) > 8:
            lines.append(f"... (+{len(kernel_items) - 8} items)")
        label = "\\n".join(lines) if lines else "(sin items kernel)"

        is_accepting = any(
            item.non_terminal == augmented_start and item.next_symbol() is None
            for item in state
        )
        if is_accepting:
            dot.node(
                str(idx),
                label,
                shape="doublecircle",
                style="rounded,filled",
                fillcolor="lightgreen",
            )
        else:
            dot.node(str(idx), label)

    for (src, symbol), dest in transitions.items():
        dot.edge(str(src), str(dest), label=symbol, fontsize="9")

    try:
        dot.render(filename, format="png", cleanup=True)
        print(f"[OK] Grafico con items kernel guardado como '{filename}.png'")
    except Exception as exc:  # pragma: no cover - graphviz runtime errors
        print(f"[WARNING] No se pudo generar el grafico kernel: {exc}")
        print("   Revisa la instalacion de Graphviz: https://graphviz.org/download/")
