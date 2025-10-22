# Guía de Integración con Frontend

## 🎯 Objetivo

Este documento explica cómo integrar el Parser LR(1) con un frontend (React, Vue, Angular, etc.).

---

## 📦 Archivos Necesarios

### Backend Python:
- `lr1_parser/` - Paquete completo
- `api_helper.py` - **Funciones para API**
- `demo.py` - Incluye `parsear_gramatica_desde_texto()`

---

## 🔌 Opción 1: API REST con Flask

### 1. Instalar dependencias:
```bash
pip install flask flask-cors
```

### 2. Crear `app.py`:
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from api_helper import procesar_gramatica_api

app = Flask(__name__)
CORS(app)  # Permitir CORS para frontend

@app.route('/api/parse', methods=['POST'])
def parse_grammar():
    """
    Endpoint para procesar gramática.
    
    Request body:
    {
        "grammar": "S -> C C\nC -> c C\nC -> d"
    }
    
    Response:
    {
        "success": true,
        "grammar": {...},
        "first": {...},
        "follow": {...},
        "states": 10
    }
    """
    data = request.get_json()
    grammar_text = data.get('grammar', '')
    
    resultado = procesar_gramatica_api(grammar_text)
    
    return jsonify(resultado)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 3. Ejecutar servidor:
```bash
python app.py
```

### 4. Probar con curl:
```bash
curl -X POST http://localhost:5000/api/parse \
  -H "Content-Type: application/json" \
  -d '{"grammar": "S -> C C\nC -> c C\nC -> d"}'
```

---

## 🌐 Opción 2: API REST con FastAPI

### 1. Instalar dependencias:
```bash
pip install fastapi uvicorn
```

### 2. Crear `fastapi_app.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api_helper import procesar_gramatica_api

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GrammarRequest(BaseModel):
    grammar: str

@app.post("/api/parse")
async def parse_grammar(request: GrammarRequest):
    """Procesar gramática y retornar análisis LR(1)"""
    resultado = procesar_gramatica_api(request.grammar)
    return resultado

@app.get("/health")
async def health():
    return {"status": "ok"}

# Ejecutar con: uvicorn fastapi_app:app --reload
```

### 3. Ejecutar servidor:
```bash
uvicorn fastapi_app:app --reload --port 8000
```

### 4. Documentación automática:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 💻 Frontend - React Example

### Componente para ingresar gramática:

```jsx
import React, { useState } from 'react';

