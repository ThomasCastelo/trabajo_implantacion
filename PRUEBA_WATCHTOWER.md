# 🧪 Guía de Prueba de Watchtower

## ✅ Sistema Levantado

Los contenedores están corriendo:
- **App**: http://localhost:8000
- **Watchtower**: Monitoreando cada 5 minutos

---

## 🔬 Cómo Probar el Auto-Update

### Opción 1: Prueba Rápida (Recomendada)

1. **Hacer un cambio visible en el código:**

```python
# En main.py, busca la ruta raíz y añade algo visible:

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "mensaje": "ACTUALIZACIÓN AUTOMÁTICA FUNCIONANDO! ✅",  # <- AÑADIR ESTO
        # resto del código...
    })
```

2. **Hacer commit y push:**

```powershell
git add main.py
git commit -m "test: probar auto-update de watchtower"
git push origin main
```

3. **Esperar el pipeline (2-3 minutos):**
   - Ve a GitHub → Actions
   - Espera a que termine el pipeline
   - Verifica en Docker Hub que hay nueva imagen

4. **Esperar a Watchtower (máximo 5 minutos):**

```powershell
# Ver logs en tiempo real de watchtower
docker logs -f watchtower

# En otra terminal, ver cuando la app se reinicia
docker logs -f museo-dinosaurios-app
```

5. **Verificar el cambio:**
   - Abre http://localhost:8000
   - Deberías ver el mensaje actualizado

---

### Opción 2: Probar Inmediatamente (Sin Esperar)

Si no quieres esperar 5 minutos, puedes forzar a Watchtower a revisar ahora:

```powershell
# Parar watchtower
docker stop watchtower

# Levantarlo de nuevo con intervalo de 30 segundos (solo para pruebas)
docker run -d --name watchtower-test `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -e DOCKER_API_VERSION=1.44 `
  -e WATCHTOWER_LABEL_ENABLE=true `
  -e WATCHTOWER_CLEANUP=true `
  containrrr/watchtower:latest `
  --interval 30

# Ver logs en tiempo real
docker logs -f watchtower-test
```

---

### Opción 3: Actualización Manual (Para Verificar que Funciona)

```powershell
# Forzar actualización inmediata (run once)
docker run --rm `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -e DOCKER_API_VERSION=1.44 `
  containrrr/watchtower:latest `
  --run-once `
  --cleanup `
  museo-dinosaurios-app
```

---

## 📋 Comandos Útiles

### Ver logs en tiempo real:
```powershell
# Watchtower
docker logs -f watchtower

# App
docker logs -f museo-dinosaurios-app
```

### Ver estado de contenedores:
```powershell
docker ps
```

### Ver última actualización de la imagen:
```powershell
docker images | Select-String "museo-dinosaurios"
```

### Reiniciar servicios:
```powershell
docker-compose restart
```

### Parar todo:
```powershell
docker-compose down
```

### Levantar todo:
```powershell
docker-compose up -d
```

---

## 🎯 Qué Esperar Ver en los Logs

### Watchtower detectando actualización:
```
time="..." level=info msg="Found new thomascasot/museo-dinosaurios:latest image"
time="..." level=info msg="Stopping /museo-dinosaurios-app with SIGTERM"
time="..." level=info msg="Starting /museo-dinosaurios-app"
```

### App reiniciándose:
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## ✅ Checklist de Verificación

- [ ] GitHub Actions pipeline completado exitosamente
- [ ] Nueva imagen publicada en Docker Hub
- [ ] Watchtower detectó la actualización (ver logs)
- [ ] Contenedor app se reinició automáticamente
- [ ] Cambios visibles en http://localhost:8000
- [ ] Imagen vieja eliminada (si CLEANUP=true)

---

## 🐛 Troubleshooting

### Watchtower no detecta cambios:
- Verifica que la imagen en Docker Hub sea más reciente
- Verifica que el label `watchtower.enable=true` está en el contenedor
- Revisa logs: `docker logs watchtower`

### App no se actualiza:
- Verifica que el contenedor tiene el label correcto
- Fuerza pull: `docker pull thomascasot/museo-dinosaurios:latest`
- Reinicia manualmente: `docker-compose restart app`

### Error de API version:
- Ya está solucionado con `DOCKER_API_VERSION=1.44`
- Si persiste, verifica versión de Docker Desktop

---

**Tiempo total del flujo completo:** 6-8 minutos desde push hasta ver cambios
