# 📊 Autómatas LR(1): AFN y AFD

## 🎯 Conceptos Clave

En el contexto del **Parser LR(1)**, los términos "AFN" y "AFD" se usan de forma **análoga** (no literal) para describir dos formas de visualizar el autómata:

### 1️⃣ AFN - Autómata con Clausura Completa
**"Autómata Finito No-determinista" (análogo)**

- Muestra **TODOS los items** de cada estado
- Incluye: Items kernel + Items de clausura derivados
- Más detallado y completo
- Útil para entender el proceso de derivación

**Ejemplo de estado:**
```
Estado 0:
  S' -> . A, $        ← Kernel
  A -> . A ( A ), $   ← Clausura
  A -> ., $           ← Clausura
  A -> . A ( A ), (   ← Clausura
  A -> ., (           ← Clausura
```

### 2️⃣ AFD - Autómata con Solo Kernel
**"Autómata Finito Determinista" (análogo)**

- Muestra **SOLO items kernel** de cada estado
- Omite items derivados (se asumen implícitos)
- Más compacto y limpio
- Útil para visualización simplificada

**Ejemplo del mismo estado:**
```
Estado 0:
  S' -> . A, $        ← Solo kernel
```

---

## 🔍 Diferencias Visuales

| Aspecto | AFN (Clausura Completa) | AFD (Solo Kernel) |
|---------|-------------------------|-------------------|
| **Items por estado** | Todos (kernel + clausura) | Solo kernel |
| **Tamaño visual** | Más grande | Más compacto |
| **Información** | Completa | Esencial |
| **Uso** | Análisis detallado | Presentación limpia |

---

## 🚀 Cómo Generar los Gráficos

### Opción 1: Desde Python (Script)
```bash
python generar_afn_afd.py
```

Genera:
- `lr1_afn_ejemplo.png` - AFN (clausura completa)
- `lr1_afd_ejemplo_kernel.png` - AFD (solo kernel)

### Opción 2: Desde el API
```bash
# Iniciar servidor
python main.py

# Llamar endpoint
curl -X POST http://localhost:8000/parse/graphs \
  -H "Content-Type: application/json" \
  -d '{"grammar": "A -> A ( A )\nA -> epsilon"}'
```

Retorna ambos gráficos en base64.

### Opción 3: Programáticamente
```python
from lr1_parser import Grammar, LR1Parser

grammar = Grammar()
grammar.add_production("A", ["A", "(", "A", ")"])
grammar.add_production("A", [])  # epsilon

parser = LR1Parser(grammar)
parser.build()

# AFN - Clausura completa
parser.visualize_automaton("mi_afn")

# AFD - Solo kernel
parser.visualize_simplified_automaton("mi_afd")
```

---

## 📚 Gramática de Ejemplo

```
A -> A ( A )
A -> ε
```

**Estados generados:** ~8 estados

**AFN:** Cada estado muestra 4-6 items
**AFD:** Cada estado muestra 1-3 items kernel

---

## ⚙️ Archivos Modificados

- `lr1_parser/parser.py`: 
  - `visualize_automaton()` - Genera AFN
  - `visualize_simplified_automaton()` - Genera AFD
- `api_helper.py`:
  - `generar_graficos_base64()` - Retorna ambos en base64
- `API_USAGE.md`:
  - Documentación del endpoint `/parse/graphs`

---

## 💡 Notas Importantes

1. **Ambos autómatas son el MISMO autómata**, solo difieren en qué items muestran
2. **Las transiciones son idénticas** en ambos
3. **El comportamiento del parser es el mismo** con ambos
4. **AFD ≠ LALR(1)**: AFD aquí solo significa "versión compacta visual", no fusión de estados

---

## 🎓 Contexto Académico

Este enfoque (AFN/AFD para LR) es común en cursos de compiladores donde se usa la **analogía** con autómatas finitos para ayudar a entender:

- **Clausura** → Similar a epsilon-clausura en AFN
- **Kernel** → Similar a estados esenciales en AFD
- **Mismo autómata, diferente vista** → Como AFN vs AFD (mismo lenguaje)

**No confundir con:**
- AFN/AFD de análisis léxico (regex)
- Subset construction (conversión AFN→AFD)
- LALR(1) (fusión de estados LR)
