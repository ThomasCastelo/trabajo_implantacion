# 🚀 DevOps & CI/CD - Museo de Dinosaurios FastAPI

## Descripción General

Este documento describe la configuración de DevOps y CI/CD para la aplicación FastAPI "Museo de Dinosaurios".

### Componentes Principales

1. **Docker**: Containerización de la aplicación
2. **GitHub Actions**: Pipeline de integración continua
3. **Docker Hub**: Registro de imágenes Docker
4. **Git**: Control de versiones

---

## 🐳 Docker

### Dockerfile Multi-stage

La aplicación utiliza un Dockerfile con dos etapas:

#### Stage 1: Builder
- Imagen base: `python:3.11-slim`
- Instala dependencias necesarias
- Compila las librerías Python
- Limpia archivos innecesarios (`__pycache__`, `.pyc`)

#### Stage 2: Runtime
- Imagen base: `python:3.11-slim`
- Copia solo lo necesario del builder
- Crea usuario no-root para mayor seguridad
- Variables de entorno optimizadas
- Health check configurado

### Ventajas del enfoque multi-stage

✅ **Menor tamaño final** (no incluye herramientas de compilación)
✅ **Mayor seguridad** (usuario no-root)
✅ **Mejor rendimiento** (menos capas innecesarias)
✅ **Cacheo eficiente** (reutilización de capas)

### Comandos Docker

```bash
# Construir imagen
docker build -t museo-dinosaurios:latest .

# Ejecutar contenedor
docker run -p 8000:8000 museo-dinosaurios:latest

# Usar docker-compose
docker-compose up -d
docker-compose down
```

---

## 🔄 GitHub Actions CI/CD

### Pipeline automatizado

El workflow `docker-ci-cd.yml` se ejecuta en:
- **Eventos**: Push y Pull Requests
- **Ramas**: main y develop

### Etapas del Pipeline

#### 1️⃣ **Test Job**
```yaml
- Checkout del código
- Setup Python 3.11
- Instalación de dependencias
- Linting con Flake8
```

**Triggers**: Siempre se ejecuta en push o PR

#### 2️⃣ **Docker Build & Push**
```yaml
- Setup Docker Buildx
- Login a Docker Hub
- Build de imagen Docker
- Push a Docker Hub (solo en push a main/develop)
```

**Triggers**: Solo después de pasar tests
**Condiciones**: Solo en push a main/develop (no en PR)

#### 3️⃣ **Notifications**
```yaml
- Verifica estado del pipeline
- Notifica resultado final
```

### Flujo Visual

```
┌─── Push a GitHub ───┐
│                      │
│  Trigger Workflow    │
│         │            │
│         ▼            │
│  ┌──────────────┐    │
│  │  Test Job   │    │
│  └──────┬───────┘    │
│         │ Success    │
│         ▼            │
│  ┌──────────────────────┐
│  │ Docker Build & Push  │
│  │ (si es push a main)  │
│  └──────┬───────────────┘
│         │ Success
│         ▼
│  ┌──────────────┐
│  │ Notifications│
│  └──────────────┘
│
└──────────────────────┘
```

---

## 🏷️ Tagging Strategy

### Tags Docker

La imagen se taguea automáticamente con:

| Tag | Propósito | Ejemplo |
|-----|-----------|---------|
| `latest` | Última versión (rama main) | `usuario/museo:latest` |
| `develop` | Rama de desarrollo | `usuario/museo:develop` |
| Rama | Nombre de rama | `usuario/museo:feature-x` |
| SHA | Hash del commit | `usuario/museo:main-a1b2c3d` |

---

## 🔐 Secretos GitHub necesarios

Configurar en GitHub → Settings → Secrets and variables:

```
DOCKERHUB_USERNAME = tu_usuario_dockerhub
DOCKERHUB_TOKEN = tu_token_dockerhub
```

### Obtener Docker Hub Token

1. Login en [Docker Hub](https://hub.docker.com/)
2. Settings → Security → New Access Token
3. Guardar en GitHub Secrets

---

## 📋 Requisitos previos

### Instalar Git

```bash
# Windows
choco install git
# o descargar desde https://git-scm.com/

# Linux
sudo apt-get install git

# macOS
brew install git
```

### Instalar Docker

```bash
# Windows/Mac: Docker Desktop
# https://www.docker.com/products/docker-desktop

# Linux
sudo apt-get install docker.io
sudo usermod -aG docker $USER
```

---

## 📤 Subir a GitHub

### Primero: Inicializar repositorio local

```bash
cd c:\implantacion\fastapi_plantillascomunes
git init
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
git add .
git commit -m "Initial commit: Museo de Dinosaurios FastAPI"
```

### Segundo: Conectar con repositorio remoto

```bash
# Reemplaza usuario/repo con tus valores
git remote add origin https://github.com/usuario/museo-dinosaurios.git
git branch -M main
git push -u origin main
```

### Tercero: Verificar en GitHub

1. Ir a https://github.com/usuario/museo-dinosaurios
2. Verificar que el código esté pusheado
3. Ir a "Actions" para ver el pipeline

---

## 🚀 Despliegue Automático

### Opciones de Deploy

#### A. Docker Hub (Automático)

La imagen se pushea automáticamente a Docker Hub en cada push a main.

```bash
# Alguien puede descargar y correr tu imagen
docker pull usuario/museo-dinosaurios:latest
docker run -p 8000:8000 usuario/museo-dinosaurios:latest
```

#### B. Heroku (Manual)

```bash
# Instalar Heroku CLI
npm install -g heroku

# Login y crear app
heroku login
heroku create tu-app-nombre

# Deploy
git push heroku main
```

#### C. AWS/Google Cloud (Avanzado)

Requiere configuración adicional de secrets y roles IAM.

---

## 📊 Monitoreo

### Ver ejecución del Pipeline

1. GitHub → Tu repositorio → Actions
2. Seleccionar el workflow "FastAPI CI/CD Pipeline"
3. Ver logs detallados de cada job

### Métricas importantes

- ✅ Tests passed/failed
- 📦 Docker image size
- ⏱️ Tiempo de ejecución
- 🔐 Vulnerabilidades detectadas

---

## 🐛 Troubleshooting

### El workflow no se ejecuta

**Causa**: Archivo YAML con sintaxis incorrecta

**Solución**:
```bash
# Validar YAML en línea
# https://www.yamllint.com/
```

### Docker build falla

**Causa**: Archivo Dockerfile incorrecto

**Solución**:
```bash
# Probar localmente
docker build -t test:latest .
```

### Login a Docker Hub falla

**Causa**: Secrets no configurados o token expirado

**Solución**:
1. Verificar secrets en GitHub Settings
2. Regenerar token en Docker Hub
3. Actualizar secrets en GitHub

---

## 📚 Referencias

- [GitHub Actions Documentation](https://docs.github.com/es/actions)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/concepts/)
- [Best Practices Docker](https://docs.docker.com/develop/dev-best-practices/)

---

## ✅ Checklist DevOps

- [x] Dockerfile multi-stage creado
- [x] docker-compose.yml configurado
- [x] .gitignore y .dockerignore creados
- [x] GitHub Actions workflow creado
- [x] Documentación DevOps completada
- [ ] Secrets configurados en GitHub
- [ ] Primer push a GitHub realizado
- [ ] Verificar ejecución del workflow

---

*Última actualización: Febrero 2026*