function GrammarParser() {
  const [grammar, setGrammar] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const parseGrammar = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:5000/api/parse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ grammar }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setResult(data);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Error de conexión con el servidor');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grammar-parser">
      <h2>Parser LR(1)</h2>
      
      <div className="input-section">
        <label>Ingresa tu gramática:</label>
        <textarea
          value={grammar}
          onChange={(e) => setGrammar(e.target.value)}
          placeholder="Ejemplo:&#10;S -> C C&#10;C -> c C&#10;C -> d"
          rows={10}
          cols={50}
        />
      </div>
      
      <button onClick={parseGrammar} disabled={loading}>
        {loading ? 'Procesando...' : 'Analizar Gramática'}
      </button>
      
      {error && (
        <div className="error">
          <h3>Error:</h3>
          <p>{error}</p>
        </div>
      )}
      
      {result && (
        <div className="result">
          <h3>Resultados:</h3>
          
          <div className="section">
            <h4>Producciones:</h4>
            <ul>
              {result.grammar.productions.map((prod, idx) => (
                <key={idx}>
                  {prod.non_terminal} → {prod.production.join(' ')}
                </li>
              ))}
            </ul>
          </div>
          
          <div className="section">
            <h4>Conjuntos FIRST:</h4>
            <pre>{JSON.stringify(result.first, null, 2)}</pre>
          </div>
          
          <div className="section">
            <h4>Conjuntos FOLLOW:</h4>
            <pre>{JSON.stringify(result.follow, null, 2)}</pre>
          </div>
          
          <div className="section">
            <h4>Estados del Autómata:</h4>
            <p>{result.states}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default GrammarParser;
```

---

## 🎨 Frontend - Vue Example

```vue
<template>
  <div class="grammar-parser">
    <h2>Parser LR(1)</h2>
    
    <div class="input-section">
      <label>Ingresa tu gramática:</label>
      <textarea
        v-model="grammar"
        placeholder="Ejemplo:
S -> C C
C -> c C
C -> d"
        rows="10"
        cols="50"
      ></textarea>
    </div>
    
    <button @click="parseGrammar" :disabled="loading">
      {{ loading ? 'Procesando...' : 'Analizar Gramática' }}
    </button>
    
    <div v-if="error" class="error">
      <h3>Error:</h3>
      <p>{{ error }}</p>
    </div>
    
    <div v-if="result" class="result">
      <h3>Resultados:</h3>
      
      <div class="section">
        <h4>Producciones:</h4>
        <ul>
          <li v-for="(prod, idx) in result.grammar.productions" :key="idx">
            {{ prod.non_terminal }} → {{ prod.production.join(' ') }}
          </li>
        </ul>
      </div>
      
      <div class="section">
        <h4>Estados del Autómata:</h4>
        <p>{{ result.states }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      grammar: '',
      result: null,
      loading: false,
      error: null,
    };
  },
  methods: {
    async parseGrammar() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch('http://localhost:5000/api/parse', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ grammar: this.grammar }),
        });
        
        const data = await response.json();
        
        if (data.success) {
          this.result = data;
        } else {
          this.error = data.error;
        }
      } catch (err) {
        this.error = 'Error de conexión con el servidor';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
```

---

## 📋 Formato de Datos

### Request (Frontend → Backend):
```json
{
  "grammar": "S -> C C\nC -> c C\nC -> d"
}
```

### Response (Backend → Frontend):
```json
{
  "success": true,
  "error": null,
  "grammar": {
    "productions": [
      {
        "id": 1,
        "non_terminal": "S",
        "production": ["C", "C"]
      },
      {
        "id": 2,
        "non_terminal": "C",
        "production": ["c", "C"]
      },
      {
        "id": 3,
        "non_terminal": "C",
        "production": ["d"]
      }
    ],
    "terminals": ["$", "c", "d"],
    "non_terminals": ["C", "S", "S'"]
  },
  "first": {
    "C": ["c", "d"],
    "S": ["c", "d"],
    "S'": ["c", "d"]
  },
  "follow": {
    "C": ["$", "c", "d"],
    "S": ["$"],
    "S'": ["$"]
  },
  "states": 10,
  "conflicts": []
}
```

---

## ⚙️ Configuración de Producción

### 1. Usar variables de entorno:
```python
# config.py
import os

CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
PORT = int(os.getenv('PORT', 5000))
```

### 2. Dockerfile (opcional):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### 3. requirements.txt:
```
flask==2.3.0
flask-cors==4.0.0
graphviz==0.20.1
```

---

## 🚀 Despliegue

### Opciones:
1. **Heroku** - `heroku create` + `git push heroku main`
2. **Railway** - Conectar repositorio GitHub
3. **Render** - Deploy automático
4. **AWS Lambda** - Serverless con API Gateway
5. **Google Cloud Run** - Contenedor automático

---

## 🔒 Seguridad

### Recomendaciones:
1. **Validar entrada:**
   ```python
   if len(grammar_text) > 10000:
       return {"error": "Gramática demasiado grande"}
   ```

2. **Rate limiting:**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

3. **CORS específico en producción:**
   ```python
   CORS(app, origins=["https://tu-frontend.com"])
   ```

---

## ✅ Testing

### Test de integración:
```python
import requests

# Test básico
response = requests.post('http://localhost:5000/api/parse', json={
    'grammar': 'S -> C C\nC -> c C\nC -> d'
})

assert response.status_code == 200
data = response.json()
assert data['success'] == True
assert data['states'] == 10
```

---

**¡Tu parser LR(1) está listo para el frontend!** 🎉
