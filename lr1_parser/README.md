# Parser LR(1) - Paquete Modular

Este paquete contiene la implementación modular del Parser LR(1).

## 📦 Módulos

### `__init__.py`
Exporta todas las clases y funciones públicas del paquete.

### `grammar.py`
**Clase:** `Grammar`

Representa una gramática libre de contexto.
- Gestión de producciones
- Cálculo de FIRST/FOLLOW
- Identificación de terminales y no terminales

### `item.py`
**Clase:** `LR1Item`

Representa un item LR(1): `[A → α·β, a]`
- Operaciones sobre items
- Comparación y hashing

### `parser.py`
**Clase:** `LR1Parser`

Implementa el análisis sintáctico LR(1) completo.
- Construcción del autómata
- Tabla de parsing
- Visualizaciones (completa y simplificada)

### `visualizer.py`
**Clase:** `RegularGrammarAFNVisualizer`

Visualizador de AFN y AFD para gramáticas regulares.
- Generación de autómatas finitos
- Análisis de determinismo

### `examples.py`
Funciones para crear gramáticas de ejemplo.
- `create_example_grammar_1()` - Expresiones aritméticas
- `create_example_grammar_2()` - Gramática S → A a | ...
- `create_example_grammar_3()` - Gramática recursiva

## 🚀 Uso

```python
from lr1_parser import Grammar, LR1Parser

grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])

parser = LR1Parser(grammar)
parser.build()
parser.print_parsing_table()
```

## 📝 Documentación

Ver archivos en el directorio raíz:
- `ESTRUCTURA.md` - Documentación detallada
- `EJEMPLOS_USO.py` - Ejemplos prácticos
- `ARQUITECTURA.txt` - Diagrama visual
