# -*- coding: utf-8 -*-
"""
Módulo RegularGrammarAFNVisualizer
Define el visualizador de AFN y AFD para gramáticas regulares.
"""

import graphviz


class RegularGrammarAFNVisualizer:
    """Visualizador de AFN y AFD para gramáticas regulares"""
    
    def __init__(self, grammar):
        """
        Inicializa el visualizador con una gramática.
        
        Args:
            grammar: Objeto Grammar con las producciones
        """
        self.grammar = grammar
        self.states = set()
        self.transitions = {}
        self.final_states = set()
        
    def _analyze_grammar(self):
        """Analiza la gramática para identificar estados y transiciones"""
        self.states = set(self.grammar.non_terminals)
        self.states.add("F")  # Estado final
        self.final_states.add("F")
        
        for nt, prod in self.grammar.productions:
            if not prod or prod[0] == self.grammar.epsilon:
                # Producción epsilon: A -> ε (A es estado final)
                self.final_states.add(nt)
            elif len(prod) == 1:
                # Forma: A -> a (transición al estado final)
                if (nt, prod[0]) not in self.transitions:
                    self.transitions[(nt, prod[0])] = []
                if "F" not in self.transitions[(nt, prod[0])]:
                    self.transitions[(nt, prod[0])].append("F")
            elif len(prod) == 2:
                # Forma: A -> aB (transición de A a B con símbolo a)
                if (nt, prod[0]) not in self.transitions:
                    self.transitions[(nt, prod[0])] = []
                if prod[1] not in self.transitions[(nt, prod[0])]:
                    self.transitions[(nt, prod[0])].append(prod[1])
    
    def visualize_afn(self, filename="afn_grammar"):
        """
        Genera visualización del AFN de la gramática regular.
        
        Args:
            filename: Nombre del archivo de salida (sin extensión)
        """
        self._analyze_grammar()
        
        dot = graphviz.Digraph(comment="AFN de la Gramática Regular")
        dot.attr(rankdir="LR")
        dot.attr("node", shape="circle", fontsize="12")
        
        # Marcar estado inicial
        initial_state = self.grammar.start_symbol
        dot.node("START", shape="point", width="0")
        dot.edge("START", initial_state, label="")
        
        # Añadir estados normales
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape="doublecircle", style="filled", 
                        fillcolor="lightgreen")
            else:
                dot.node(state, shape="circle")
        
        # Añadir transiciones
        for (src, symbol), dest_list in self.transitions.items():
            for dest in dest_list:
                dot.edge(src, dest, label=symbol, fontsize="10")
        
        # Guardar
        try:
            dot.render(filename, format="png", cleanup=True)
            print(f"\n[OK] AFN generado: '{filename}.png'")
        except Exception as e:
            print(f"\n[WARNING] No se pudo generar el AFN: {e}")
    
    def visualize_afd(self, filename="afd_grammar"):
        """
        Genera visualización del AFD de la gramática regular (determinización del AFN).
        
        Args:
            filename: Nombre del archivo de salida (sin extensión)
        """
        self._analyze_grammar()
        
        # Para gramáticas regulares lineales por la derecha, el AFD es similar al AFN
        # (ya que no hay epsilon-transiciones ni no-determinismo en las producciones típicas)
        
        dot = graphviz.Digraph(comment="AFD de la Gramática Regular")
        dot.attr(rankdir="LR")
        dot.attr("node", shape="circle", fontsize="12")
        
        # Marcar estado inicial
        initial_state = self.grammar.start_symbol
        dot.node("START", shape="point", width="0")
        dot.edge("START", initial_state, label="", style="bold")
        
        # Añadir estados
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape="doublecircle", style="filled", 
                        fillcolor="lightblue", penwidth="2")
            else:
                dot.node(state, shape="circle", penwidth="1.5")
        
        # Añadir transiciones (agrupadas por símbolo si hay múltiples destinos)
        for (src, symbol), dest_list in self.transitions.items():
            if len(dest_list) == 1:
                dot.edge(src, dest_list[0], label=symbol, fontsize="10", penwidth="1.5")
            else:
                # Múltiples destinos (indica no-determinismo, necesita determinización)
                for i, dest in enumerate(dest_list):
                    label = f"{symbol}[{i+1}]"
                    dot.edge(src, dest, label=label, fontsize="10", 
                            style="dashed", penwidth="1.5")
        
        # Guardar
        try:
            dot.render(filename, format="png", cleanup=True)
            print(f"[OK] AFD generado: '{filename}.png'")
        except Exception as e:
            print(f"[WARNING] No se pudo generar el AFD: {e}")
    
    def print_automaton_info(self):
        """Imprime información del autómata"""
        self._analyze_grammar()
        
        print("\n" + "=" * 60)
        print("INFORMACIÓN DEL AUTÓMATA FINITO")
        print("=" * 60)
        
        print(f"\n📍 Estado inicial: {self.grammar.start_symbol}")
        print(f"📊 Total de estados: {len(self.states)}")
        print(f"✅ Estados finales: {sorted(self.final_states)}")
        print(f"🔄 Transiciones: {len(self.transitions)}")
        
        print("\n🔗 Detalle de transiciones:")
        for (src, symbol), dest_list in sorted(self.transitions.items()):
            for dest in dest_list:
                print(f"   δ({src}, {symbol}) = {dest}")
        
        # Verificar si es determinista
        is_deterministic = all(len(dest_list) == 1 
                               for dest_list in self.transitions.values())
        
        print(f"\n🎯 Tipo de autómata: {'AFD (Determinista)' if is_deterministic else 'AFN (No Determinista)'}")
