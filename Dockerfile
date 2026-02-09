# ============================================
# DOCKERFILE - CONSTRUCCIÓN DE IMAGEN DOCKER
# ============================================
# Este Dockerfile usa una estrategia multi-stage (2 etapas):
# 1. Builder: Compila e instala dependencias (stage pesado)
# 2. Runtime: Imagen final optimizada (solo lo necesario)
# Ventaja: Imagen final más pequeña y segura

# ============================================
# STAGE 1: BUILDER - Construir dependencias
# ============================================
# Imagen base: Python 3.11 slim (versión ligera)
FROM python:3.11-slim AS builder

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar herramientas de compilación necesarias para algunas librerías Python
# gcc: Compilador C necesario para algunos paquetes que usan extensiones en C
# --no-install-recommends: No instalar paquetes recomendados (reduce tamaño)
# rm -rf /var/lib/apt/lists/*: Limpiar caché de apt para reducir tamaño
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements.txt primero (aprovecha caché de Docker)
# Si requirements.txt no cambia, Docker reutiliza esta capa en futuros builds
COPY requirements.txt .

# Instalar dependencias Python en /root/.local (instalación de usuario)
# --no-cache-dir: No guardar caché de pip (reduce tamaño)
# --user: Instalar en directorio de usuario, no global
# --no-compile: No compilar .pyc (se harán en runtime si es necesario)
# Las líneas find: Eliminar archivos de caché Python para reducir tamaño
RUN pip install --no-cache-dir --user --no-compile -r requirements.txt \
    && find /root/.local -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true \
    && find /root/.local -type f -name '*.pyc' -delete \
    && find /root/.local -type f -name '*.pyo' -delete

# ============================================
# STAGE 2: RUNTIME - Imagen final optimizada
# ============================================
# Nueva imagen base limpia (NO hereda archivos del builder)
FROM python:3.11-slim

# Metadatos de la imagen (información visible con docker inspect)
LABEL maintainer="tu-email@example.com" \
      version="1.0" \
      description="FastAPI Museo Dinosaurios"

# Variables de entorno para optimizar Python en producción
ENV PYTHONUNBUFFERED=1 \              # No hacer buffer de stdout/stderr (logs en tiempo real)
    PYTHONDONTWRITEBYTECODE=1 \        # No crear archivos .pyc (reduce escritura en disco)
    PYTHONHASHSEED=random \            # Hash aleatorio para seguridad
    PIP_NO_CACHE_DIR=1 \               # Deshabilitar caché de pip
    PIP_DISABLE_PIP_VERSION_CHECK=1    # No verificar versión de pip (más rápido)

# Crear usuario no-root llamado 'fastapi' con UID 1000
# Ejecutar como no-root es una buena práctica de seguridad
# mkdir -p /app: Crear directorio de la aplicación
# chown: Dar permisos al usuario fastapi sobre /app
RUN useradd -m -u 1000 fastapi && \
    mkdir -p /app && \
    chown -R fastapi:fastapi /app

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde el stage builder
# /root/.local (del builder) → /home/fastapi/.local (runtime)
COPY --from=builder /root/.local /home/fastapi/.local

# Copiar TODO el código fuente al contenedor
# El . al final significa: copiar al directorio actual (/app)
COPY . .

# Cambiar permisos de todos los archivos al usuario fastapi
RUN chown -R fastapi:fastapi /app

# Agregar el directorio de binarios Python al PATH
# Permite ejecutar uvicorn sin ruta completa
ENV PATH=/home/fastapi/.local/bin:$PATH

# Cambiar al usuario no-root (a partir de aquí, todo corre como 'fastapi')
USER fastapi

# Exponer puerto 8000 (documentación, no abre realmente el puerto)
EXPOSE 8000

# Health check: Docker verificará cada 30s si la app responde
# --interval=30s: Revisar cada 30 segundos
# --timeout=10s: Timeout de 10 segundos
# --start-period=5s: Esperar 5 segundos antes del primer check
# --retries=3: 3 fallos consecutivos = contenedor unhealthy
# Comando: Hacer petición HTTP a localhost:8000 con Python
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').read()" || exit 1

# Comando por defecto al iniciar el contenedor
# Ejecuta uvicorn para servir la aplicación FastAPI
# main:app → archivo main.py, objeto app
# --host 0.0.0.0 → Escuchar en todas las interfaces (necesario para Docker)
# --port 8000 → Puerto donde escucha la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
