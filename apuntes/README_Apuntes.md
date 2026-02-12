# 🦕 Sistema de Autenticación y Autorización para fastapi_plantillascomunes

## ✅ Implementación Completada

Se ha implementado un sistema completo de autenticación y autorización en la aplicación `fastapi_plantillascomunes` con las siguientes características:

### 🔐 Características Principales

#### 1. **Autenticación**
- **Login**: Los usuarios pueden iniciar sesión con su nombre de usuario y contraseña
- **Registro**: Los nuevos usuarios pueden registrarse en la plataforma
- **Logout**: Los usuarios pueden cerrar su sesión en cualquier momento
- **Contraseñas**: Las contraseñas se protegen con `bcrypt` para mayor seguridad

#### 2. **Control de Acceso**
- **Usuarios regulares**: Solo pueden **VER** los dinosaurios
- **Administradores**: Pueden **AÑADIR**, **ACTUALIZAR** y **BORRAR** dinosaurios
- **Protección 403**: Acceso prohibido para usuarios sin permisos

#### 3. **Sesiones**
- Gestión de sesiones con `SessionMiddleware` de Starlette
- Las sesiones expiran en 7 días
- Almacenamiento seguro de datos de usuario

### 📁 Estructura de Archivos Creados

```
fastapi_plantillascomunes/
├── data/
│   ├── usuario_repository.py      # Repositorio de usuarios
│   └── database.py                # Conexión a BD (existente)
├── domain/
│   └── model/
│       └── Usuario.py             # Modelo de usuario
├── routers/
│   ├── __init__.py
│   └── auth_router.py             # Router de autenticación
├── utils/
│   ├── __init__.py
│   ├── session.py                 # Gestión de sesiones
│   └── dependencies.py            # Dependencias de autorización
├── sql/
│   └── create_usuarios_table.sql   # Script SQL para crear tabla
├── template/
│   ├── base.html                  # Plantilla base actualizada
│   ├── index.html                 # Índice actualizado
│   ├── login.html                 # Formulario de login
│   ├── registro.html              # Formulario de registro
│   └── 403.html                   # Página de acceso prohibido
├── main.py                        # Aplicación actualizada
├── requirements.txt               # Dependencias actualizadas
├── crear_tabla_usuarios.py        # Script para crear la tabla BD
└── crear_usuario_admin.py         # Script para crear admin
```

### 🚀 Instalación y Configuración

#### 1. Instalar Dependencias

```bash
cd fastapi_plantillascomunes
pip install -r requirements.txt
```

Las nuevas dependencias agregadas son:
- `bcrypt==4.1.2` - Para hash de contraseñas
- `starlette==0.37.0` - Para middleware de sesiones

#### 2. Crear Tabla de Usuarios

```bash
python crear_tabla_usuarios.py
```

Esto creará la tabla `usuarios` en la base de datos con los campos:
- `id` (INT, primary key)
- `username` (VARCHAR, único)
- `password_hash` (VARBINARY)
- `email` (VARCHAR, opcional)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### 3. Crear Usuario Admin

```bash
python crear_usuario_admin.py
```

Esto crea el usuario administrador con credenciales iniciales:
- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Email**: `admin@dinosaurios.local`

⚠️ **IMPORTANTE**: Cambia la contraseña del admin después de la primera vez

#### 4. Iniciar la Aplicación

```bash
python main.py
```

La aplicación estará disponible en: `http://127.0.0.1:8000`

### 📋 Flujo de Uso

#### Como Usuario Nuevo

1. **Accede a** `http://127.0.0.1:8000`
2. **Serás redirigido a** `/auth/login`
3. **Haz clic en** "¿No tienes cuenta?" para ir al registro
4. **Completa el formulario** de registro:
   - Usuario (mínimo 3 caracteres)
   - Contraseña (mínimo 6 caracteres)
   - Confirmar contraseña
   - Email (opcional)
5. **Tras el registro**, serás autologeado y redirigido al inicio
6. **Verás** la opción "Ver Dinosaurios" donde podrás consultar la lista
7. **En el menú lateral** aparecerá tu nombre de usuario con la etiqueta "USUARIO"

#### Como Administrador

1. **Inicia sesión** con:
   - Usuario: `admin`
   - Contraseña: `admin123`
2. **Verás en el menú** una sección adicional "⚙️ Administración" con opciones:
   - Insertar Dinosaurio
   - Borrar Dinosaurios
   - Actualizar Dinosaurio
3. **Podrás gestionar** completamente los dinosaurios
4. **Tu nombre de usuario** tendrá la etiqueta "ADMIN" en rojo

### 🔒 Sistema de Seguridad

#### Protección de Rutas

Todas las rutas principales están protegidas:

