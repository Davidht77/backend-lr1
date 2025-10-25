# -*- coding: utf-8 -*-
"""
API Helper - Funciones para integración con FastAPI Backend
Convierte toda la salida del parser a formato JSON para el frontend
"""

from lr1_parser import Grammar, LR1Parser
import json
import base64
import os


def parsear_gramatica_desde_texto_interno(texto):
    """Parsea una gramática desde texto (función interna)."""
    grammar = Grammar()
    lineas = texto.strip().split('\n')
    
    for i, linea in enumerate(lineas, 1):
        linea = linea.strip()
        
        if not linea or linea.startswith('#'):
            continue
        
        separador = None
        if '->' in linea:
            separador = '->'
        elif ':' in linea:
            separador = ':'
        else:
            print(f"[ERROR] Línea {i}: Formato inválido: {linea}")
            return None
        
        partes = linea.split(separador, 1)
        if len(partes) != 2:
            print(f"[ERROR] Línea {i}: No se pudo parsear: {linea}")
            return None
        
        no_terminal = partes[0].strip()
        produccion_str = partes[1].strip()
        
        if not no_terminal:
            print(f"[ERROR] Línea {i}: No terminal vacío")
            return None
        
        if not produccion_str or produccion_str.lower() == 'epsilon' or produccion_str == 'ε':
            produccion = []
        else:
            produccion = produccion_str.split()
        
        grammar.add_production(no_terminal, produccion)
    
    if len(grammar.productions) == 0:
        print("[ERROR] No se encontraron producciones válidas")
        return None
    
    return grammar


def parsear_gramatica(texto_gramatica):
    """Parsea una gramática desde texto y construye el parser."""
    try:
        grammar = parsear_gramatica_desde_texto_interno(texto_gramatica)
        if grammar is None:
            return None, None
        
        parser = LR1Parser(grammar)
        parser.build()
        
        return grammar, parser
    except Exception as e:
        print(f"Error al parsear gramática: {e}")
        return None, None


def obtener_producciones_json(grammar):
    """Convierte las producciones a formato JSON."""
    producciones = []
    for i, (nt, prod) in enumerate(grammar.productions):
        producciones.append({
            "id": i,
            "lhs": nt,
            "rhs": prod if prod else ["ε"],
            "rhs_str": " ".join(prod) if prod else "ε"
        })
    return producciones


def obtener_simbolos_json(grammar, parser):
    """Obtiene terminales y no terminales en formato JSON."""
    return {
        "terminals": sorted(list(grammar.terminals - {grammar.epsilon, grammar.end_marker})),
        "end_marker": grammar.end_marker,
        "non_terminals": sorted(list(grammar.non_terminals - {parser.augmented_start})),
        "start_symbol": list(grammar.non_terminals)[0] if grammar.non_terminals else None,
        "augmented_start": parser.augmented_start
    }


def obtener_first_follow_json(grammar, parser):
    """Obtiene los conjuntos FIRST y FOLLOW en formato JSON."""
    first_dict = {}
    follow_dict = {}
    
    for nt in grammar.non_terminals:
        if nt != parser.augmented_start:
            first_dict[nt] = sorted(list(parser.first.get(nt, set())))
            follow_dict[nt] = sorted(list(parser.follow.get(nt, set())))
    
    return {
        "first": first_dict,
        "follow": follow_dict
    }


def obtener_automata_json(parser):
    """Convierte el autómata LR(1) a formato JSON."""
    states_info = []
    
    for idx, state in enumerate(parser.states):
        kernel_items = []
        all_items = []
        
        for item in state:
            item_str = str(item)
            all_items.append(item_str)
            
            is_kernel = False
            if idx == 0:
                if item.non_terminal == parser.augmented_start and item.dot_position == 0:
                    is_kernel = True
            else:
                if item.dot_position > 0:
                    is_kernel = True
            
            if is_kernel:
                kernel_items.append(item_str)
        
        is_accept = any(
            item.non_terminal == parser.augmented_start and 
            item.next_symbol() is None
            for item in state
        )
        
        states_info.append({
            "id": idx,
            "items": all_items,
            "kernel_items": kernel_items,
            "is_accept": is_accept,
            "num_items": len(all_items)
        })
    
    transitions = []
    for (src, symbol), dest in parser.transitions.items():
        transitions.append({
            "from": src,
            "to": dest,
            "symbol": symbol
        })
    
    return {
        "num_states": len(parser.states),
        "states": states_info,
        "transitions": transitions
    }


