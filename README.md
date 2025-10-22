# Parser LR(1) - Análisis Sintáctico

Implementación completa de un Parser LR(1) con visualización gráfica del autómata.

## 📁 Archivos Esenciales del Programa

### 🔧 Archivos NECESARIOS (No Borrar)

#### 1. `lr1_parser.py` ⭐ CORE
El archivo principal con toda la lógica del parser:
- Clase `Grammar`: Manejo de gramáticas libres de contexto
- Clase `LR1Item`: Representación de items LR(1)
- Clase `LR1Parser`: Parser completo con:
  - Cálculo de FIRST y FOLLOW
  - Construcción del autómata LR(1)
  - Generación de tabla de parsing
  - Visualización gráfica del autómata

#### 2. `demo.py` 🎯 INTERFAZ
Demo interactiva con 6 gramáticas predefinidas:
- Expresiones Aritméticas
- Lista de elementos  
- Declaraciones
- Paréntesis balanceados
- Expresiones booleanas
- Asignaciones

#### 3. `requirements.txt` 📦 DEPENDENCIAS
```
graphviz
```

#### 4. `README.md` 📖 DOCUMENTACIÓN
Este archivo con instrucciones de uso.

### 🧪 Archivos Opcionales

- `test_parser.py` - Tests unitarios (recomendado para desarrollo)

### 🖼️ Archivos Generados Automáticamente

Estos archivos se crean al ejecutar el programa y pueden borrarse:
- `automaton_*.png` - Gráficos del autómata completo
- `automaton_*_simplified.png` - Gráficos con items kernel

## 🚀 Instalación

### Requisitos Previos

1. **Python 3.7+**
2. **Graphviz**: https://graphviz.org/download/
   - Windows: Descargar e instalar, añadir al PATH
   - Linux: `sudo apt-get install graphviz`
   - macOS: `brew install graphviz`

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Ejecutar Demo Interactivo

```bash
python demo.py
```

Selecciona una gramática del menú y el programa:
1. Mostrará las producciones
2. Calculará FIRST y FOLLOW
3. Generará la tabla de parsing
4. Creará gráficos PNG del autómata

### Usar en Tu Código

```python
from lr1_parser import Grammar, LR1Parser

# Crear gramática
grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])
grammar.add_production("T", ["id"])

# Construir parser
parser = LR1Parser(grammar)
parser.build()

# Ver resultados
grammar.print_grammar()
parser.print_parsing_table()

# Generar gráficos
parser.visualize_automaton("mi_automata")
parser.visualize_simplified_automaton("mi_automata")
```

## 📊 Características

### ✅ Funcionalidades Implementadas

- ✓ Cálculo automático de terminales y no terminales
- ✓ Conjuntos FIRST con soporte para epsilon
- ✓ Conjuntos FOLLOW con propagación correcta
- ✓ Items LR(1) con lookaheads
- ✓ Función CLOSURE para derivar items
- ✓ Función GOTO para transiciones
- ✓ Construcción del autómata LR(1) (AFD)
- ✓ Tabla de parsing (ACTION y GOTO)
- ✓ Detección de conflictos
- ✓ Visualización gráfica completa

### 📈 Dos Tipos de Visualización

#### 1. Autómata Completo (`automaton_*.png`)
- Muestra **items kernel + clausura**
- Hasta 10 items por estado
- Formato: `[A -> α . β, a]`
- Para análisis detallado

#### 2. Items Kernel (`automaton_*_simplified.png`)
- Solo **items kernel** (esenciales)
- Hasta 8 items por estado
- Formato: `[A → α • β, a]`
- Más compacto y legible

## 🔑 Conceptos Clave

### Items LR(1)

Formato: `[A -> α • β, a]`
- `A`: No terminal
- `α`: Símbolos procesados (antes del punto)
- `•`: Posición actual
- `β`: Símbolos pendientes (después del punto)
- `a`: Lookahead (token de búsqueda anticipada)

### Items Kernel

Los items que **definen cada estado**:
- **Estado I0**: Solo `[S' → • S, $]` (item inicial aumentado)
- **Otros estados**: Items donde `dot_position > 0`

Los **items de clausura** se derivan de los kernel mediante `CLOSURE()`.

## 📝 Estructura del Código

```
lr1_parser.py (676 líneas)
├── Grammar
│   ├── add_production()      # Añadir producciones
│   ├── compute_first()       # Calcular FIRST
│   ├── compute_follow()      # Calcular FOLLOW
│   └── print_grammar()       # Mostrar gramática
│
├── LR1Item
│   ├── next_symbol()         # Símbolo después del punto
│   └── advance()             # Mover punto una posición
│
└── LR1Parser
    ├── build()               # Construir parser completo
    ├── closure()             # Clausura de items
    ├── goto()                # Transiciones
    ├── build_automaton()     # Construir AFD
    ├── build_parsing_table() # Generar tablas
    ├── visualize_automaton() # Gráfico completo
    └── visualize_simplified_automaton() # Gráfico kernel
```

## 🎓 Ejemplo de Salida

```
============================================================
GRAMÁTICA
============================================================
E' -> E
E -> E + T | T
T -> id

============================================================
CONJUNTOS FIRST
============================================================
FIRST(E) = { id }
FIRST(T) = { id }

============================================================
TABLA DE PARSING LR(1)
============================================================
Estado   | ACTION               | GOTO
         | $    +    id         | E    T
---------+---------------------+-------
0        |           s1         | 3    2
1        | r2   r2              |
2        | r1   r1              |
3        | acc  s4              |
4        |           s1         |      5
5        | r0   r0              |

============================================================
```

Además se generan dos archivos PNG con los gráficos del autómata.

## 🗂️ Resumen de Archivos

| Archivo | Tipo | ¿Necesario? | Descripción |
|---------|------|-------------|-------------|
| `lr1_parser.py` | Python | ✅ SÍ | Core del parser |
| `demo.py` | Python | ✅ SÍ | Interfaz interactiva |
| `requirements.txt` | Texto | ✅ SÍ | Dependencias |
| `README.md` | Markdown | ✅ SÍ | Documentación |
| `test_parser.py` | Python | ⚠️ Opcional | Tests unitarios |
| `automaton_*.png` | Imagen | ❌ NO | Generados automáticamente |
| `__pycache__/` | Carpeta | ❌ NO | Archivos compilados Python |

## ⚠️ Notas

- Graphviz debe estar **instalado en el sistema**, no solo el paquete Python
- Los gráficos se generan en el directorio actual
- Los archivos PNG se sobrescriben en cada ejecución
- Estados de aceptación: doble círculo verde

## 📚 Referencias

- Compiladores: Principios, Técnicas y Herramientas (Aho, Sethi, Ullman)
- Modern Compiler Implementation (Andrew Appel)

---

**Autor:** Davidht77  
**Repositorio:** backend-lr1  
**Fecha:** Octubre 2025
