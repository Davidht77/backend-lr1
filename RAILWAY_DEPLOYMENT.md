# 🚂 Deployment en Railway - Parser LR(1) API

## ⚠️ Problema: Gráficos retornan `null`

Si los gráficos retornan `null` en producción, es porque **Graphviz no está instalado** como dependencia del sistema.

## ✅ Solución

Railway soporta dos métodos de deployment:

### Opción 1: Nixpacks (Recomendado) ⭐

Railway usa Nixpacks por defecto si no hay Dockerfile. El archivo `nixpacks.toml` ya está configurado:

```toml
[phases.setup]
nixPkgs = ["graphviz"]
```

**⚠️ IMPORTANTE:** Railway prioriza Dockerfile sobre Nixpacks. Si tienes ambos archivos, Railway usará Docker.

**Pasos:**
1. **Asegúrate de NO tener un `Dockerfile` en la raíz** (debe estar renombrado a `Dockerfile.backup`)
2. Verifica que `nixpacks.toml` esté en la raíz del proyecto
3. Haz commit y push:
   ```bash
   git add nixpacks.toml railway.json
   git commit -m "Configure Nixpacks with Graphviz for Railway"
   git push
   ```
4. Railway detectará automáticamente Nixpacks
5. Verifica en los logs que diga: **"Building with Nixpacks"**

### Opción 2: Docker (Alternativa)

Si prefieres usar Docker, Railway también lo soporta:

**Pasos:**
1. En Railway, ve a Settings → Deploy
2. Cambia el Builder a "Dockerfile"
3. Redeploy el proyecto

El `Dockerfile` ya incluye la instalación de Graphviz:
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends graphviz
```

## 🔍 Verificación

Después del deployment, verifica que Graphviz esté instalado:

1. **Health Check:**
   ```bash
   curl https://tu-app.railway.app/health
   ```
   
   Deberías ver:
   ```json
   {
     "status": "healthy",
     "service": "lr1-parser-api",
     "graphviz_available": true,
     "graphviz_path": "/nix/store/.../bin/dot"
   }
   ```

2. **Test de gráficos:**
   ```bash
   curl -X POST https://tu-app.railway.app/parse/graphs \
     -H "Content-Type: application/json" \
     -d '{"grammar": "S -> A\nA -> a"}'
   ```
   
   Deberías ver:
   ```json
   {
     "success": true,
     "data": {
       "automaton_afn": "iVBORw0KGgo...",
       "automaton_afd": "iVBORw0KGgo..."
     }
   }
   ```

## 📋 Checklist de Deployment

- [ ] `nixpacks.toml` está en la raíz del proyecto
- [ ] `requirements_api.txt` incluye `graphviz>=0.20`
- [ ] Railway está configurado para usar Nixpacks (o Dockerfile)
- [ ] Variables de entorno configuradas (si aplica)
- [ ] Endpoint `/health` retorna `graphviz_available: true`
- [ ] Endpoint `/parse/graphs` retorna imágenes base64 válidas

## 🐛 Troubleshooting

### Los gráficos siguen retornando `null`

1. **Verifica los logs de Railway:**
   - Ve a Deployments → Latest Deployment → View Logs
   - Busca errores de tipo: `[ERROR] Error generando AFD`

2. **Verifica que Graphviz se instaló:**
   - En los logs de build, busca: `graphviz`
   - Debe aparecer en la lista de paquetes instalados

3. **Fuerza un rebuild:**
   - Settings → Deploy → Redeploy

4. **Prueba localmente con Docker:**
   ```bash
   docker build -t lr1-parser-api .
   docker run -p 8000:8000 lr1-parser-api
   ```
   Luego visita: http://localhost:8000/health

## 🔗 Variables de Entorno

Railway no requiere configuración adicional para este proyecto, pero puedes agregar:

```bash
# Opcional: Modo debug
DEBUG=true

# Puerto (Railway lo configura automáticamente)
PORT=8000
```

## 📦 Archivos Importantes

- `nixpacks.toml` - Configuración de Nixpacks (incluye Graphviz)
- `Dockerfile` - Configuración Docker alternativa
- `railway.json` - Configuración específica de Railway
- `requirements_api.txt` - Dependencias de Python
- `.dockerignore` - Archivos excluidos del build Docker

## 🚀 Deploy Completo

```bash
# 1. Añadir archivos de configuración
git add nixpacks.toml Dockerfile railway.json .dockerignore

# 2. Commit
git commit -m "Configure Railway deployment with Graphviz support"

# 3. Push
git push origin main

# 4. Railway detectará los cambios y redeployará automáticamente
```

## ✅ Resultado Esperado

Después del deployment exitoso:

```json
// GET /health
{
  "status": "healthy",
  "service": "lr1-parser-api",
  "graphviz_available": true,
  "graphviz_path": "/nix/store/xyz.../bin/dot"
}

// POST /parse con generate_graphs: true
{
  "success": true,
  "data": {
    "graphs": {
      "automaton_afn": "iVBORw0KGgoAAAA...",  // ✓ No null
      "automaton_afd": "iVBORw0KGgoAAAA..."   // ✓ No null
    }
  }
}
```
