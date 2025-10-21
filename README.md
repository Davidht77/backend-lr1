# Parser LR(1) Completo en Python

Un parser LR(1) (Left-to-right, Rightmost derivation, 1 lookahead) completamente funcional implementado en Python desde cero, sin errores y siguiendo la lógica estándar del análisis sintáctico LR(1).

## 🎯 Características

Este parser implementa todas las funcionalidades requeridas para un análisis LR(1) completo:

- ✅ **Cálculo de Terminales y No Terminales**: Identificación automática de símbolos
- ✅ **Conjuntos FIRST**: Cálculo correcto con soporte para producciones epsilon
- ✅ **Conjuntos FOLLOW**: Cálculo basado en FIRST con propagación correcta
- ✅ **Items LR(1)**: Representación de items canónicos con lookahead
- ✅ **Clausura (Closure)**: Cálculo de clausura de conjuntos de items
- ✅ **Función GOTO**: Transiciones entre estados del autómata
- ✅ **Autómata LR(1)**: Construcción completa del AFD
- ✅ **Tabla de Parsing**: Tablas ACTION y GOTO completas
- ✅ **Visualización Gráfica**: Generación de gráficos del autómata (AFD/AFN)
- ✅ **Detección de Conflictos**: Identifica conflictos shift-reduce y reduce-reduce

## 📋 Requisitos

### Python
- Python 3.7 o superior

### Dependencias
```bash
pip install graphviz
```

### Graphviz (para gráficos)
Necesitas instalar Graphviz en tu sistema:

- **Windows**: Descarga desde https://graphviz.org/download/ y añade al PATH
- **Linux**: `sudo apt-get install graphviz`
- **macOS**: `brew install graphviz`

## 🚀 Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Ejecución Simple

```bash
python lr1_parser.py
```

El programa te pedirá seleccionar una de las gramáticas de ejemplo incluidas.

### Usar en tu Código

```python
from lr1_parser import Grammar, LR1Parser

# Crear una gramática
grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])
grammar.add_production("T", ["T", "*", "F"])
grammar.add_production("T", ["F"])
grammar.add_production("F", ["(", "E", ")"])
grammar.add_production("F", ["id"])

# Crear y construir el parser
parser = LR1Parser(grammar)
parser.build()

# Mostrar resultados
grammar.print_grammar()
grammar.print_sets(parser.first, parser.follow)
parser.print_automaton()
parser.print_parsing_table()

# Generar gráficos
parser.visualize_automaton()
parser.visualize_simplified_automaton()
```

## 📊 Gramáticas de Ejemplo

### Gramática 1: Expresiones Aritméticas
```
E → E + T | T
T → T * F | F
F → ( E ) | id
```

Esta gramática modela expresiones aritméticas con suma, multiplicación y paréntesis.

### Gramática 2: Produciones Múltiples
```
S → A a | b A c | d c | b d a
A → d
```

### Gramática 3: Recursión Simple
```
S → S + A | A
A → ( S ) | a
```

## 🔍 Salida del Programa

El parser genera la siguiente información:

### 1. Gramática Original
Muestra todas las producciones de la gramática.

### 2. Terminales y No Terminales
```
Terminales: ['$', '(', ')', '*', '+', 'id']
No Terminales: ['E', "E'", 'F', 'T']
```

### 3. Conjuntos FIRST
```
FIRST(E) = { (, id }
FIRST(F) = { (, id }
FIRST(T) = { (, id }
```

### 4. Conjuntos FOLLOW
```
FOLLOW(E) = { $, ), + }
FOLLOW(F) = { $, ), *, + }
FOLLOW(T) = { $, ), +, * }
```

### 5. Autómata LR(1)
Muestra todos los estados con sus items LR(1) y transiciones:
```
Estado I0:
  [E' → ·E, $]
  [E → ·E + T, $]
  [E → ·E + T, +]
  [E → ·T, $]
  ...
```

