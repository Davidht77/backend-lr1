# Estructura Modular del Parser LR(1)

## 📁 Organización del Código

El proyecto ha sido modularizado para mejorar la legibilidad y el mantenimiento del código. La estructura es la siguiente:

```
backend-lr1/
│
├── lr1_parser/              # Paquete principal
│   ├── __init__.py          # Exporta todas las clases y funciones
│   ├── grammar.py           # Clase Grammar
│   ├── item.py              # Clase LR1Item
│   ├── parser.py            # Clase LR1Parser
│   ├── visualizer.py        # Clase RegularGrammarAFNVisualizer
│   └── examples.py          # Funciones de ejemplo
│
├── lr1_parser.py            # Punto de entrada principal
├── demo.py                  # Demo interactivo
├── requirements.txt         # Dependencias
└── ESTRUCTURA.md            # Este archivo
```

## 📦 Módulos

### 1. `lr1_parser/grammar.py`
**Clase: `Grammar`**

Representa una gramática libre de contexto.

**Responsabilidades:**
- Gestión de producciones
- Cálculo de conjuntos FIRST
- Cálculo de conjuntos FOLLOW
- Identificación de terminales y no terminales
- Impresión de la gramática y sus conjuntos

**Métodos principales:**
```python
grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.compute_first()
grammar.compute_follow(first)
grammar.print_grammar()
```

---

### 2. `lr1_parser/item.py`
**Clase: `LR1Item`**

Representa un item LR(1): `[A → α·β, a]`

**Responsabilidades:**
- Representación de items con punto y lookahead
- Operaciones sobre items (advance, next_symbol)
- Comparación y hashing de items

**Métodos principales:**
```python
item = LR1Item("E", ["E", "+", "T"], 1, "$")
next_sym = item.next_symbol()
new_item = item.advance()
```

---

### 3. `lr1_parser/parser.py`
**Clase: `LR1Parser`**

Implementa el análisis sintáctico LR(1) completo.

**Responsabilidades:**
- Construcción del autómata LR(1)
- Cálculo de clausuras (closure)
- Cálculo de transiciones (goto)
- Construcción de tabla de parsing
- Visualización del autómata (completo y simplificado)
- Impresión de tabla de clausura

**Métodos principales:**
```python
parser = LR1Parser(grammar)
parser.build()
parser.print_automaton()
parser.print_parsing_table()
parser.print_closure_table()
parser.visualize_automaton("output")
parser.visualize_simplified_automaton("output_simple")
```

---

### 4. `lr1_parser/visualizer.py`
**Clase: `RegularGrammarAFNVisualizer`**

Visualizador de AFN y AFD para gramáticas regulares.

**Responsabilidades:**
- Análisis de gramáticas regulares
- Generación de AFN (Autómata Finito No determinista)
- Generación de AFD (Autómata Finito Determinista)
- Detección de estados finales y transiciones

**Métodos principales:**
```python
visualizer = RegularGrammarAFNVisualizer(grammar)
visualizer.visualize_afn("afn_output")
visualizer.visualize_afd("afd_output")
visualizer.print_automaton_info()
```

---

### 5. `lr1_parser/examples.py`
**Funciones de ejemplo**

Proporciona gramáticas de ejemplo predefinidas.

**Funciones:**
- `create_example_grammar_1()` - Expresiones aritméticas (E → E + T | T, etc.)
- `create_example_grammar_2()` - Gramática S → A a | b A c | d c | b d a
- `create_example_grammar_3()` - Gramática simple S → S + A | A

```python
from lr1_parser import create_example_grammar_1

grammar = create_example_grammar_1()
```

---

## 🚀 Uso

### Importación básica
```python
from lr1_parser import Grammar, LR1Parser

# Crear gramática
grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])

# Crear parser
parser = LR1Parser(grammar)
parser.build()
parser.print_parsing_table()
```

### Uso con ejemplos predefinidos
```python
from lr1_parser import create_example_grammar_1, LR1Parser

grammar = create_example_grammar_1()
parser = LR1Parser(grammar)
parser.build()
parser.visualize_automaton("mi_automata")
```

### Ejecución del programa principal
```bash
python lr1_parser.py
```

### Ejecución del demo interactivo
```bash
python demo.py
```

---

## 🎯 Ventajas de la Modularización

1. **Separación de responsabilidades**: Cada módulo tiene una responsabilidad clara.
2. **Mantenibilidad**: Es más fácil localizar y modificar funcionalidades específicas.
3. **Legibilidad**: Archivos más pequeños y enfocados (~150-500 líneas cada uno).
4. **Reutilización**: Las clases pueden importarse individualmente según necesidad.
5. **Testing**: Facilita la creación de tests unitarios por módulo.
6. **Escalabilidad**: Permite agregar nuevas funcionalidades sin afectar el código existente.

---

## 📊 Líneas de código por módulo

- `grammar.py`: ~180 líneas
- `item.py`: ~50 líneas
- `parser.py`: ~470 líneas
- `visualizer.py`: ~150 líneas
- `examples.py`: ~60 líneas
- `__init__.py`: ~25 líneas
- `lr1_parser.py`: ~100 líneas (punto de entrada)

**Total modularizado**: ~1035 líneas distribuidas en 7 archivos
**Antes**: ~930 líneas en 1 archivo

---

## 🔧 Extensión

Para agregar nueva funcionalidad:

1. **Nueva gramática de ejemplo**: Agregar función en `examples.py`
2. **Nuevo algoritmo de parsing**: Agregar clase en nuevo archivo `lr1_parser/nuevo_parser.py`
3. **Nueva visualización**: Extender `visualizer.py` o crear nuevo visualizador
4. **Nuevas operaciones sobre gramáticas**: Extender clase `Grammar` en `grammar.py`

---

## 📝 Notas

- Todos los módulos mantienen compatibilidad con el código existente
- El archivo `lr1_parser.py` actúa como punto de entrada con retrocompatibilidad
- `demo.py` ya usa los imports modulares correctamente
- Las dependencias se mantienen en `requirements.txt` (graphviz)