```python
# Requiere autenticación
@app.get("/")
async def inicio(request: Request, usuario: dict = Depends(require_auth)):
    ...

# Requiere autenticación y permisos de admin
@app.get("/insert_dinosaurios")
async def insert_dinosaurios(request: Request, usuario: dict = Depends(require_auth_admin)):
    ...
```

#### Hash de Contraseñas

Las contraseñas se hashean con `bcrypt` usando:
- **Algoritmo**: bcrypt
- **Salting**: Automático
- **Verificación**: Comparación segura de hashes

#### Variables de Sesión

Se almacenan en `request.session`:
- `user_id`: ID del usuario
- `username`: Nombre de usuario
- `authenticated`: Indicador de autenticación

### 🌐 Rutas Disponibles

#### Autenticación
- `GET /auth/login` - Mostrar formulario de login
- `POST /auth/login` - Procesar login
- `GET /auth/registro` - Mostrar formulario de registro
- `POST /auth/registro` - Procesar registro
- `GET /auth/logout` - Cerrar sesión

#### Datos (requieren autenticación)
- `GET /` - Página de inicio
- `GET /dinosaurios` - Ver lista de dinosaurios (todos pueden)
- `GET /insert_dinosaurios` - Formulario de inserción (solo admin)
- `POST /do_insertar_dinosaurio` - Insertar dinosaurio (solo admin)
- `GET /actualizar` - Formulario de actualización (solo admin)
- `POST /do_actualizar_dinosaurio` - Actualizar dinosaurio (solo admin)
- `GET /borrar` - Formulario de borrado (solo admin)
- `POST /do_borrar_dinosaurio` - Borrar dinosaurio (solo admin)

### 🎨 Interfaz de Usuario

#### Elementos Nuevos

1. **Login/Registro**: Interfaz moderna con diseño responsive
2. **Menú Lateral Actualizado**:
   - Muestra usuario actual
   - Badge con rol (ADMIN/USUARIO)
   - Sección separada para funciones de admin
   - Botón de logout en rojo
3. **Página de Error 403**: Acceso prohibido con diseño consistente
4. **Índice Mejorado**: Muestra opciones según el rol del usuario

### 📝 Modificaciones en Archivos Existentes

#### `main.py`
- Agregado `SessionMiddleware`
- Incluido `auth_router`
- Agregadas dependencias `require_auth` y `require_auth_admin`
- Todas las rutas ahora requieren autenticación
- Verificación de permisos de admin en rutas de administración

#### `template/base.html`
- Agregada visualización de usuario actual
- Agregada sección de administración condicional
- Botón de logout
- Mejorado el diseño visual
- Badge de rol de usuario

#### `template/index.html`
- Personalizado con nombre del usuario
- Muestra opciones según el rol
- Indicación de funciones solo para admin

#### `requirements.txt`
- `bcrypt==4.1.2`
- `starlette==0.37.0`

### 🧪 Pruebas Recomendadas

1. **Registro de Usuario**
   - Crear usuario nuevo
   - Intentar registrarse con usuario existente (debe fallar)
   - Intentar contraseñas que no coinciden (debe fallar)

2. **Login**
   - Login con credenciales correctas
   - Login con contraseña incorrecta (debe fallar)
   - Login con usuario que no existe (debe fallar)

3. **Permisos**
   - Como usuario: acceder a `/insert_dinosaurios` (debe mostrar 403)
   - Como admin: acceder a todas las rutas de administración
   - Logout y verificar redirección a login

4. **Sesiones**
   - Verificar que la sesión persiste al navegar
   - Cerrar sesión y verificar redirección a login

### 🔧 Configuración Personalizable

En `main.py`, puedes cambiar:

```python
app.add_middleware(
    SessionMiddleware,
    secret_key="tu_clave_secreta_muy_segura_cambiala_en_produccion",  # Cambiar
    session_cookie="session",
    max_age=3600 * 24 * 7,  # 7 días - puedes ajustar
    same_site="lax",
    https_only=False  # Cambiar a True en producción con HTTPS
)
```

### 🚨 Notas de Seguridad Importantes

1. **Secreto de Sesión**: Cambia `secret_key` en producción
2. **HTTPS**: Activa `https_only=True` en producción
3. **Contraseña Admin**: Cambia `admin123` después de la primera vez
4. **Validación de Entrada**: Implementa validación adicional según necesites
5. **Logs**: Considera agregar logs de acceso para auditoría

### 📚 Tecnologías Utilizadas

- **FastAPI**: Framework web moderno
- **Starlette**: ASGI toolkit con soporte de sesiones
- **Jinja2**: Motor de plantillas
- **MySQL Connector**: Conexión a base de datos
- **bcrypt**: Hash seguro de contraseñas
- **Pydantic**: Validación de datos

---

**Implementación completada el 22 de enero de 2026** ✅
