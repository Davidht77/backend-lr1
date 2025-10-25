# 🔧 SOLUCIÓN COMPLETA: Gráficos retornan NULL en Railway

## 🎯 Problema

Los gráficos del autómata retornan `null` cuando el API está deployado en Railway:

```json
"graphs": {
    "automaton_afn": null,
    "automaton_afd": null
}
```

## 💡 Causa

**Graphviz no está instalado como dependencia del sistema** en Railway. 

La librería Python `graphviz` está instalada, pero necesita el ejecutable `dot` del sistema para generar los gráficos PNG.

## ✅ Solución

### Paso 1: Añadir archivos de configuración

Ya están creados en tu repositorio:

- ✅ `nixpacks.toml` - Configura Nixpacks para instalar Graphviz
- ✅ `Dockerfile` - Alternativa con Docker
- ✅ `railway.json` - Configuración de Railway
- ✅ `.dockerignore` - Optimización de build

### Paso 2: Hacer commit y push

```bash
git add nixpacks.toml Dockerfile railway.json .dockerignore RAILWAY_DEPLOYMENT.md
git commit -m "Add Graphviz system dependency for Railway deployment"
git push origin main
```

### Paso 3: Redeploy en Railway

Railway detectará automáticamente los cambios y redeployará.

**O fuerza un redeploy:**
1. Ve a tu proyecto en Railway
2. Settings → Deploy
3. Click en "Redeploy"

### Paso 4: Verificar

**1. Health Check:**
```bash
curl https://tu-app.railway.app/health
```

**Resultado esperado:**
```json
{
  "status": "healthy",
  "service": "lr1-parser-api",
  "graphviz_available": true,  // ← Debe ser true
  "graphviz_path": "/nix/store/.../bin/dot"
}
```

**2. Test de gráficos:**
```bash
curl -X POST https://tu-app.railway.app/parse \
  -H "Content-Type: application/json" \
  -d '{
    "grammar": "S -> C C\nC -> c C\nC -> d",
    "generate_graphs": true
  }'
```

**Resultado esperado:**
```json
{
  "success": true,
  "data": {
    "graphs": {
      "automaton_afn": "iVBORw0KGgo...",  // ✓ Base64 válido
      "automaton_afd": "iVBORw0KGgo..."   // ✓ Base64 válido
    }
  }
}
```

## 📋 Cambios Realizados

### 1. `nixpacks.toml` (NUEVO)
```toml
[phases.setup]
nixPkgs = ["...", "graphviz"]  # ← Instala Graphviz del sistema
```

### 2. `Dockerfile` (NUEVO)
```dockerfile
RUN apt-get install -y graphviz  # ← Instala Graphviz en Docker
```

### 3. `main.py` (ACTUALIZADO)
```python
@app.get("/health")
def health_check():
    # Ahora verifica si Graphviz está disponible
    graphviz_installed = shutil.which("dot") is not None
    return {
        "graphviz_available": graphviz_installed,
        "graphviz_path": shutil.which("dot")
    }
```

### 4. `api_helper.py` (ACTUALIZADO)
```python
# Ahora tiene logging detallado para debug
print(f"[DEBUG] Generando AFD en: {afn_path}")
print(f"[DEBUG] Existe: {os.path.exists(expected_file)}")
```

## 🐛 Si sigue sin funcionar

### 1. Verifica los logs de Railway

En Railway → Deployments → Latest → View Logs

Busca:
- ✅ `Installing graphviz` durante el build
- ❌ `[ERROR] Error generando AFD` durante runtime

### 2. Fuerza uso de Nixpacks

Si Railway está usando otro builder:
1. Settings → Deploy
2. Builder: Nixpacks
3. Config file path: `nixpacks.toml`
4. Redeploy

### 3. Prueba con Docker localmente

```bash
# Build
docker build -t lr1-parser-test .

# Run
docker run -p 8000:8000 lr1-parser-test

# Test
curl http://localhost:8000/health
```

## 📞 Siguiente paso para el Frontend

Una vez que los gráficos funcionen en Railway, asegúrate de que el frontend esté llamando correctamente:

```typescript
const response = await fetch('https://tu-app.railway.app/parse', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    grammar: grammarText,
    generate_graphs: true  // ← IMPORTANTE!
  })
});

const result = await response.json();
const graphs = result.data.graphs; // ← Aquí estarán las imágenes
```

## 📚 Documentación Completa

- **Deployment:** [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
- **API Usage:** [API_USAGE.md](API_USAGE.md)
- **Frontend Fix:** [SOLUCION_FRONTEND.md](SOLUCION_FRONTEND.md)

## ✅ Resumen

1. ✅ Archivos de configuración creados
2. ✅ Health check actualizado para verificar Graphviz
3. ✅ Logging mejorado para debug
4. 🔄 **Falta:** Hacer commit y push a Railway
5. 🔄 **Falta:** Verificar deployment con `/health`
6. 🔄 **Falta:** Probar generación de gráficos
