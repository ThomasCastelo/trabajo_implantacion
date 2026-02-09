# 📤 Guía: Subir Proyecto a GitHub

Esta guía te ayudará a subir tu proyecto "Museo de Dinosaurios FastAPI" a GitHub.

## Requisitos Previos

### 1. Tener una cuenta GitHub
- Si no tienes, crea una en [github.com](https://github.com)
- Verifica tu email

### 2. Tener GitHub CLI o Git instalado
```bash
# Windows (con Chocolatey)
choco install git

# O descargar desde https://git-scm.com/download/win
```

### 3. Crear un repositorio en GitHub
1. Ve a [github.com/new](https://github.com/new)
2. Nombre del repo: `museo-dinosaurios` (o tu preferencia)
3. Descripción: "FastAPI Museo de Dinosaurios con CI/CD"
4. Selecciona **Public** o **Private**
5. NO inicialices con README (lo haremos nosotros)
6. Click "Create repository"

---

## Paso a Paso: Subir el Código

### Paso 1: Configurar Git localmente

```bash
cd c:\implantacion\fastapi_plantillascomunes

# Configurar nombre y email (necesario)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Verificar configuración
git config --list
```

### Paso 2: Inicializar repositorio local

```bash
# Inicializar git en el proyecto
git init

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit: Museo de Dinosaurios FastAPI con CI/CD"
```

**Nota**: Si ves errores sobre `.git` ya existente, es que ahí ya hay un repo:
```bash
# Eliminar git anterior si es necesario
rm -r .git
git init
```

### Paso 3: Conectar con GitHub

**⚠️ REEMPLAZA TUS VALORES**

```bash
# Usar HTTPS (recomendado para principiantes)
git remote add origin https://github.com/TU_USUARIO/museo-dinosaurios.git

# Verificar que se agregó
git remote -v
# Debe mostrar:
# origin  https://github.com/TU_USUARIO/museo-dinosaurios.git (fetch)
# origin  https://github.com/TU_USUARIO/museo-dinosaurios.git (push)
```

### Paso 4: Cambiar rama a 'main'

```bash
# Renombrar rama master a main (mejor práctica)
git branch -M main

# Verificar
git branch
# Debe mostrar:
# * main
```

### Paso 5: Push al repositorio remoto

```bash
# Subir código a GitHub (primera vez)
git push -u origin main

# Ingresar credenciales:
# - Username: tu_usuario_github
# - Password: tu_token_de_acceso (o contraseña, ver más abajo)
```

**Si GitHub pide token en lugar de contraseña**:

1. Ve a [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Nombre: `git-token`
4. Selecciona scopes: `repo`, `workflow`
5. Click "Generate token"
6. Copia el token y usalo como contraseña

---

## Opción 2: Usando GitHub CLI (Más fácil)

Si prefieres usar la línea de comandos de GitHub:

```bash
# Instalar GitHub CLI (Windows)
choco install gh

# Login
gh auth login
# Selecciona: GitHub.com → HTTPS → Y (autenticar) → Y (login)

# Crear repositorio directamente
gh repo create museo-dinosaurios --public --source=. --remote=origin --push

# Listo! Ya está en GitHub
```

---

## Verificar que el código está en GitHub

1. Abre [github.com/TU_USUARIO/museo-dinosaurios](https://github.com/TU_USUARIO/museo-dinosaurios)
2. Verifica que ves tus archivos
3. Comprueba que existe `.github/workflows/docker-ci-cd.yml`

---

## Configurar Secrets para CI/CD

Para que el pipeline funcione, necesitas configurar los secretos:

### 1. Obtener Docker Hub Token

```bash
# Login en Docker Hub
docker login

# O ir a https://hub.docker.com/settings/security
# New Access Token
# Nombre: github-token
# Copiar el token
```

### 2. Agregar Secrets en GitHub

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Agregar:
   ```
   DOCKERHUB_USERNAME = tu_usuario_dockerhub
   DOCKERHUB_TOKEN = (el token que copiaste)
   ```

---

## Ver el Pipeline en Acción

Una vez que hayas pusheado:

1. Ve a tu repositorio
2. Click en la pestaña "Actions"
3. Verás el workflow "FastAPI CI/CD Pipeline"
4. Click para ver logs detallados

**Primer run**: Tomará unos 5-10 minutos

---

## Após Cambios Futuros

Cada vez que hagas cambios:

```bash
# Ver cambios
git status

# Agregar cambios
git add .

# Commit
git commit -m "Descripción del cambio"

# Push
git push origin main
```

---

## Troubleshooting

### Error: "fatal: not a git repository"
```bash
# Solución: Estás en carpeta equivocada
cd c:\implantacion\fastapi_plantillascomunes
git init
```

### Error: "fatal: Could not read from remote repository"
```bash
# Solución: Verificar que el remote está correcto
git remote -v

# Si está mal, corregir:
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/museo-dinosaurios.git
```

### Error: "Authentication failed"
```bash
# Solución: Usar token en lugar de contraseña
# Generar token en GitHub Settings
# Usar el token como contraseña en el prompt
```

### El workflow no se ejecuta
```
Espera 1-2 minutos después del push
Verifica que .github/workflows/docker-ci-cd.yml existe en main
Revisa la pestaña "Actions" para error details
```

---

## Próximos Pasos

✅ **Completados:**
- [ ] Código pusheado a GitHub
- [ ] Secrets configurados
- [ ] Workflow ejecutado exitosamente
- [ ] Imagen en Docker Hub

📚 **Documentación**: Revisar `DEVOPS.md` para más detalles

---

## Referencias

- [GitHub Docs](https://docs.github.com/)
- [GitHub CLI](https://cli.github.com/)
- [GitHub Actions](https://github.com/features/actions)
- [Docker Hub](https://hub.docker.com/)

---

*Última actualización: Febrero 2026*
