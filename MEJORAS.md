# 🦖 Museo de Dinosaurios - FastAPI Mejorado

Sistema completo de gestión de dinosaurios con autenticación, roles de usuario y relaciones N-M.

## ✨ Nuevas Características

### 1. **Base de Datos Enriquecida**
- ✅ Tabla `dinosaurios` con campos extendidos (tipo, peso, altura, longitud, dieta)
- ✅ Tabla `eras` - Períodos geológicos (Triásico, Jurásico, Cretácico)
- ✅ Tabla `regiones` - Ubicaciones geográficas
- ✅ Tabla `habitats` - Tipos de entornos
- ✅ Tabla `dinosaurios_habitats` - Relación N-M

### 2. **Sistema de Roles y Permisos**
- ✅ Campo `rol` en tabla `usuarios` (admin o usuario)
- ✅ Campo `activo` para activar/desactivar usuarios
- ✅ Permisos diferenciados por rol
- ✅ Rutas protegidas con `require_auth_admin`

### 3. **Nuevas Pantallas y Funcionalidades**
- ✅ **Dinosaurios**: Crear, leer, actualizar, borrar (CRUD)
- ✅ **Eras Geológicas**: Gestión completa
- ✅ **Regiones**: Gestión de ubicaciones
- ✅ **Hábitats**: Gestión de entornos
- ✅ Formularios completos y validados
- ✅ Interfaz mejorada con Bootstrap

### 4. **Modelos de Datos**
```
Dinosaurio
├── id
├── nombre
├── descripcion
├── tipo
├── peso_kg
├── altura_metros
├── longitud_metros
├── dieta
├── era_id (FK)
├── region_id (FK)
├── creador_id (FK)
└── habitats (N-M)

Era
├── id
├── nombre
├── periodo_inicio
├── periodo_fin
└── descripcion

Region
├── id
├── nombre
├── pais
├── continente
└── descripcion

Habitat
├── id
├── nombre
├── tipo_ambiente
└── descripcion

Dinosaurios_Habitats (N-M)
├── dinosaurio_id (FK)
└── habitat_id (FK)
```

## 📁 Estructura de Archivos

### Modelos (`domain/model/`)
- `Dinosaurio.py` - Mejorado con más campos
- `Usuario.py` - Nuevo campo `rol` y `activo`
- `Era.py` - ✨ Nuevo
- `Region.py` - ✨ Nuevo
- `Habitat.py` - ✨ Nuevo

### Repositorios (`data/`)
- `dinosaurio_repository.py` - Mejorado con relación N-M
- `usuario_repository.py` - Métodos para gestionar roles
- `era_repository.py` - ✨ Nuevo
- `region_repository.py` - ✨ Nuevo
- `habitat_repository.py` - ✨ Nuevo

### Routers (`routers/`)
- `auth_router.py` - Existente
- `dinosaurios_router.py` - ✨ Nuevo - CRUD completo
- `eras_router.py` - ✨ Nuevo
- `regiones_router.py` - ✨ Nuevo
- `habitats_router.py` - ✨ Nuevo

### Plantillas (`template/`)
- `base.html` - Actualizado con nuevo menú
- `dinosaurios.html` - Mejorado
- `ver_dinosaurio.html` - ✨ Nuevo
- `nuevo_dinosaurio.html` - ✨ Nuevo
- `editar_dinosaurio.html` - ✨ Nuevo
- `eras.html` - ✨ Nuevo
- `nueva_era.html` - ✨ Nuevo
- `editar_era.html` - ✨ Nuevo
- `regiones.html` - ✨ Nuevo
- `nueva_region.html` - ✨ Nuevo
- `editar_region.html` - ✨ Nuevo
- `habitats.html` - ✨ Nuevo
- `nuevo_habitat.html` - ✨ Nuevo
- `editar_habitat.html` - ✨ Nuevo

### SQL
- `sql/create_complete_database.sql` - ✨ Nuevo con todas las tablas

## 🚀 Instalación y Configuración

### 1. Ejecutar las migraciones
```bash
python run_migrations.py
```

