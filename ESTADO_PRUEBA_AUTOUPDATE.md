# 🧪 Estado de la Prueba de Auto-Update

**Fecha:** 10 de febrero de 2026, 10:35  
**Estado:** ✅ EN PROGRESO

---

## ✅ Cambios Realizados

### 1. Modificación del Código ✅
**Archivo modificado:** `main.py`  
**Cambio realizado:** 
```python
# ANTES:
app = FastAPI(title="🦖 Museo de Dinosaurios", ...)

# DESPUÉS:
app = FastAPI(
    title="🦖 Museo de Dinosaurios - AUTO-UPDATE FUNCIONANDO ✅", 
    version="2.0.0"
)
```

### 2. Commit y Push ✅
```
Commit: edc1d6e
Mensaje: "test: probar auto-update de Watchtower - cambio visible en título"
Estado: Pusheado a origin/main
```

---

## 📊 Timeline del Proceso

```
┌─────────────────────────────────────────────────────────────┐
│                    LÍNEA DE TIEMPO                          │
└─────────────────────────────────────────────────────────────┘

✅ 10:35 - Push a GitHub
    └─> Trigger GitHub Actions

⏳ 10:35-10:38 - GitHub Actions (EN PROGRESO - 2-3 min)
    ├─> Job 1: Tests & Linting
    ├─> Job 2: Build Docker & Push a Docker Hub
    └─> Job 3: Notifications

⏱️  10:38-10:43 - Watchtower esperando (máximo 5 min)
    └─> Próxima revisión programada: ~10:37 (cada 5 min)

🎯 10:38-10:43 - Auto-Update (when ready)
    ├─> Detectar nueva imagen
    ├─> Pull nueva imagen
    ├─> Stop contenedor viejo
    ├─> Start contenedor nuevo
    └─> ✅ ACTUALIZACIÓN COMPLETA

📍 ESTAMOS AQUÍ: GitHub Actions ejecutándose...
```

---

## 🔍 Cómo Verificar Cada Etapa

### Etapa 1: GitHub Actions (AHORA)
**URL:** https://github.com/Thomas-Casot/fastapi_plantillascomunes/actions

**Qué buscar:**
- ✅ Job "Test" completado (verde)
- ✅ Job "Docker Build & Push" completado (verde)
- ✅ Job "Notifications" completado (verde)
- ⏱️ Tiempo total: 2-3 minutos

**Comando alternativo:**
```powershell
# Ver estado del workflow (requiere GitHub CLI)
gh run list --limit 1
```

---

### Etapa 2: Docker Hub (Después de GitHub Actions)
**URL:** https://hub.docker.com/r/thomascasot/museo-dinosaurios/tags

**Qué buscar:**
- Nueva imagen con tag `latest`
- Timestamp actualizado (hace pocos minutos)
- Tamaño de la imagen

---

### Etapa 3: Watchtower (Automático - máx 5 min)

**Opción A: Ver logs en tiempo real**
```powershell
# Ejecutar en una nueva terminal
.\monitor_watchtower.ps1

# O directamente:
docker logs -f watchtower
```

**Qué buscar en los logs:**
```
✅ ESTO ES LO QUE VERÁS cuando funcione:

time="..." level=info msg="Found new thomascasot/museo-dinosaurios:latest image (sha256:..."
time="..." level=info msg="Stopping /museo-dinosaurios-app with SIGTERM"
time="..." level=info msg="Creating /museo-dinosaurios-app"
time="..." level=info msg="Starting /museo-dinosaurios-app"
```

**Opción B: Ver logs de la app**
```powershell
# Ejecutar en otra terminal
.\monitor_app.ps1

# O directamente:
docker logs -f museo-dinosaurios-app
```

**Qué buscar:**
```
✅ REINICIO del servidor:

INFO:     Shutting down
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### Etapa 4: Verificación Final

**Verificar en el navegador:**
```
1. Ir a: http://localhost:8000/docs
2. Debería ver el título actualizado:
   "🦖 Museo de Dinosaurios - AUTO-UPDATE FUNCIONANDO ✅"
