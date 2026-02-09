# 🔐 Guía Rápida: Configurar Secrets en GitHub

## Paso 1: Obtener Docker Hub Token

### 1.1 Ir a Docker Hub
- URL: https://hub.docker.com
- Inicia sesión (o crea cuenta si no tienes)

### 1.2 Generar Access Token
1. Click en tu **avatar** (esquina superior derecha)
2. **Account Settings** → **Security**
3. Click **"New Access Token"**
4. Configurar:
   ```
   Description: github-actions-token
   Access permissions: Read, Write, Delete
   ```
5. Click **"Generate"**
6. ⚠️ **COPIAR TOKEN** - Solo se muestra una vez

---

## Paso 2: Configurar Secrets en GitHub

### 2.1 Ir a tu repositorio en GitHub
```
https://github.com/TU_USUARIO/TU_REPOSITORIO
```

### 2.2 Navegar a Settings
1. Click en **"Settings"** (pestaña superior derecha)
2. En el menú lateral izquierdo → **"Secrets and variables"**
3. Click en **"Actions"**

### 2.3 Agregar Secret 1: DOCKERHUB_USERNAME
1. Click **"New repository secret"**
2. Llenar:
   ```
   Name: DOCKERHUB_USERNAME
   Secret: tu_usuario_dockerhub
   ```
   Ejemplo: Si tu Docker Hub es `juan123`, poner `juan123`
3. Click **"Add secret"**

### 2.4 Agregar Secret 2: DOCKERHUB_TOKEN
1. Click **"New repository secret"** otra vez
2. Llenar:
   ```
   Name: DOCKERHUB_TOKEN
   Secret: (pegar el token que copiaste de Docker Hub)
   ```
   Ejemplo: `dckr_pat_abc123xyz...`
3. Click **"Add secret"**

---

## Verificar Secrets Configurados

Deberías ver:
```
DOCKERHUB_USERNAME    Updated X seconds ago
DOCKERHUB_TOKEN       Updated X seconds ago
```

---

## ⚠️ Notas Importantes

1. **NO necesitas crear repositorio en Docker Hub**
   - GitHub Actions lo crea automáticamente en el primer push
   
2. **El token es como una contraseña**
   - Nunca lo compartas
   - Si lo pierdes, genera uno nuevo
   
3. **Nomenclatura del repositorio en Docker Hub**
   - Será: `tu_usuario_dockerhub/museo-dinosaurios`
   - Se crea automáticamente cuando el workflow corre

---

## Próximo Paso: Push a GitHub

Una vez configurados los secrets:

```bash
cd c:\implantacion\fastapi_plantillascomunes

# Si ya hiciste git init, add, commit:
git push -u origin main

# Si no, hacer:
git init
git add .
git commit -m "Initial commit con CI/CD"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

---

## Ver el Pipeline en Acción

1. Después del push, ir a GitHub
2. Tu repositorio → Pestaña **"Actions"**
3. Verás "FastAPI CI/CD Pipeline" ejecutándose
4. Esperar ~5-10 minutos
5. ✅ Si todo está bien → Imagen en Docker Hub

---

## Troubleshooting

### Error: "Invalid username or password"
- Verificar que DOCKERHUB_USERNAME sea exacto (case-sensitive)
- Regenerar token en Docker Hub y actualizar DOCKERHUB_TOKEN

### El workflow no se ejecuta
- Verificar que el archivo existe: `.github/workflows/docker-ci-cd.yml`
- Esperar 1-2 minutos después del push

### "Repository not found" en Docker Hub
- Es normal - se crea automáticamente
- Si es privado → hacerlo público en Docker Hub settings

---

*Última actualización: Febrero 2026*
