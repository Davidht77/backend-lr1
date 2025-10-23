# Guía de uso del Backend FastAPI - Parser LR(1)

## 🚀 Instalación y Setup

```bash
# 1. Instalar dependencias
pip install -r requirements_api.txt

# 2. Iniciar el servidor
python main.py

# El servidor estará disponible en: http://localhost:8000
```

## 📚 Documentación Interactiva

Una vez iniciado el servidor, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints Disponibles

### 1. `/parse` - Procesamiento Completo (Recomendado)

Procesa una gramática y retorna **TODA** la información.

**Request:**
```json
POST http://localhost:8000/parse
Content-Type: application/json

{
  "grammar": "S -> C C\nC -> c C\nC -> d",
  "generate_graphs": false
}
```

**Response:**
```json
{
  "success": true,
  "error": null,
  "data": {
    "grammar": {
      "productions": [
        {"id": 0, "lhs": "S", "rhs": ["C", "C"], "rhs_str": "C C"},
        {"id": 1, "lhs": "C", "rhs": ["c", "C"], "rhs_str": "c C"},
        {"id": 2, "lhs": "C", "rhs": ["d"], "rhs_str": "d"}
      ],
      "num_productions": 3
    },
    "symbols": {
      "terminals": ["c", "d"],
      "end_marker": "$",
      "non_terminals": ["C", "S"],
      "start_symbol": "S",
      "augmented_start": "S'"
    },
    "first_follow": {
      "first": {
        "S": ["c", "d"],
        "C": ["c", "d"]
      },
      "follow": {
        "S": ["$"],
        "C": ["$", "c", "d"]
      }
    },
    "automaton": {
      "num_states": 10,
      "states": [...],
      "transitions": [...]
    },
    "parsing_table": {
      "action": {...},
      "goto": {...},
      "headers": {...}
    },
    "closure_table": [...]
  }
}
```

### 2. `/parse/productions` - Solo Producciones

Retorna únicamente las producciones de la gramática.

**Request:**
```json
POST http://localhost:8000/parse/productions
{
  "grammar": "S -> C C\nC -> c C\nC -> d"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "productions": [
      {"id": 0, "lhs": "S", "rhs": ["C", "C"], "rhs_str": "C C"},
      {"id": 1, "lhs": "C", "rhs": ["c", "C"], "rhs_str": "c C"},
      {"id": 2, "lhs": "C", "rhs": ["d"], "rhs_str": "d"}
    ],
    "num_productions": 3
  }
}
```

### 3. `/parse/symbols` - Solo Símbolos

Retorna terminales y no terminales.

**Response:**
```json
{
  "success": true,
  "data": {
    "terminals": ["c", "d"],
    "end_marker": "$",
    "non_terminals": ["C", "S"],
    "start_symbol": "S",
    "augmented_start": "S'"
  }
}
```

### 4. `/parse/first-follow` - Conjuntos FIRST y FOLLOW

**Response:**
```json
{
  "success": true,
  "data": {
    "first": {
      "S": ["c", "d"],
      "C": ["c", "d"]
    },
    "follow": {
      "S": ["$"],
      "C": ["$", "c", "d"]
    }
  }
}
```

### 5. `/parse/automaton` - Autómata LR(1)

Retorna estados, items y transiciones del autómata.

**Response:**
```json
{
  "success": true,
  "data": {
    "num_states": 10,
    "states": [
      {
        "id": 0,
        "items": [
          "[S' -> . S, $]",
          "[S -> . C C, $]",
          "[C -> . c C, c]",
          "[C -> . d, c]"
        ],
        "kernel_items": ["[S' -> . S, $]"],
        "is_accept": false,
        "num_items": 4
      },
      ...
    ],
    "transitions": [
      {"from": 0, "to": 3, "symbol": "S"},
      {"from": 0, "to": 2, "symbol": "C"},
      {"from": 0, "to": 4, "symbol": "c"},
      ...
    ]
  }
}
```

### 6. `/parse/table` - Tabla de Parsing (ACTION y GOTO)

