# CI/CD y Watchtower - FastAPI Museo de Dinosaurios

## 🔄 Flujo Completo de Deployment Automático

### 1️⃣ CI/CD (GitHub Actions)

Cuando haces `git push origin main`:

1. **Test Job** → Ejecuta tests y linting de código Python
2. **Docker Build & Push** → Construye imagen Docker y la sube a Docker Hub
3. **Notifications** → Confirma que todo fue exitoso

**Archivo:** `.github/workflows/docker-ci-cd.yml`

**Resultado:** Imagen `thomascasot/museo-dinosaurios:latest` en Docker Hub

---

### 2️⃣ Watchtower (Auto-Update)

Watchtower monitorea Docker Hub cada 5 minutos:

```yaml
# docker-compose.yml
watchtower:
  image: containrrr/watchtower
  command: --interval 300 --cleanup
```

**Qué hace:**
- Revisa si hay nueva versión de `museo-dinosaurios:latest`
- Si detecta cambio → Para contenedor viejo
- Descarga nueva imagen
- Levanta contenedor con código actualizado

---

### 3️⃣ Workflow Completo

```
Código local → git push → GitHub Actions → Docker Hub → Watchtower → Servidor
     ↓             ↓            ↓              ↓           ↓          ↓
  Editas       Sube a      Tests +         Sube       Detecta    Auto-update
  archivo      GitHub      Build          imagen      cambio     en 5 min
```

---

## 🛠️ Comandos Importantes

### Desarrollo Local (con hot-reload)
```powershell
docker-compose -f docker-compose.dev.yml up -d
# Cambios en templates requieren: docker restart museo-dinosaurios-dev
```

### Producción (con Watchtower)
```powershell
git add .
git commit -m "Feature: ..."
git push origin main
# → Espera 5-10 min y Watchtower actualiza automáticamente
```

---

## ⚙️ Configuración

**Secrets requeridos en GitHub:**
- `DOCKERHUB_USERNAME`: thomascasot
- `DOCKERHUB_TOKEN`: Access token de Docker Hub

**Repositorio Docker Hub:** 
- `thomascasot/museo-dinosaurios`

---

## 📊 Tiempos Aproximados

- GitHub Actions (build + push): **1-2 minutos**
- Watchtower (siguiente revisión): **máximo 5 minutos**
- **Total desde push hasta actualización:** 6-7 minutos
