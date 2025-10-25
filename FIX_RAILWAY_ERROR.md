# 🚨 SOLUCIÓN AL ERROR: pip: command not found

## ❌ Error Actual

```
/bin/bash: line 1: pip: command not found
ERROR: failed to build: failed to solve: process "/bin/bash -ol pipefail -c pip install -r requirements_api.txt" did not complete successfully: exit code: 127
```

## 🔍 Causa

Railway está detectando el `Dockerfile` y lo está usando automáticamente, pero está generando su propio Dockerfile que no funciona correctamente.

## ✅ Solución - Elige UNA opción:

### Opción 1: Usar Nixpacks (RECOMENDADO - Más simple)

**Paso 1:** Renombra o elimina el Dockerfile temporalmente

```bash
# Renombrar
mv Dockerfile Dockerfile.backup

# O eliminar
rm Dockerfile
```

**Paso 2:** Asegúrate de que `nixpacks.toml` esté presente:

```bash
git add nixpacks.toml railway.json
git commit -m "Use Nixpacks for deployment"
git push
```

**Paso 3:** Railway usará Nixpacks automáticamente y detectará el `nixpacks.toml`

---

### Opción 2: Forzar Nixpacks en Railway Web UI

**Paso 1:** Ve a tu proyecto en Railway

**Paso 2:** Settings → Environment → Builder

**Paso 3:** Selecciona "Nixpacks" (no "Dockerfile")

**Paso 4:** Redeploy

---

### Opción 3: Usar Dockerfile (Si prefieres Docker)

**Paso 1:** Elimina `nixpacks.toml` y `railway.json`

```bash
rm nixpacks.toml railway.json
```

**Paso 2:** Asegúrate de que el Dockerfile esté correcto:

```dockerfile
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends graphviz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements_api.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_api.txt

COPY . .

ENV PORT=8000
EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
```

**Paso 3:** Commit y push:

```bash
git add Dockerfile
git commit -m "Use Docker for deployment with Graphviz"
git push
```

---

## 🎯 Recomendación: Opción 1 (Nixpacks)

**Es más simple y Railway lo maneja mejor.**

### Comandos completos:

```bash
# 1. Renombrar Dockerfile para evitar conflictos
git mv Dockerfile Dockerfile.backup

# 2. Commit los cambios
git add nixpacks.toml railway.json
git commit -m "Configure Nixpacks with Graphviz for Railway"

# 3. Push
git push origin main

# 4. Railway redeployará automáticamente usando Nixpacks
```

---

## 🔍 Verificar qué builder está usando Railway

**Logs de Railway:**
- Si dice **"Building with Nixpacks"** ✓ Correcto
- Si dice **"Building Dockerfile"** ✗ Incorrecto (si quieres Nixpacks)

---

## ✅ Después del deployment exitoso

Verifica con:

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

---

## 📋 Resumen de Archivos

### Si usas NIXPACKS (Recomendado):
- ✅ Mantén: `nixpacks.toml`, `railway.json`
- ❌ Renombra: `Dockerfile` → `Dockerfile.backup`

### Si usas DOCKER:
- ✅ Mantén: `Dockerfile`
- ❌ Elimina: `nixpacks.toml`, `railway.json`

---

## 🐛 Si sigue fallando

1. **Revisa los logs de Railway** para ver qué builder está usando
2. **Fuerza un rebuild** desde Railway UI
3. **Verifica que solo tengas UNO de estos:**
   - `nixpacks.toml` (para Nixpacks)
   - `Dockerfile` (para Docker)
   - NO ambos al mismo tiempo

---

## 💡 Tip

Railway detecta automáticamente el builder en este orden:
1. Si existe `Dockerfile` → usa Docker
2. Si existe `nixpacks.toml` → usa Nixpacks
3. Si ninguno existe → detecta automáticamente por lenguaje

**Por eso, si quieres usar Nixpacks, DEBES renombrar/eliminar el Dockerfile.**