def obtener_tabla_parsing_json(grammar, parser):
    """Convierte la tabla de parsing (ACTION y GOTO) a formato JSON con metadatos para visualización."""
    action_table = {}
    goto_table = {}
    
    # Preparar action con formato visual mejorado
    for state_idx, actions in parser.parsing_table["action"].items():
        action_table[str(state_idx)] = {}
        for terminal, (action_type, value) in actions.items():
            entry = {
                "type": action_type,
                "value": value
            }
            
            # Añadir display text y color según tipo
            if action_type == "shift":
                entry["display"] = f"s{value}"
                entry["color"] = "green"
            elif action_type == "reduce":
                # Obtener la producción para mostrar
                prod_nt, prod_rhs = grammar.productions[value]
                rhs_str = " ".join(prod_rhs) if prod_rhs else "ε"
                entry["display"] = f"r{value}"
                entry["production"] = f"{prod_nt} → {rhs_str}"
                entry["color"] = "red"
            elif action_type == "accept":
                entry["display"] = "acc"
                entry["color"] = "blue"
            
            action_table[str(state_idx)][terminal] = entry
    
    # Preparar goto con formato visual
    for state_idx, gotos in parser.parsing_table["goto"].items():
        goto_table[str(state_idx)] = {}
        for non_terminal, target_state in gotos.items():
            goto_table[str(state_idx)][non_terminal] = {
                "type": "goto",
                "value": target_state,
                "display": str(target_state),
                "color": "purple"
            }
    
    terminals = sorted(list(grammar.terminals - {grammar.epsilon}))
    non_terminals = sorted(list(grammar.non_terminals - {parser.augmented_start}))
    
    # Obtener lista de producciones para referencia
    productions_list = []
    for i, (nt, prod) in enumerate(grammar.productions):
        rhs_str = " ".join(prod) if prod else "ε"
        productions_list.append({
            "id": i,
            "lhs": nt,
            "rhs": prod if prod else ["ε"],
            "display": f"{nt} → {rhs_str}"
        })
    
    return {
        "action": action_table,
        "goto": goto_table,
        "headers": {
            "terminals": terminals,
            "non_terminals": non_terminals
        },
        "productions": productions_list,
        "num_states": len(parser.states)
    }


def obtener_tabla_clausura_json(parser):
    """Convierte la tabla de clausura a formato JSON (mejorado para frontend)."""
    clausuras = []
    
    # Estado inicial
    initial_state = parser.states[0]
    initial_kernel = []
    initial_closure = []
    
    for item in initial_state:
        item_str = str(item)
        if item.non_terminal == parser.augmented_start and item.dot_position == 0:
            initial_kernel.append(item_str)
        else:
            initial_closure.append(item_str)
    
    # Todos los items para el estado inicial
    all_initial_items = initial_kernel + initial_closure
    
    clausuras.append({
        "state_id": 0,
        "goto_label": "INITIAL",
        "kernel_items": initial_kernel,
        "kernel_display": "; ".join(initial_kernel),
        "closure_items": all_initial_items,
        "closure_display": "; ".join(all_initial_items[:5]) + 
                          (f"; ... (+{len(all_initial_items) - 5})" if len(all_initial_items) > 5 else ""),
        "num_items": len(initial_state),
        "goto_transitions": None
    })
    
    # Mapeo inverso de transiciones
    reverse_transitions = {}
    for (src, symbol), dest in parser.transitions.items():
        if dest not in reverse_transitions:
            reverse_transitions[dest] = []
        reverse_transitions[dest].append((src, symbol))
    
    # Resto de estados
    for state_idx in range(1, len(parser.states)):
        state = parser.states[state_idx]
        
        # Separar kernel y closure
        kernel = []
        closure_extra = []
        
        for item in state:
            item_str = str(item)
            if item.dot_position > 0:
                kernel.append(item_str)
            else:
                closure_extra.append(item_str)
        
        # Información de goto
        goto_info = reverse_transitions.get(state_idx, [])
        goto_labels = [f"goto({src}, {sym})" for src, sym in goto_info]
        goto_label = ", ".join(goto_labels) if goto_labels else ""
        
        # Todos los items
        all_items = kernel + closure_extra
        
        # Display compacto
        kernel_display = "; ".join(kernel)
        
        # Mostrar hasta 5 items en closure_display
        closure_preview = all_items[:5]
        closure_display = "; ".join(closure_preview)
        if len(all_items) > 5:
            closure_display += f"; ... (+{len(all_items) - 5} más)"
        
        clausuras.append({
            "state_id": state_idx,
            "goto_label": goto_label,
            "kernel_items": kernel,
            "kernel_display": kernel_display,
            "closure_items": all_items,
            "closure_display": closure_display,
            "num_items": len(state),
            "goto_transitions": goto_info
        })
    
    return clausuras


