# Quick Start - Parser LR(1)

Guía rápida para empezar a usar el Parser LR(1) en menos de 5 minutos.

## Instalación Rápida

### 1. Instalar Dependencias

```bash
pip install graphviz
```

### 2. Instalar Graphviz (Opcional - para gráficos)

- **Windows**: Descargar desde https://graphviz.org/download/ y agregar al PATH
- **Linux**: `sudo apt-get install graphviz`
- **macOS**: `brew install graphviz`

## Uso Básico

### Opción 1: Ejecutar Demo Automática (Recomendado)

```bash
python demo_auto.py
```

Esto ejecutará automáticamente:
- Análisis completo de una gramática de ejemplo
- Cálculo de FIRST y FOLLOW
- Construcción del autómata
- Generación de tabla de parsing
- Múltiples ejemplos
- Generación de gráficos

### Opción 2: Ejecutar Pruebas

```bash
python test_parser.py
```

Ejecuta 8 pruebas con diferentes gramáticas para verificar que todo funciona.

### Opción 3: Usar el Parser Principal

```bash
python lr1_parser.py
```

Selecciona una de las gramáticas de ejemplo predefinidas.

## Primer Ejemplo de Código

Crea un archivo `mi_parser.py`:

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

# Mostrar resultados
grammar.print_grammar()
grammar.print_sets(parser.first, parser.follow)
parser.print_parsing_table()

# Generar gráficos
parser.visualize_automaton()
```

Ejecuta:
```bash
python mi_parser.py
```

## Ejemplos de Gramáticas

### Ejemplo 1: Lista Simple

```python
grammar = Grammar()
grammar.add_production("L", ["L", ",", "E"])
grammar.add_production("L", ["E"])
grammar.add_production("E", ["id"])
```

### Ejemplo 2: Declaraciones

```python
grammar = Grammar()
grammar.add_production("D", ["type", "L", ";"])
grammar.add_production("L", ["L", ",", "id"])
grammar.add_production("L", ["id"])
```

### Ejemplo 3: Expresiones con Paréntesis

```python
grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])
grammar.add_production("T", ["(", "E", ")"])
grammar.add_production("T", ["id"])
```

### Ejemplo 4: Producción Epsilon (vacía)

```python
grammar = Grammar()
grammar.add_production("S", ["(", "S", ")"])
grammar.add_production("S", [])  # Producción epsilon
```

## Comandos Útiles

### Ver Todos los Ejemplos Disponibles

```bash
python example_custom.py
```

Menú interactivo con 8 ejemplos de gramáticas diferentes.

### Demo Interactiva

```bash
python demo.py
```

Demo paso a paso con explicaciones (requiere interacción).

### Demo Automática Completa

```bash
python demo_auto.py
```

Demo completa sin interacción del usuario.

## Estructura de Archivos

```
backend-lr1/
├── lr1_parser.py           # Parser LR(1) principal
├── example_custom.py       # Ejemplos personalizados
├── test_parser.py          # Suite de pruebas
├── demo.py                 # Demo interactiva
├── demo_auto.py            # Demo automática
├── README.md               # Documentación completa
├── QUICKSTART.md           # Esta guía
└── requirements.txt        # Dependencias
```

## Salida del Parser

El parser genera:

1. **Gramática aumentada**: Muestra todas las producciones
2. **Terminales y No Terminales**: Lista de símbolos
3. **Conjuntos FIRST**: Para cada no terminal
4. **Conjuntos FOLLOW**: Para cada no terminal
5. **Autómata LR(1)**: Todos los estados e items
6. **Tabla de Parsing**: Acciones (ACTION y GOTO)
7. **Gráficos PNG**: Visualización del autómata

## Archivos Generados

Después de ejecutar el parser, encontrarás:

- `*.png` - Gráficos del autómata generados
- La salida en consola con toda la información

## Conceptos Básicos

### ¿Qué es LR(1)?

- **L**: Left-to-right (lee de izquierda a derecha)
- **R**: Rightmost derivation (derivación por la derecha)
- **1**: Un símbolo de lookahead

### Notación en las Producciones

```
A -> B C D    # A produce B, C, D
A -> epsilon  # A produce cadena vacía (usar: A -> [] en código)
A -> a | b    # A produce 'a' o 'b' (dos producciones separadas)
```

### Items LR(1)

```
[E -> E + . T, $]
```

- `E -> E + . T` : Producción con punto que indica posición
- `$` : Símbolo de lookahead (lo que esperamos ver después)

### Tabla de Parsing

- `s5` : Shift (desplazar) e ir al estado 5
- `r3` : Reduce (reducir) usando producción 3
- `acc` : Accept (aceptar la entrada)

## Personalización

### Crear Tu Propia Gramática

```python
from lr1_parser import Grammar, LR1Parser

# Inicializar
grammar = Grammar()

# Añadir producciones (la primera define el símbolo inicial)
grammar.add_production("S", ["a", "B"])
grammar.add_production("B", ["b"])

# Construir y mostrar
parser = LR1Parser(grammar)
parser.build()

grammar.print_grammar()
parser.print_parsing_table()
```

### Generar Solo Gráficos

```python
parser.visualize_automaton("mi_automata")
parser.visualize_simplified_automaton("mi_automata")
```

Genera:
- `mi_automata.png` (detallado)
- `mi_automata_simplified.png` (simplificado)

## Solución de Problemas

### Error: "No module named 'graphviz'"

```bash
pip install graphviz
```

### Error: "No se pudo generar el gráfico"

Necesitas instalar Graphviz en tu sistema (no solo el paquete Python):
- Windows: https://graphviz.org/download/
- Linux: `sudo apt-get install graphviz`
- macOS: `brew install graphviz`

### Caracteres extraños en la salida

El parser usa solo caracteres ASCII estándar. Si ves problemas, verifica la codificación de tu terminal.

## Siguientes Pasos

1. **Lee el README.md** - Documentación completa
2. **Ejecuta los ejemplos** - `python example_custom.py`
3. **Crea tu gramática** - Usa el código de ejemplo
4. **Explora los tests** - `python test_parser.py`
5. **Lee el código fuente** - `lr1_parser.py` está bien comentado

## Recursos Adicionales

- **Dragon Book**: Compilers: Principles, Techniques, and Tools (Aho, Lam, Sethi, Ullman)
- **Código completo**: Revisa `lr1_parser.py` para entender la implementación
- **Ejemplos**: `example_custom.py` tiene 8 ejemplos de gramáticas diferentes

## Ayuda Rápida

**¿Quieres ver un ejemplo funcionando YA?**

```bash
python demo_auto.py
```

**¿Quieres probar que todo funciona?**

```bash
python test_parser.py
```

**¿Quieres explorar ejemplos?**

```bash
python example_custom.py
```

---

¡Listo! Ya tienes un parser LR(1) completamente funcional.

Para más información detallada, consulta el archivo `README.md`.