**Response (formato mejorado con metadatos visuales):**
```json
{
  "success": true,
  "data": {
    "action": {
      "0": {
        "c": {
          "type": "shift",
          "value": 4,
          "display": "s4",
          "color": "green"
        },
        "d": {
          "type": "shift",
          "value": 1,
          "display": "s1",
          "color": "green"
        }
      },
      "1": {
        "$": {
          "type": "reduce",
          "value": 2,
          "display": "r2",
          "color": "red",
          "production": "C → d"
        }
      },
      "3": {
        "$": {
          "type": "accept",
          "value": null,
          "display": "acc",
          "color": "blue"
        }
      }
    },
    "goto": {
      "0": {
        "S": {
          "type": "goto",
          "value": 3,
          "display": "3",
          "color": "purple"
        },
        "C": {
          "type": "goto",
          "value": 2,
          "display": "2",
          "color": "purple"
        }
      }
    },
    "headers": {
      "terminals": ["$", "c", "d"],
      "non_terminals": ["C", "S"]
    },
    "productions": [
      {"id": 0, "lhs": "S'", "rhs": ["S"], "display": "S' → S"},
      {"id": 1, "lhs": "S", "rhs": ["C", "C"], "display": "S → C C"},
      {"id": 2, "lhs": "C", "rhs": ["d"], "display": "C → d"}
    ],
    "num_states": 10
  }
}
```

**Campos de cada entrada ACTION:**
- `type`: "shift", "reduce" o "accept"
- `value`: número de estado (shift), número de producción (reduce), o null (accept)
- `display`: texto para mostrar (ej: "s4", "r2", "acc")
- `color`: sugerencia de color ("green" shift, "red" reduce, "blue" accept)
- `production`: (solo en reduce) texto de la producción para tooltip

**Campos de cada entrada GOTO:**
- `type`: "goto"
- `value`: número de estado destino
- `display`: texto para mostrar
- `color`: sugerencia de color ("purple")

### 7. `/parse/string` - Parsear una Cadena de Entrada

Parsea una cadena usando el parser LR(1) y retorna el proceso paso a paso.

**Request:**
```json
POST http://localhost:8000/parse/string
Content-Type: application/json

{
  "grammar": "S -> C C\nC -> c C\nC -> d",
  "input_string": "c c d d"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "success": true,
    "accepted": true,
    "error": null,
    "steps": [
      {
        "step": 1,
        "stack": [0],
        "symbol_stack": [],
        "remaining_input": "c c d d $",
        "current_state": 0,
        "current_token": "c",
        "action": "shift",
        "action_detail": "Desplazar a estado 4"
      },
      {
        "step": 4,
        "stack": [0, 4, 4, 1],
        "symbol_stack": ["c", "c", "d"],
        "remaining_input": "d $",
        "current_state": 1,
        "current_token": "d",
        "action": "reduce",
        "action_detail": "Reducir por producción 2: C → d",
        "production_id": 2,
        "production_lhs": "C",
        "production_rhs": ["d"]
      }
    ],
    "summary": {
      "total_steps": 10,
      "input_tokens": ["c", "c", "d", "d"],
      "input_length": 4,
      "accepted": true
    }
  }
}
```

**Campos de respuesta:**
- `accepted`: `true` si la cadena fue aceptada, `false` si fue rechazada
- `error`: mensaje de error si la cadena no fue aceptada
- `steps`: array con cada paso del parsing
- `summary`: resumen del análisis

**Campos de cada paso:**
- `step`: número del paso
- `stack`: pila de estados
- `symbol_stack`: pila de símbolos (para visualización)
- `remaining_input`: entrada que falta por procesar
- `current_state`: estado actual
- `current_token`: token actual siendo procesado
- `action`: tipo de acción ("shift", "reduce", "accept")
- `action_detail`: descripción de la acción
- `production_id`, `production_lhs`, `production_rhs`: (solo en reduce) información de la producción

### 8. `/parse/closure` - Tabla de Clausura

