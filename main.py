# -*- coding: utf-8 -*-
"""
Backend FastAPI para el Parser LR(1)
Proporciona endpoints REST para procesar gramáticas desde el frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import api_helper

app = FastAPI(
    title="Parser LR(1) API",
    description="API REST para análisis sintáctico LR(1)",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Modelos Pydantic para validación de requests
# ============================================================================

class GrammarRequest(BaseModel):
    """
    Modelo para el request de procesamiento de gramática.
    
    Ejemplo:
        {
            "grammar": "S -> C C\nC -> c C\nC -> d",
            "generate_graphs": false
        }
    """
    grammar: str
    generate_graphs: Optional[bool] = False


class ParseStringRequest(BaseModel):
    """
    Modelo para el request de parsing de una cadena.
    
    Ejemplo:
        {
            "grammar": "S -> C C\nC -> c C\nC -> d",
            "input_string": "c c d d"
        }
    """
    grammar: str
    input_string: str


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/")
def root():
    """Endpoint raíz con información de la API."""
    return {
        "message": "Parser LR(1) API",
        "version": "1.0.0",
        "endpoints": {
            "/parse": "POST - Procesar gramática completa",
            "/parse/productions": "POST - Solo producciones",
            "/parse/symbols": "POST - Solo símbolos",
            "/parse/first-follow": "POST - Solo FIRST y FOLLOW",
            "/parse/automaton": "POST - Solo autómata",
            "/parse/table": "POST - Solo tabla de parsing",
            "/parse/closure": "POST - Solo tabla de clausura",
            "/parse/string": "POST - Parsear una cadena de entrada",
            "/health": "GET - Estado del servidor"
        }
    }


@app.get("/health")
def health_check():
    """Endpoint de health check."""
    import shutil
    
    # Verificar si graphviz está instalado
    graphviz_installed = shutil.which("dot") is not None
    
    return {
        "status": "healthy",
        "service": "lr1-parser-api",
        "graphviz_available": graphviz_installed,
        "graphviz_path": shutil.which("dot") if graphviz_installed else None
    }


@app.post("/parse")
def parse_grammar(request: GrammarRequest):
    """
    Procesa una gramática y retorna TODA la información.
    
    Args:
        request: GrammarRequest con la gramática en texto
    
    Returns:
        JSON con toda la información del parser
    
    Example:
        POST /parse
        {
            "grammar": "S -> C C\nC -> c C\nC -> d",
            "generate_graphs": false
        }
    """
    try:
        resultado = api_helper.procesar_gramatica_completo(
            request.grammar,
            generar_graficos=request.generate_graphs
        )
        
        if not resultado["success"]:
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/parse/productions")
def parse_productions(request: GrammarRequest):
    """
    Parsea una gramática y retorna solo las producciones.
    
    Returns:
        JSON con las producciones
    """
    try:
        grammar, parser = api_helper.parsear_gramatica(request.grammar)
        
        if grammar is None:
            raise HTTPException(status_code=400, detail="Error al parsear gramática")
        
        return {
            "success": True,
            "data": {
                "productions": api_helper.obtener_producciones_json(grammar),
                "num_productions": len(grammar.productions)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/parse/symbols")
def parse_symbols(request: GrammarRequest):
    """
    Parsea una gramática y retorna solo los símbolos (terminales y no terminales).
    
    Returns:
        JSON con terminales y no terminales
    """
    try:
        grammar, parser = api_helper.parsear_gramatica(request.grammar)
        
        if grammar is None:
            raise HTTPException(status_code=400, detail="Error al parsear gramática")
        
        return {
            "success": True,
            "data": api_helper.obtener_simbolos_json(grammar, parser)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/parse/first-follow")
def parse_first_follow(request: GrammarRequest):
    """
    Parsea una gramática y retorna los conjuntos FIRST y FOLLOW.
    
    Returns:
        JSON con FIRST y FOLLOW
    """
    try:
        grammar, parser = api_helper.parsear_gramatica(request.grammar)
        
        if grammar is None:
            raise HTTPException(status_code=400, detail="Error al parsear gramática")
        
        return {
            "success": True,
            "data": api_helper.obtener_first_follow_json(grammar, parser)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/parse/automaton")
def parse_automaton(request: GrammarRequest):
    """
    Parsea una gramática y retorna el autómata LR(1).
    
    Returns:
        JSON con estados y transiciones del autómata
    """
    try:
        grammar, parser = api_helper.parsear_gramatica(request.grammar)
        
        if grammar is None:
            raise HTTPException(status_code=400, detail="Error al parsear gramática")
        
        return {
            "success": True,
            "data": api_helper.obtener_automata_json(parser)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/parse/table")
def parse_table(request: GrammarRequest):
    """
    Parsea una gramática y retorna la tabla de parsing (ACTION y GOTO).
    
    Returns:
        JSON con la tabla de parsing
    """
    try:
        grammar, parser = api_helper.parsear_gramatica(request.grammar)
        
        if grammar is None:
            raise HTTPException(status_code=400, detail="Error al parsear gramática")
        
        return {
            "success": True,
            "data": api_helper.obtener_tabla_parsing_json(grammar, parser)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/parse/closure")
def parse_closure(request: GrammarRequest):
    """
    Parsea una gramática y retorna la tabla de clausura.
    
    Returns:
        JSON con la tabla de clausura
    """
    try:
        grammar, parser = api_helper.parsear_gramatica(request.grammar)
        
        if grammar is None:
            raise HTTPException(status_code=400, detail="Error al parsear gramática")
        
        return {
            "success": True,
            "data": api_helper.obtener_tabla_clausura_json(parser)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/parse/graphs")
def parse_graphs(request: GrammarRequest):
    """
    Parsea una gramática y retorna los gráficos en base64.
    
    Returns:
        JSON con imágenes en base64
    """
    try:
        grammar, parser = api_helper.parsear_gramatica(request.grammar)
        
        if grammar is None:
            raise HTTPException(status_code=400, detail="Error al parsear gramática")
        
        return {
            "success": True,
            "data": api_helper.generar_graficos_base64(parser)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/parse/string")
def parse_string(request: ParseStringRequest):
    """
    Parsea una cadena de entrada usando la gramática proporcionada.
    Retorna el proceso paso a paso del parsing.
    
    Args:
        request: ParseStringRequest con la gramática y la cadena a parsear
    
    Returns:
        JSON con los pasos del parsing y el resultado
    
    Example:
        POST /parse/string
        {
            "grammar": "S -> C C\nC -> c C\nC -> d",
            "input_string": "c c d d"
        }
    """
    try:
        # Parsear la gramática
        grammar, parser = api_helper.parsear_gramatica(request.grammar)
        
        if grammar is None:
            raise HTTPException(status_code=400, detail="Error al parsear gramática")
        
        # Parsear la cadena
        resultado = api_helper.parsear_cadena(grammar, parser, request.input_string)
        
        if not resultado["success"] and resultado["error"]:
            # Si hay error de sintaxis, retornar con éxito pero indicando rechazo
            return {
                "success": True,
                "data": resultado
            }
        
        return {
            "success": True,
            "data": resultado
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


# ============================================================================
# Ejecutar servidor
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Leer puerto de variable de entorno (Railway) o usar 8000 por defecto
    port = int(os.getenv("PORT", 8000))
    
    # Detectar si estamos en producción (Railway) o desarrollo local
    is_production = os.getenv("RAILWAY_ENVIRONMENT") is not None
    
    print("=" * 80)
    print("Iniciando servidor FastAPI - Parser LR(1)")
    print("=" * 80)
    print(f"\nPuerto: {port}")
    print(f"Modo: {'Producción' if is_production else 'Desarrollo'}")
    print("\nEndpoints disponibles:")
    print(f"  • http://localhost:{port}/docs       - Documentación interactiva (Swagger)")
    print(f"  • http://localhost:{port}/redoc      - Documentación alternativa (ReDoc)")
    print(f"  • http://localhost:{port}/parse      - Endpoint principal")
    print("=" * 80)
    
    # En producción, no usar reload para evitar problemas con Railway
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=not is_production)