3. Version: 2.0.0
```

**Comando para verificar versión de la imagen:**
```powershell
docker inspect museo-dinosaurios-app | Select-String "Image"
```

---

## ⏱️ Tiempo Estimado Total

| Etapa | Tiempo | Estado |
|-------|--------|--------|
| Push a GitHub | Instantáneo | ✅ Completado |
| GitHub Actions | 2-3 minutos | ⏳ En progreso |
| Espera Watchtower | 0-5 minutos | ⏸️ Pendiente |
| Auto-Update | 10-20 segundos | ⏸️ Pendiente |
| **TOTAL** | **6-8 minutos** | **~5 min restantes** |

---

## 🎯 Qué Hacer Ahora

### Opción 1: Esperar Pacientemente (Recomendado)
```powershell
# Terminal 1: Monitorear Watchtower
.\monitor_watchtower.ps1

# Terminal 2: Monitorear App (en otra ventana)
.\monitor_app.ps1

# Esperar 5-8 minutos y ver la magia ✨
```

### Opción 2: Forzar Update Inmediato (Si tienes prisa)
```powershell
# Espera a que GitHub Actions termine (2-3 min)
# Luego fuerza la actualización:

docker run --rm `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -e DOCKER_API_VERSION=1.44 `
  containrrr/watchtower:latest `
  --run-once `
  --cleanup `
  museo-dinosaurios-app
```

### Opción 3: Verificar Manualmente
```powershell
# 1. Verificar que GitHub Actions terminó
# URL: https://github.com/Thomas-Casot/fastapi_plantillascomunes/actions

# 2. Verificar imagen en Docker Hub
# URL: https://hub.docker.com/r/thomascasot/museo-dinosaurios

# 3. Ver cuándo revisará Watchtower
docker logs watchtower | Select-String "Scheduling"

# 4. Ver versión actual de la app
docker exec museo-dinosaurios-app python -c "import main; print(main.app.version)"
```

---

## 📸 Evidencias para la Entrega

### Screenshots Recomendados:

1. **GitHub Actions completado** ✅
   - Captura de pantalla de GitHub → Actions → Workflow exitoso

2. **Docker Hub actualizado** ✅
   - Captura de https://hub.docker.com/r/thomascasot/museo-dinosaurios/tags

3. **Logs de Watchtower** ✅
   - Captura mostrando "Found new image" y "Starting"

4. **Aplicación actualizada** ✅
   - Captura de http://localhost:8000/docs mostrando nuevo título

5. **docker-compose.yml** ✅
   - Mostrar configuración de Watchtower

---

## 🐛 Si Algo Va Mal

### GitHub Actions falla:
```powershell
# Ver logs del workflow
gh run view

# Si no tienes GitHub CLI, ve a:
# https://github.com/Thomas-Casot/fastapi_plantillascomunes/actions
```

### Watchtower no detecta cambios:
```powershell
# Verificar que la imagen se actualizó en Docker Hub
# Forzar pull manual:
docker pull thomascasot/museo-dinosaurios:latest

# Reiniciar contenedor manualmente:
docker-compose restart app
```

### La app no arranca:
```powershell
# Ver logs de error:
docker logs museo-dinosaurios-app --tail 50

# Verificar health check:
docker inspect museo-dinosaurios-app | Select-String "Health"
```

---

## ✅ Checklist de Verificación

- [x] Código modificado con cambio visible
- [x] Commit realizado
- [x] Push a GitHub exitoso
- [ ] GitHub Actions completado (esperar 2-3 min)
- [ ] Nueva imagen en Docker Hub
- [ ] Watchtower detectó cambio (esperar máx 5 min)
- [ ] Contenedor reiniciado automáticamente
- [ ] Cambios visibles en http://localhost:8000/docs
- [ ] Screenshots capturados para entrega

---

**Estado actual:** ⏳ Esperando que GitHub Actions termine...  
**Próximo paso:** Monitorear Watchtower cuando la imagen esté en Docker Hub  
**Tiempo estimado restante:** ~5-8 minutos

---

*Actualizado: 10 de febrero de 2026, 10:35*