**Response (formato mejorado para tablas):**
```json
{
  "success": true,
  "data": [
    {
      "state_id": 0,
      "goto_label": "INITIAL",
      "kernel_items": ["[S' -> . S, $]"],
      "kernel_display": "[S' -> . S, $]",
      "closure_items": [
        "[S' -> . S, $]",
        "[S -> . C C, $]",
        "[C -> . c C, c]",
        "[C -> . d, c]"
      ],
      "closure_display": "[S' -> . S, $]; [S -> . C C, $]; [C -> . c C, c]; [C -> . d, c]",
      "num_items": 4,
      "goto_transitions": null
    },
    {
      "state_id": 1,
      "goto_label": "goto(0, S)",
      "kernel_items": ["[S' -> S ., $]"],
      "kernel_display": "[S' -> S ., $]",
      "closure_items": ["[S' -> S ., $]"],
      "closure_display": "[S' -> S ., $]",
      "num_items": 1,
      "goto_transitions": [[0, "S"]]
    }
  ]
}
```

**Campos:**
- `state_id`: Número del estado
- `goto_label`: Etiqueta de transición (ej: "goto(0, S)")
- `kernel_items`: Array con items kernel (formato completo)
- `kernel_display`: String para mostrar kernel en formato compacto
- `closure_items`: Array completo con todos los items del estado
- `closure_display`: String compacto con preview de la clausura (máximo 5 items)
- `num_items`: Total de items en el estado
- `goto_transitions`: Array de tuplas [estado_origen, símbolo]


### 9. `/parse/graphs` - Gráficos en Base64

Genera y retorna los gráficos del autómata en formato base64.

**Request:**
```json
POST http://localhost:8000/parse/graphs
{
  "grammar": "S -> C C\nC -> c C\nC -> d"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "automaton_full": "iVBORw0KGgoAAAANSUhEUgAA...",
    "automaton_simplified": "iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

## 🌐 Ejemplo desde JavaScript (Frontend)

```javascript
// Procesar gramática
async function procesarGramatica() {
  const response = await fetch('http://localhost:8000/parse', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      grammar: "S -> C C\nC -> c C\nC -> d",
      generate_graphs: false
    })
  });
  
  const resultado = await response.json();
  
  if (resultado.success) {
    console.log('Producciones:', resultado.data.grammar.productions);
    console.log('Estados:', resultado.data.automaton.num_states);
    console.log('FIRST:', resultado.data.first_follow.first);
    console.log('FOLLOW:', resultado.data.first_follow.follow);
  } else {
    console.error('Error:', resultado.error);
  }
}

// Obtener solo tabla de parsing
async function obtenerTabla() {
  const response = await fetch('http://localhost:8000/parse/table', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      grammar: "E -> E + T\nE -> T\nT -> id"
    })
  });
  
  const resultado = await response.json();
  console.log('Tabla ACTION:', resultado.data.action);
  console.log('Tabla GOTO:', resultado.data.goto);
}
```

## 🐍 Ejemplo desde Python

```python
import requests
import json

# Endpoint
url = "http://localhost:8000/parse"

# Gramática
gramatica = {
    "grammar": "S -> C C\nC -> c C\nC -> d",
    "generate_graphs": False
}

# Request
response = requests.post(url, json=gramatica)
resultado = response.json()

if resultado["success"]:
    print(f"✓ Producciones: {resultado['data']['grammar']['num_productions']}")
    print(f"✓ Estados: {resultado['data']['automaton']['num_states']}")
    print(f"✓ FIRST: {resultado['data']['first_follow']['first']}")
else:
    print(f"✗ Error: {resultado['error']}")
```

## 📝 Formato de Gramáticas

Las gramáticas deben enviarse en formato texto con:
- **Separador**: `->` o `:`
- **Una producción por línea**
- **Producciones vacías**: `epsilon` o `ε`

Ejemplos válidos:
```
S -> C C
C -> c C
C -> d
```

```
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
```

## ⚠️ Manejo de Errores

Si hay un error, la respuesta será:
```json
{
  "success": false,
  "error": "Descripción del error",
  "data": null
}
```

HTTP Status Codes:
- `200`: Éxito
- `400`: Error en la gramática (formato inválido)
- `500`: Error interno del servidor

## 🔧 Configuración CORS

El servidor está configurado para aceptar requests desde cualquier origen. En producción, modifica `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-frontend.com"],  # Especifica tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚦 Health Check

```bash
GET http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "lr1-parser-api"
}
```
