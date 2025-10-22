# -*- coding: utf-8 -*-
"""
API Helper - Funciones para integración con Frontend
Facilita la comunicación entre frontend y el parser LR(1)
"""

from lr1_parser import Grammar, LR1Parser
from demo import parsear_gramatica_desde_texto
import json


def procesar_gramatica_api(texto_gramatica):
    """
    Procesa una gramática desde texto y retorna resultados en formato JSON-friendly.
    
    Args:
        texto_gramatica: String con producciones, formato:
                        "S -> C C\nC -> c C\nC -> d"
    
    Returns:
        dict con estructura:
        {
            "success": bool,
            "error": str o None,
            "grammar": {
                "productions": [...],
                "terminals": [...],
                "non_terminals": [...]
            },
            "first": {...},
            "follow": {...},
            "states": int,
            "conflicts": [...]
        }
    """
    resultado = {
        "success": False,
        "error": None,
        "grammar": None,
        "first": None,
        "follow": None,
        "states": 0,
        "conflicts": []
    }
    
    try:
        # Parsear gramática
        grammar = parsear_gramatica_desde_texto(texto_gramatica)
        
        if grammar is None:
            resultado["error"] = "No se pudo parsear la gramática"
            return resultado
        
        # Construir parser
        parser = LR1Parser(grammar)
        parser.build()
        
        # Recopilar información de la gramática
        resultado["grammar"] = {
            "productions": [
                {
                    "id": i,
                    "non_terminal": nt,
                    "production": prod if prod else ["epsilon"]
                }
                for i, (nt, prod) in enumerate(grammar.productions)
            ],
            "terminals": sorted(list(grammar.terminals - {grammar.epsilon})),
            "non_terminals": sorted(list(grammar.non_terminals))
        }
        
        # FIRST sets
        resultado["first"] = {
            nt: sorted(list(parser.first.get(nt, set())))
            for nt in grammar.non_terminals
        }
        
        # FOLLOW sets
        resultado["follow"] = {
            nt: sorted(list(parser.follow.get(nt, set())))
            for nt in grammar.non_terminals
        }
        
        # Estados
        resultado["states"] = len(parser.states)
        
        # Detectar conflictos (buscar en tabla de parsing)
        conflictos = []
        for state_idx in range(len(parser.states)):
            if state_idx in parser.parsing_table["action"]:
                for terminal, actions in parser.parsing_table["action"][state_idx].items():
                    # Si hay múltiples acciones, es un conflicto
                    # (esto requeriría modificar el parser para detectar)
                    pass
        
        resultado["conflicts"] = conflictos
        resultado["success"] = True
        
    except Exception as e:
        resultado["error"] = str(e)
    
    return resultado


def convertir_gramatica_a_json(grammar, parser):
    """
    Convierte una gramática y su parser a formato JSON.
    
    Args:
        grammar: Objeto Grammar
        parser: Objeto LR1Parser
    
    Returns:
        str: JSON con toda la información
    """
    datos = {
        "productions": [
            {
                "id": i,
                "lhs": nt,
                "rhs": prod if prod else ["ε"]
            }
            for i, (nt, prod) in enumerate(grammar.productions)
        ],
        "terminals": sorted(list(grammar.terminals - {grammar.epsilon})),
        "non_terminals": sorted(list(grammar.non_terminals)),
        "first": {
            nt: sorted(list(parser.first.get(nt, set())))
            for nt in grammar.non_terminals
        },
        "follow": {
            nt: sorted(list(parser.follow.get(nt, set())))
            for nt in grammar.non_terminals
        },
        "num_states": len(parser.states),
        "parsing_table": {
            "action": {
                str(state): {
                    term: {"type": action[0], "value": action[1]}
                    for term, action in actions.items()
                }
                for state, actions in parser.parsing_table["action"].items()
            },
            "goto": {
                str(state): gotos
                for state, gotos in parser.parsing_table["goto"].items()
            }
        }
    }
    
    return json.dumps(datos, indent=2, ensure_ascii=False)


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 80)
    print("API HELPER - Test")
    print("=" * 80)
    
    # Ejemplo de gramática desde frontend
    gramatica_frontend = """S -> C C
C -> c C
C -> d"""
    
    print("\nGramática recibida del frontend:")
    print(gramatica_frontend)
    
    # Procesar
    resultado = procesar_gramatica_api(gramatica_frontend)
    
    print("\n" + "=" * 80)
    print("Resultado (formato JSON-friendly):")
    print("=" * 80)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    if resultado["success"]:
        print("\n✓ Gramática procesada exitosamente")
        print(f"✓ Producciones: {len(resultado['grammar']['productions'])}")
        print(f"✓ Estados del autómata: {resultado['states']}")
    else:
        print(f"\n✗ Error: {resultado['error']}")
