# ✅ RESUMEN: Generación de AFN y AFD para Parser LR(1)

## 🎯 Lo que se implementó

Tu parser LR(1) **ahora genera DOS tipos de gráficos** que coinciden con la metodología que te enseñaron:

### 1️⃣ **AFN (Autómata con Clausura Completa)**
- Muestra **TODOS los items** de cada estado (kernel + clausura)
- Formato: Óvalos verticales como en tu primera imagen
- Archivo generado: `lr1_afn_ejemplo.png`
- Uso: Análisis detallado del autómata

### 2️⃣ **AFD (Autómata Solo Kernel)**
- Muestra **SOLO items kernel** de cada estado
- Formato: Óvalos compactos como en tu segunda imagen
- Archivo generado: `lr1_afd_ejemplo_kernel.png`
- Uso: Visualización simplificada

---

## 📂 Archivos Modificados

### ✅ `lr1_parser/parser.py`
```python
# AFN - Clausura completa
def visualize_automaton(filename="automaton_lr1"):
    # Muestra TODOS los items (kernel + clausura)
    # Formato: óvalos verticales
    # Orientación: Top-to-Bottom

# AFD - Solo kernel
def visualize_simplified_automaton(filename="automaton_lr1_simplified"):
    # Muestra SOLO items kernel
    # Formato: óvalos compactos
    # Orientación: Top-to-Bottom
```

### ✅ `api_helper.py`
```python
def generar_graficos_base64(parser, filename_prefix="automaton_api"):
    # Retorna:
    # - automaton_afn: Base64 del AFN
    # - automaton_afd: Base64 del AFD
```

### ✅ `generar_afn_afd.py` (NUEVO)
Script standalone para generar ambos gráficos:
```bash
python generar_afn_afd.py
```

### ✅ `AFN_AFD_EXPLICACION.md` (NUEVO)
Documentación completa explicando:
- Qué es AFN y AFD en contexto LR(1)
- Diferencias visuales
- Cómo generarlos
- Contexto académico

### ✅ `API_USAGE.md`
Actualizado `/parse/graphs` con:
- Descripción de AFN vs AFD
- Ejemplos de uso
- Campos de respuesta

---

## 🚀 Cómo Usar

### Opción 1: Script Directo
```bash
python generar_afn_afd.py
```

**Resultado:**
- ✅ `lr1_afn_ejemplo.png` - AFN (8 estados, todos los items)
- ✅ `lr1_afd_ejemplo_kernel.png` - AFD (8 estados, solo kernel)

### Opción 2: Desde API
```bash
# Iniciar servidor
python main.py

# En otro terminal
curl -X POST http://localhost:8000/parse/graphs \
  -H "Content-Type: application/json" \
  -d '{"grammar": "A -> A ( A )\nA -> epsilon"}'
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "automaton_afn": "base64_del_afn...",
    "automaton_afd": "base64_del_afd..."
  }
}
```

### Opción 3: Programático
```python
from lr1_parser import Grammar, LR1Parser

grammar = Grammar()
grammar.add_production("A", ["A", "(", "A", ")"])
grammar.add_production("A", [])

parser = LR1Parser(grammar)
parser.build()

parser.visualize_automaton("mi_afn")           # AFN
parser.visualize_simplified_automaton("mi_afd") # AFD
```

---

## 📊 Ejemplo Real: A -> A ( A ) | A -> ε

### AFN (Clausura Completa)
```
Estado 0:
  S' -> . A, $
  A -> . A ( A ), $
  A -> ., $
  A -> . A ( A ), (
  A -> ., (

Estado 1:
  S' -> A ., $
  A -> A . ( A ), $
  A -> A . ( A ), (
```

### AFD (Solo Kernel)
```
Estado 0:
  S' -> . A, $

Estado 1:
  S' -> A ., $
  A -> A . ( A ), $
  A -> A . ( A ), (
```

**Mismo autómata, diferente nivel de detalle visual.**

---

## 🎓 Respuesta a tu Pregunta Original

> "¿Es posible hacerlo?"

**✅ SÍ, ya está implementado.**

Tu parser **SIEMPRE generó el autómata LR(1) correcto**, solo faltaba la **visualización en dos formatos**:

1. **AFN** = Visualización completa (kernel + clausura)
2. **AFD** = Visualización compacta (solo kernel)

**Ambos representan el MISMO autómata**, solo cambia qué items muestran visualmente.

---

## 🔑 Conceptos Clave (para tu profesor/examen)

| Concepto | Descripción |
|----------|-------------|
| **Items Kernel** | Items con punto > 0, o items iniciales |
| **Items de Clausura** | Items derivados por la función closure() |
| **AFN LR(1)** | Autómata mostrando kernel + clausura |
| **AFD LR(1)** | Autómata mostrando solo kernel |
| **Transiciones** | Idénticas en ambas visualizaciones |
| **Estados** | Mismos en ambas visualizaciones |

**NO confundir con:**
- AFN/AFD de expresiones regulares (análisis léxico)
- LALR(1) (fusión de estados)

---

## 📁 Archivos Generados

Después de ejecutar `python generar_afn_afd.py`:

```
backend-lr1/
├── lr1_afn_ejemplo.png           ← AFN (clausura completa)
├── lr1_afd_ejemplo_kernel.png    ← AFD (solo kernel)
├── generar_afn_afd.py            ← Script de generación
└── AFN_AFD_EXPLICACION.md        ← Documentación completa
```

---

## 🎯 Conclusión

✅ **Tu parser LR(1) ahora genera ambos gráficos (AFN y AFD)**  
✅ **Coinciden con la metodología que te enseñaron**  
✅ **Funcionan con cualquier gramática**  
✅ **Disponibles vía API para tu frontend**  

**¡Listo para presentar o usar en tu proyecto! 🚀**