def generar_graficos_base64(parser, filename_prefix="automaton_api"):
    """Genera los gráficos del autómata LR(1) y los convierte a base64."""
    import traceback
    
    resultado = {
        "automaton_afn": None,  # AFD = solo kernel
        "automaton_afd": None   # AFN = clausura completa
    }
    
    try:
        # AFD - Autómata con solo items kernel
        afn_path = f"{filename_prefix}_afn"
        print(f"[DEBUG] Generando AFD en: {afn_path}")
        parser.visualize_automaton(afn_path)
        
        expected_file = f"{afn_path}.png"
        print(f"[DEBUG] Buscando archivo: {expected_file}")
        print(f"[DEBUG] Existe: {os.path.exists(expected_file)}")
        
        if os.path.exists(expected_file):
            with open(expected_file, "rb") as f:
                data = f.read()
                resultado["automaton_afn"] = base64.b64encode(data).decode('utf-8')
                print(f"[DEBUG] AFD generado exitosamente, tamaño: {len(resultado['automaton_afn'])} chars")
            os.remove(expected_file)
        else:
            print(f"[ERROR] No se encontró el archivo: {expected_file}")
    except Exception as e:
        print(f"[ERROR] Error generando AFD: {e}")
        traceback.print_exc()
    
    try:
        # AFN - Autómata con clausura completa (todos los items)
        afd_path = f"{filename_prefix}_afd"
        print(f"[DEBUG] Generando AFN en: {afd_path}")
        parser.visualize_simplified_automaton(afd_path)
        
        kernel_file = f"{afd_path}_kernel.png"
        print(f"[DEBUG] Buscando archivo: {kernel_file}")
        print(f"[DEBUG] Existe: {os.path.exists(kernel_file)}")
        
        if os.path.exists(kernel_file):
            with open(kernel_file, "rb") as f:
                data = f.read()
                resultado["automaton_afd"] = base64.b64encode(data).decode('utf-8')
                print(f"[DEBUG] AFN generado exitosamente, tamaño: {len(resultado['automaton_afd'])} chars")
            os.remove(kernel_file)
        else:
            print(f"[ERROR] No se encontró el archivo: {kernel_file}")
    except Exception as e:
        print(f"[ERROR] Error generando AFN: {e}")
        traceback.print_exc()
    
    return resultado


def procesar_gramatica_completo(texto_gramatica, generar_graficos=False):
    """Procesa una gramática y retorna TODA la información en formato JSON."""
    resultado = {
        "success": False,
        "error": None,
        "data": None
    }
    
    try:
        grammar, parser = parsear_gramatica(texto_gramatica)
        
        if grammar is None or parser is None:
            resultado["error"] = "No se pudo parsear la gramática. Verifica el formato."
            return resultado
        
        data = {
            "grammar": {
                "productions": obtener_producciones_json(grammar),
                "num_productions": len(grammar.productions)
            },
            "symbols": obtener_simbolos_json(grammar, parser),
            "first_follow": obtener_first_follow_json(grammar, parser),
            "automaton": obtener_automata_json(parser),
            "parsing_table": obtener_tabla_parsing_json(grammar, parser),
            "closure_table": obtener_tabla_clausura_json(parser)
        }
        
        if generar_graficos:
            data["graphs"] = generar_graficos_base64(parser)
        
        resultado["success"] = True
        resultado["data"] = data
        
    except Exception as e:
        resultado["error"] = f"Error al procesar gramática: {str(e)}"
    
    return resultado