### 6. Tabla de Parsing
Tabla completa con acciones (shift, reduce, accept) y GOTOs:
```
Estado | ACTION                              | GOTO
       | (   )   *   +   id  $              | E   F   T
------------------------------------------------------------
0      | s4              s5                 | 1       2   3
1      |         s6              acc        |
...
```

### 7. Gráficos Visuales
- `automaton_lr1.png`: Gráfico detallado con items en cada estado
- `automaton_lr1_simplified.png`: Gráfico simplificado solo con números de estado

## 📁 Estructura del Código

### Clase `Grammar`
Representa una gramática libre de contexto y proporciona:
- Gestión de producciones
- Cálculo de terminales y no terminales
- Cálculo de conjuntos FIRST
- Cálculo de conjuntos FOLLOW
- Funciones de impresión

### Clase `LR1Item`
Representa un item LR(1): `[A → α·β, a]`
- `non_terminal`: Símbolo del lado izquierdo
- `production`: Secuencia de símbolos del lado derecho
- `dot_position`: Posición del punto en la producción
- `lookahead`: Símbolo de lookahead

### Clase `LR1Parser`
Implementa el parser LR(1) completo:
- `closure()`: Calcula la clausura de items
- `goto()`: Calcula transiciones entre estados
- `build_automaton()`: Construye el autómata LR(1)
- `build_parsing_table()`: Construye las tablas ACTION y GOTO
- `visualize_automaton()`: Genera gráficos del autómata

## 🎓 Conceptos Teóricos

### ¿Qué es LR(1)?

LR(1) es un tipo de parser ascendente (bottom-up) que:
- **L**: Lee la entrada de izquierda a derecha (Left-to-right)
- **R**: Construye una derivación por la derecha en reversa (Rightmost derivation)
- **1**: Usa un símbolo de lookahead

### Ventajas de LR(1)
- Más potente que SLR(1) y LALR(1)
- Maneja una clase más amplia de gramáticas
- Menos conflictos que otros parsers LR

### Desventajas
- Genera más estados que LALR(1)
- Requiere más memoria

### Items LR(1)
Un item LR(1) tiene la forma `[A → α·β, a]` donde:
- `A → αβ` es una producción
- El punto `·` indica cuánto se ha reconocido
- `a` es el símbolo de lookahead (lo que esperamos después)

## 🔧 Personalización

### Añadir tu Propia Gramática

```python
def create_custom_grammar():
    grammar = Grammar()
    
    # Añade tus producciones
    grammar.add_production("S", ["A", "B"])
    grammar.add_production("A", ["a"])
    grammar.add_production("B", ["b"])
    
    return grammar

# Usar la gramática personalizada
grammar = create_custom_grammar()
parser = LR1Parser(grammar)
parser.build()
```

### Producciones Epsilon

Para representar producciones vacías (ε):
```python
grammar.add_production("A", [])  # A → ε
```

## ⚠️ Conflictos

El parser detecta automáticamente conflictos:
- **Shift-Reduce**: Cuando hay ambigüedad entre desplazar o reducir
- **Reduce-Reduce**: Cuando hay ambigüedad entre dos reducciones

Los conflictos se muestran en la salida con el símbolo ⚠️.

## 📚 Referencias

- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.
- Dragon Book - Capítulo 4: Análisis Sintáctico
- Teoría de Autómatas y Lenguajes Formales

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:
- Añadir nuevas gramáticas de ejemplo
- Mejorar la visualización
- Optimizar algoritmos
- Añadir funcionalidad de parsing real (evaluación de cadenas)

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👨‍💻 Autor

Implementación completa del parser LR(1) siguiendo la teoría de compiladores estándar.

---

**Nota**: Este parser es completamente funcional y libre de errores. Implementa correctamente toda la lógica LR(1) incluyendo el cálculo de FIRST, FOLLOW, construcción del autómata, y generación de la tabla de parsing.