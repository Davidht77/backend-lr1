# Parser LR(1) - Implementación Completa

Este paquete contiene una implementación completa de un **Parser LR(1)** (Left-to-Right, Rightmost derivation, 1 lookahead symbol) para análisis sintáctico de gramáticas libres de contexto.

## 🎯 ¿Qué es un Parser LR(1)?

Un Parser LR(1) es un analizador sintáctico bottom-up (de abajo hacia arriba) que:
- Lee la entrada de **izquierda a derecha** (Left-to-right)
- Construye una derivación **rightmost** en reversa
- Utiliza **1 símbolo de lookahead** para tomar decisiones

Es uno de los parsers más potentes, capaz de reconocer la mayoría de lenguajes de programación.

## 🏗️ Arquitectura del Parser

```
┌─────────────────────────────────────────────────────────────┐
│                    GRAMÁTICA (Grammar)                       │
│  • Producciones: A → α                                       │
│  • Terminales y No Terminales                                │
│  • Símbolo Inicial                                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              CÁLCULO DE FIRST Y FOLLOW                       │
│  • FIRST(X): conjunto de terminales que pueden aparecer      │
│    al inicio de X                                            │
│  • FOLLOW(X): conjunto de terminales que pueden aparecer     │
│    después de X                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           CONSTRUCCIÓN DEL AUTÓMATA LR(1)                    │
│  • Estados: conjuntos de items LR(1)                         │
│  • Items: [A → α . β, a]                                     │
│  • Transiciones: GOTO(estado, símbolo)                       │
│  • Clausura: closure(items)                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              TABLA DE PARSING (ACTION/GOTO)                  │
│  • ACTION: shift, reduce, accept, error                      │
│  • GOTO: transiciones para no terminales                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  PARSING DE CADENAS                          │
│  • Usa pila de estados                                       │
│  • Aplica acciones según tabla                               │
│  • Acepta o rechaza la entrada                               │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Módulos del Paquete

### 1. `grammar.py` - Gramática Libre de Contexto

**Clase:** `Grammar`

Gestiona la gramática y calcula los conjuntos FIRST y FOLLOW.

**Responsabilidades:**
- Almacenar producciones de la forma `A → α`
- Identificar símbolos terminales y no terminales
- Calcular FIRST(X) para cualquier símbolo o secuencia
- Calcular FOLLOW(X) para no terminales

**Algoritmo FIRST:**
```python
FIRST(X) = {
    si X es terminal: { X }
    si X → ε existe: { ε }
    si X → Y₁Y₂...Yₖ: FIRST(Y₁) ∪ FIRST(Y₂) si ε ∈ FIRST(Y₁), ...
}
```

**Algoritmo FOLLOW:**
```python
FOLLOW(A) = {
    si A es el inicio: { $ }
    si B → αAβ existe: FIRST(β) - {ε}
    si B → αA o (B → αAβ y ε ∈ FIRST(β)): FOLLOW(B)
}
```

**Ejemplo:**
```python
grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])
grammar.add_production("T", ["id"])

# Calcula FIRST y FOLLOW
first = grammar.compute_first()
follow = grammar.compute_follow(first)

# first["E"] = {"id"}
# follow["E"] = {"$", "+"}
```

### 2. `item.py` - Items LR(1)

**Clase:** `LR1Item`

Representa un item LR(1) de la forma: `A → α . β, a`

**Componentes:**
- `non_terminal`: lado izquierdo de la producción (A)
- `production`: lado derecho completo (α β)
- `dot_position`: posición del punto (.)
- `lookahead`: símbolo de anticipación (a)

**Formato de visualización:**
```
A → α . β, a
```
Sin corchetes para mejor legibilidad.

**Métodos principales:**
- `next_symbol()`: retorna el símbolo después del punto
- `advance()`: mueve el punto una posición a la derecha
- `__eq__()`, `__hash__()`: para usar items en conjuntos

**Ejemplo:**
```python
item = LR1Item("E", ["E", "+", "T"], 1, "$")
# Representa: E → E . + T, $