def parsear_cadena(grammar, parser, input_string):
    """
    Parsea una cadena usando el parser LR(1) y retorna el proceso paso a paso.
    
    Args:
        grammar: Gramática del parser
        parser: Parser LR(1) construido
        input_string: Cadena a parsear (tokens separados por espacios)
    
    Returns:
        dict con el resultado del parsing y los pasos
    """
    resultado = {
        "success": False,
        "accepted": False,
        "error": None,
        "steps": [],
        "summary": {}
    }
    
    try:
        # Tokenizar la entrada
        tokens = input_string.strip().split() if input_string.strip() else []
        tokens.append(grammar.end_marker)  # Añadir $
        
        # Inicializar la pila y el índice
        stack = [0]  # Pila de estados
        symbol_stack = []  # Pila de símbolos (para visualización)
        input_idx = 0
        step_num = 0
        
        while True:
            step_num += 1
            current_state = stack[-1]
            current_token = tokens[input_idx]
            
            # Registrar el paso actual
            step = {
                "step": step_num,
                "stack": list(stack),
                "symbol_stack": list(symbol_stack),
                "remaining_input": " ".join(tokens[input_idx:]),
                "current_state": current_state,
                "current_token": current_token,
                "action": None,
                "action_detail": None
            }
            
            # Buscar la acción en la tabla
            if current_state not in parser.parsing_table["action"]:
                resultado["error"] = f"Estado {current_state} no tiene entradas en la tabla ACTION"
                resultado["steps"].append(step)
                break
            
            state_actions = parser.parsing_table["action"][current_state]
            
            if current_token not in state_actions:
                resultado["error"] = f"Error de sintaxis: token '{current_token}' inesperado en estado {current_state}"
                resultado["steps"].append(step)
                break
            
            action_type, action_value = state_actions[current_token]
            
            if action_type == "shift":
                step["action"] = "shift"
                step["action_detail"] = f"Desplazar a estado {action_value}"
                resultado["steps"].append(step)
                
                # Realizar shift
                symbol_stack.append(current_token)
                stack.append(action_value)
                input_idx += 1
                
            elif action_type == "reduce":
                prod_nt, prod_rhs = grammar.productions[action_value]
                rhs_str = " ".join(prod_rhs) if prod_rhs else "ε"
                
                step["action"] = "reduce"
                step["action_detail"] = f"Reducir por producción {action_value}: {prod_nt} → {rhs_str}"
                step["production_id"] = action_value
                step["production_lhs"] = prod_nt
                step["production_rhs"] = prod_rhs if prod_rhs else ["ε"]
                resultado["steps"].append(step)
                
                # Realizar reduce
                # Sacar |rhs| símbolos de la pila
                pop_count = len(prod_rhs) if prod_rhs else 0
                
                for _ in range(pop_count):
                    if stack:
                        stack.pop()
                    if symbol_stack:
                        symbol_stack.pop()
                
                # Estado después de sacar
                state_after_pop = stack[-1] if stack else 0
                
                # Buscar GOTO
                if state_after_pop not in parser.parsing_table["goto"]:
                    resultado["error"] = f"Estado {state_after_pop} no tiene entradas en la tabla GOTO"
                    break
                
                goto_entries = parser.parsing_table["goto"][state_after_pop]
                
                if prod_nt not in goto_entries:
                    resultado["error"] = f"No hay transición GOTO para {prod_nt} desde estado {state_after_pop}"
                    break
                
                next_state = goto_entries[prod_nt]
                
                # Push del no terminal y el nuevo estado
                symbol_stack.append(prod_nt)
                stack.append(next_state)
                
            elif action_type == "accept":
                step["action"] = "accept"
                step["action_detail"] = "Cadena aceptada ✓"
                resultado["steps"].append(step)
                resultado["accepted"] = True
                resultado["success"] = True
                break
            
            else:
                resultado["error"] = f"Acción desconocida: {action_type}"
                resultado["steps"].append(step)
                break
            
            # Seguridad: evitar loops infinitos
            if step_num > 1000:
                resultado["error"] = "Demasiados pasos, posible loop infinito"
                break
        
        # Resumen
        resultado["summary"] = {
            "total_steps": len(resultado["steps"]),
            "input_tokens": tokens[:-1],  # Sin el $
            "input_length": len(tokens) - 1,
            "accepted": resultado["accepted"]
        }
        
        if not resultado["success"] and not resultado["error"]:
            resultado["error"] = "Parsing terminado sin aceptar la cadena"
        
    except Exception as e:
        resultado["error"] = f"Error durante el parsing: {str(e)}"
    
    return resultado


if __name__ == "__main__":
    print("=" * 80)
    print("API HELPER - Test de funciones")
    print("=" * 80)
    
    gramatica_test = """S -> C C
C -> c C
C -> d"""
    
    print("\nGramática de prueba:")
    print(gramatica_test)
    print()
    
    resultado = procesar_gramatica_completo(gramatica_test, generar_graficos=False)
    
    if resultado["success"]:
        print("✓ Procesamiento exitoso!")
        print(f"\nProducciones: {resultado['data']['grammar']['num_productions']}")
        print(f"Estados: {resultado['data']['automaton']['num_states']}")
        print(f"Transiciones: {len(resultado['data']['automaton']['transitions'])}")
        
        print("\n" + "=" * 80)
        print("JSON completo (primeras 50 líneas):")
        print("=" * 80)
        json_str = json.dumps(resultado, indent=2, ensure_ascii=False)
        lines = json_str.split('\n')
        for line in lines[:50]:
            print(line)
        if len(lines) > 50:
            print(f"\n... (+{len(lines) - 50} líneas más)")
    else:
        print(f"✗ Error: {resultado['error']}")