Este script creará automáticamente:
- Todas las nuevas tablas
- Relaciones y claves foráneas
- Datos de prueba iniciales (Eras, Regiones, Hábitats)

### 2. Iniciar la aplicación
```bash
python main.py
```

O con uvicorn directamente:
```bash
uvicorn main:app --reload
```

### 3. Acceder a la aplicación
```
http://localhost:8000
```

## 👥 Usuarios de Prueba

Después de ejecutar `run_migrations.py`, se crean estos usuarios:

- **Admin**: username: `admin`, rol: `admin`
- **Usuario Normal**: username: `usuario`, rol: `usuario`

(La contraseña se configura durante la creación)

## 🔐 Sistema de Permisos

### Roles Disponibles
- **admin**: Acceso total a crear, editar y borrar dinosaurios, eras, regiones y hábitats
- **usuario**: Solo puede ver dinosaurios y sus detalles

### Rutas Protegidas
```python
@require_auth              # Solo usuarios autenticados
@require_auth_admin        # Solo administradores
```

## 📊 Relación N-M

La relación entre `dinosaurios` y `habitats` es de **muchos a muchos (N-M)**:
- Un dinosaurio puede vivir en múltiples hábitats
- Un hábitat puede haber sido hogar de múltiples dinosaurios
- Se gestiona a través de la tabla `dinosaurios_habitats`

### Métodos en DinosaurioRepository
```python
agregar_habitat(db, dinosaurio_id, habitat_id)
quitar_habitat(db, dinosaurio_id, habitat_id)
get_habitats(db, dinosaurio_id)
```

## 🎨 Interfaz

- **Bootstrap 5**: Framework CSS para responsive design
- **Emojis**: Iconos intuitivos en menús y títulos
- **Tarjetas**: Diseño moderno para listar dinosaurios
- **Formularios**: Validación en cliente

## 📝 Funcionalidades CRUD

### Dinosaurios
- ✅ **CREATE**: `/dinosaurios/nuevo/form` (GET) + `/dinosaurios/nuevo` (POST)
- ✅ **READ**: `/dinosaurios/` (lista) + `/dinosaurios/{id}` (detalle)
- ✅ **UPDATE**: `/dinosaurios/{id}/editar` (GET) + `/dinosaurios/{id}/editar` (POST)
- ✅ **DELETE**: `/dinosaurios/{id}/borrar`

### Eras
- ✅ **CREATE**: `/eras/nueva/form` (GET) + `/eras/nueva` (POST)
- ✅ **READ**: `/eras/`
- ✅ **UPDATE**: `/eras/{id}/editar` (GET) + `/eras/{id}/editar` (POST)
- ✅ **DELETE**: `/eras/{id}/borrar`

### Regiones
- ✅ **CREATE**: `/regiones/nueva/form` (GET) + `/regiones/nueva` (POST)
- ✅ **READ**: `/regiones/`
- ✅ **UPDATE**: `/regiones/{id}/editar` (GET) + `/regiones/{id}/editar` (POST)
- ✅ **DELETE**: `/regiones/{id}/borrar`

### Hábitats
- ✅ **CREATE**: `/habitats/nuevo/form` (GET) + `/habitats/nuevo` (POST)
- ✅ **READ**: `/habitats/`
- ✅ **UPDATE**: `/habitats/{id}/editar` (GET) + `/habitats/{id}/editar` (POST)
- ✅ **DELETE**: `/habitats/{id}/borrar`

## 🎯 Próximas Mejoras Posibles

- Búsqueda y filtrado de dinosaurios
- Estadísticas y reportes
- Importación/exportación de datos
- Galería de imágenes
- Sistema de comentarios
- API REST completa
- Testing automatizado

## 📝 Notas

- Todos los formularios son seguros contra inyección SQL (usando prepared statements)
- Las contraseñas se hashean con bcrypt
- Las sesiones se mantienen durante 7 días
- Las migraciones son idempotentes (se pueden ejecutar múltiples veces)

---

**Desarrollado con ❤️ y 🦖 FastAPI**
