# 📋 RESUMEN: Archivos del Proyecto LR(1)

## ✅ ARCHIVOS NECESARIOS (NO BORRAR)

### 1. `lr1_parser.py` ⭐ **ARCHIVO PRINCIPAL**
- **Tamaño**: ~731 líneas
- **Descripción**: Contiene TODA la lógica del parser LR(1)
- **Componentes**:
  - `Grammar`: Manejo de gramáticas
  - `LR1Item`: Items LR(1)
  - `LR1Parser`: Parser completo
- **Funciones clave**:
  - Cálculo de FIRST y FOLLOW
  - Construcción del autómata
  - Tabla de parsing
  - Visualización gráfica (2 tipos)

### 2. `demo.py` 🎯 **INTERFAZ DE USUARIO**
- **Tamaño**: ~455 líneas
- **Descripción**: Demo interactivo con menú
- **Incluye**: 6 gramáticas predefinidas
- **Uso**: `python demo.py`

### 3. `requirements.txt` 📦 **DEPENDENCIAS**
- **Contenido**: `graphviz`
- **Instalación**: `pip install -r requirements.txt`

### 4. `README.md` 📖 **DOCUMENTACIÓN**
- **Descripción**: Manual completo de uso
- **Incluye**: Instalación, uso, ejemplos

## ⚠️ ARCHIVOS OPCIONALES

### 5. `test_parser.py` 🧪
- Tests unitarios
- Recomendado para desarrollo
- Puede eliminarse si no desarrollas

## ❌ ARCHIVOS QUE SE PUEDEN BORRAR

### Imágenes PNG (se regeneran automáticamente)
- `automaton_*.png`
- `automaton_*_simplified.png`

### Archivos del sistema
- `__pycache__/` - Se regenera automáticamente
- `.git/` - Control de versiones (mantener si usas Git)
- `.gitignore` - Control de versiones (mantener si usas Git)

## 🎯 ARCHIVOS MÍNIMOS PARA FUNCIONAR

Para que el programa funcione, necesitas SOLO estos 3 archivos:

```
backend-lr1/
├── lr1_parser.py       ⭐ OBLIGATORIO
├── demo.py             ⭐ OBLIGATORIO
└── requirements.txt    ⭐ OBLIGATORIO
```

Con estos 3 archivos el programa funciona completamente.

## 📊 RESUMEN RÁPIDO

| Archivo | ¿Necesario? | ¿Se puede borrar? |
|---------|-------------|-------------------|
| `lr1_parser.py` | ✅ SÍ | ❌ NO |
| `demo.py` | ✅ SÍ | ❌ NO |
| `requirements.txt` | ✅ SÍ | ❌ NO |
| `README.md` | ⚠️ Recomendado | ✅ Sí (pero no es buena idea) |
| `test_parser.py` | ⚠️ Opcional | ✅ Sí |
| `*.png` | ❌ NO | ✅ Sí (se regeneran) |
| `__pycache__/` | ❌ NO | ✅ Sí (se regenera) |
| `.git/` | ⚠️ Solo para Git | ✅ Sí (si no usas Git) |

## 🚀 PARA EMPEZAR

1. Asegúrate de tener estos archivos:
   - ✅ `lr1_parser.py`
   - ✅ `demo.py`
   - ✅ `requirements.txt`

2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta:
   ```bash
   python demo.py
   ```

4. Los gráficos PNG se generarán automáticamente al seleccionar una gramática.

## 💡 NOTA IMPORTANTE

El archivo `lr1_parser.py` es el **corazón del sistema**. Contiene:
- Todas las clases
- Toda la lógica del parser
- Todas las funciones de visualización

Sin este archivo, nada funciona. Los demás archivos solo lo complementan.