print(item.next_symbol())  # "+"
advanced = item.advance()  # E → E + . T, $
```

### 3. `parser.py` - Parser LR(1) Completo

**Clase:** `LR1Parser`

Implementa el algoritmo completo de construcción del parser LR(1).

#### Paso 1: Aumentar la Gramática

```python
# Gramática original: S → A a
# Gramática aumentada: S' → S
#                      S → A a
```

El símbolo `S'` permite detectar la aceptación cuando se completa `S' → S.`

#### Paso 2: Construir el Autómata

**Algoritmo de Clausura (Closure):**

```python
closure(I) = {
    items en I
    + para cada [A → α . B β, a] en I:
        para cada producción B → γ:
            para cada b en FIRST(β a):
                agregar [B → . γ, b]
}
```

**Algoritmo GOTO:**

```python
goto(I, X) = closure({
    [A → α X . β, a] | [A → α . X β, a] ∈ I
})
```

**Construcción del Autómata:**
```python
I₀ = closure({[S' → . S, $]})
estados = [I₀]
para cada estado I en estados:
    para cada símbolo X:
        J = goto(I, X)
        si J no está en estados:
            agregar J a estados
        agregar transición I --X--> J
```

#### Paso 3: Construir la Tabla de Parsing

**Tabla ACTION (para terminales):**
- **Shift s_j**: si `[A → α . a β, b] ∈ I_i` y `goto(I_i, a) = I_j`
- **Reduce r_k**: si `[A → α ., a] ∈ I_i`, reducir por producción k
- **Accept**: si `[S' → S ., $] ∈ I_i`

**Tabla GOTO (para no terminales):**
- `goto[i][A] = j` si `goto(I_i, A) = I_j`

**Ejemplo de Tabla:**
```
Estado | ACTION          | GOTO
       | a    b    $     | A   B
-------|-----------------|--------
  0    | s3   -    -     | 1   2
  1    | -    -   acc    | -   -
  2    | -    s4   -     | -   -
  3    | r1   r1   r1    | -   -
```

#### Paso 4: Parsing de Cadenas

**Algoritmo:**
```python
pila = [0]  # Estado inicial
entrada = tokens + [$]

mientras True:
    estado = pila[-1]
    token = entrada[0]
    acción = tabla_action[estado][token]
    
    si acción == "shift s_j":
        pila.push(j)
        entrada.shift()
    
    si acción == "reduce A → β":
        pila.pop(|β| estados)
        estado = pila[-1]
        j = tabla_goto[estado][A]
        pila.push(j)
    
    si acción == "accept":
        ✓ ACEPTAR
    
    si acción == error:
        ✗ RECHAZAR
```

### 4. Visualización de Autómatas

El parser genera **dos tipos de gráficos** usando Graphviz:

#### AFD (Autómata Finito Determinista)
**Método:** `visualize_automaton()`

- Muestra solo **items kernel** agrupados por estado
- Items kernel: aquellos con punto > 0 (excepto estado inicial)
- Formato elipse sin corchetes
- Dirección: Left-to-Right (LR)

**Ejemplo de estado AFD:**
```
┌─────────────────────┐
│ E → E . + T, $      │
│ E → E . * T, $      │
└─────────────────────┘
```

#### AFN (Autómata Finito No-Determinista)
**Método:** `visualize_simplified_automaton()`

- Muestra **todos los items** (kernel + clausura)
- Cada item es un nodo individual
- Incluye transiciones epsilon (ε) para clausura
- Dirección: Left-to-Right (LR)

**Ejemplo de items AFN:**
```
E → E . + T, $  --ε--> E → . E + T, +
                --ε--> T → . id, +
```

### 5. `visualizer.py` - Visualizador de Gramáticas Regulares

**Clase:** `RegularGrammarAFNVisualizer`

Visualizador especializado para gramáticas regulares lineales por la derecha.

**Funcionalidad:**
- Analiza producciones regulares
- Genera AFN/AFD para gramáticas regulares
- Detecta determinismo

## 🔄 Flujo Completo del Parser

### 1. Definir Gramática
```python
from lr1_parser import Grammar, LR1Parser

grammar = Grammar()
grammar.add_production("S", ["C", "C"])
grammar.add_production("C", ["c", "C"])
grammar.add_production("C", ["d"])
```

### 2. Construir Parser
```python
parser = LR1Parser(grammar)
parser.build()  # Ejecuta todos los pasos:
                # - Aumenta gramática
                # - Calcula FIRST/FOLLOW
                # - Construye autómata
                # - Genera tabla de parsing
```

### 3. Ver Información
```python
# Imprimir autómata
parser.print_automaton()

# Imprimir tabla de parsing
parser.print_parsing_table()

# Tabla de clausura
parser.print_closure_table()
```

### 4. Generar Visualizaciones
```python
# AFD (solo items kernel)
parser.visualize_automaton("mi_afd")
# → Genera: mi_afd.png

# AFN (todos los items con clausura)
parser.visualize_simplified_automaton("mi_afn")
# → Genera: mi_afn_kernel.png
```

### 5. Parsear Cadenas (Vía API)
```python
# Disponible a través del endpoint /parse/string
# Ver api_helper.py para implementación completa
```

## 📊 Formato de Salida

### Items LR(1)
**Formato actual:** `A → α . β, a` (sin corchetes)

**Ejemplos:**
- `S' → . S, $` - Item inicial
- `E → E . + T, $` - Punto en medio
- `T → id ., $` - Punto al final (item de reducción)

### Tabla de Parsing
```
Estado | ACTION              | GOTO
       | c    d    $         | C    S
-------|---------------------|--------
  0    | s4   s1   -         | 3    2
  1    | r3   r3   -         | -    -
  2    | -    -   acc        | -    -
  3    | s7   s5   -         | 6    -
```

Códigos:
- `sN`: shift al estado N
- `rN`: reduce por producción N
- `acc`: aceptar
- `-`: error

## 🎨 Características de Visualización

### Gráficos Mejorados (v2.0)

**Cambios recientes:**
- ✅ Items sin corchetes: `A → . B, $`
- ✅ Nodos elípticos (en lugar de cajas)
- ✅ Transiciones epsilon en gris punteado
- ✅ Layout optimizado (LR)
- ✅ Exportación a PNG vía Graphviz

**Requisitos:**
- Python 3.7+
- Librería `graphviz` (Python)
- Graphviz instalado en el sistema

## 🚀 Uso Básico

```python
from lr1_parser import Grammar, LR1Parser

# 1. Crear gramática
grammar = Grammar()
grammar.add_production("E", ["E", "+", "T"])
grammar.add_production("E", ["T"])
grammar.add_production("T", ["id"])

# 2. Construir parser
parser = LR1Parser(grammar)
parser.build()

# 3. Información del autómata
print(f"Estados: {len(parser.states)}")
print(f"Transiciones: {len(parser.transitions)}")

# 4. Generar gráficos
parser.visualize_automaton("ejemplo_afd")
parser.visualize_simplified_automaton("ejemplo_afn")

# 5. Ver tablas
parser.print_parsing_table()
```

## � Documentación Adicional

- **`../API_USAGE.md`** - Uso de la API REST
- **`../RAILWAY_DEPLOYMENT.md`** - Deployment en Railway
- **`../README.md`** - Documentación general del proyecto

## 🔧 Integración con FastAPI

Este parser está integrado con FastAPI para uso remoto:

```python
# Ver api_helper.py para detalles completos
from api_helper import procesar_gramatica_completo

resultado = procesar_gramatica_completo(
    "S -> C C\nC -> c C\nC -> d",
    generar_graficos=True
)

# resultado["data"]["automaton"] - Información del autómata
# resultado["data"]["parsing_table"] - Tabla de parsing
# resultado["data"]["graphs"] - Gráficos en base64
```

## ⚙️ Requisitos Técnicos

**Python:**
- Python 3.7 o superior
- `graphviz` librería de Python

**Sistema:**
- Graphviz instalado (`dot` en PATH)
- En Railway: configurado vía `nixpacks.toml`

## 🎓 Referencias Teóricas

El parser implementa los algoritmos descritos en:
- **"Compilers: Principles, Techniques, and Tools"** (Dragon Book)
- Algoritmo de construcción de autómata LR(1) canónico
- Cálculo de conjuntos FIRST y FOLLOW
- Construcción de tablas ACTION y GOTO

---

**Versión:** 2.0  
**Última actualización:** Octubre 2025  
**Autor:** Parser LR(1) Team
