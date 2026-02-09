# 🦖 GUÍA RÁPIDA - Museo de Dinosaurios

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Verificar estructura
```bash
python verificar_estructura.py
```
Debe mostrar ✅ en todo.

### 2️⃣ Crear la base de datos
```bash
python run_migrations.py
```
Crea todas las tablas automáticamente.

### 3️⃣ (Opcional) Agregar dinosaurios de prueba
```bash
python seed_dinosaurios.py
```
Inserta 6 dinosaurios reales.

### 4️⃣ Iniciar servidor
```bash
python main.py
```
O si tienes uvicorn:
```bash
uvicorn main:app --reload
```

### 5️⃣ Acceder
```
http://localhost:8000
```

---

## 👤 Usuarios de Prueba

Si usas `seed_dinosaurios.py`, debes crear usuarios primero:

1. Accede a `/auth/register` 
2. Crea usuario: `admin` / `admin123` (admin)
3. Crea usuario: `usuario` / `usuario123` (usuario normal)

O modifica `seed_dinosaurios.py` con los IDs correctos.

---

## 🎯 Lo que Puedes Hacer

### Como Admin 🔴
- ✏️ Crear dinosaurios con todos los datos
- 🔗 Asignar hábitats (relación N-M)
- 📍 Crear eras y regiones
- 🌳 Crear hábitats
- 🗑️ Eliminar cualquier cosa

### Como Usuario 🟢
- 👁️ Ver dinosaurios
- 📚 Ver detalles completos
- 🔍 Explorar información

---

## 🌐 Rutas Principales

| Ruta | Método | Rol | Descripción |
|------|--------|-----|-------------|
| `/` | GET | Todos | Inicio |
| `/auth/login` | GET/POST | - | Login |
| `/auth/register` | GET/POST | - | Registro |
| `/dinosaurios/` | GET | Todos | Lista dinosaurios |
| `/dinosaurios/{id}` | GET | Todos | Detalle dinosaurio |
| `/dinosaurios/nuevo/form` | GET | Admin | Formulario nuevo |
| `/dinosaurios/nuevo` | POST | Admin | Crear dinosaurio |
| `/dinosaurios/{id}/editar` | GET/POST | Admin | Editar dinosaurio |
| `/dinosaurios/{id}/borrar` | GET | Admin | Borrar dinosaurio |
| `/eras/` | GET | Admin | Gestionar eras |
| `/regiones/` | GET | Admin | Gestionar regiones |
| `/habitats/` | GET | Admin | Gestionar hábitats |

---

## 📊 Relación N-M Explicada

### ¿Qué es?
Un dinosaurio puede vivir en múltiples hábitats.
Un hábitat puede haber alojado múltiples dinosaurios.

### ¿Cómo usarlo?
1. Crea hábitats primero (ej: Llanura Aluvial, Bosque)
2. Al crear un dinosaurio, selecciona sus hábitats
3. Puedes editar los hábitats después

### Base de datos
```sql
-- Tabla relacional
dinosaurio_id | habitat_id
      1       |     1
      1       |     3
      2       |     2
```

---

## 🛠️ Troubleshooting

### ❌ "Connection refused"
- Verifica la BD está corriendo
- Actualiza credenciales en `data/database.py`

### ❌ "Tabla no existe"
- Ejecuta: `python run_migrations.py`

### ❌ "No puedo crear dinosaurios"
- Verifica que tu usuario sea admin
- En terminal: `python -c "from data.usuario_repository import UsuarioRepository; ..."`

### ❌ "Formulario no envía"
- Verifica que las líneas del formulario usen `name=`
- Recarga la página (Ctrl+F5)

---

## 📝 Estructura Rápida

```
fastapi_plantillascomunes/
├── domain/
│   └── model/
│       ├── Dinosaurio.py     ← Modelo principal
│       ├── Usuario.py
│       ├── Era.py
│       ├── Region.py
│       └── Habitat.py
├── data/
│   ├── dinosaurio_repository.py  ← Operaciones BD
│   ├── usuario_repository.py
│   ├── era_repository.py
│   ├── region_repository.py
│   └── habitat_repository.py
├── routers/
│   ├── auth_router.py        ← Rutas de auth
│   ├── dinosaurios_router.py ← Rutas CRUD dinosaurios
│   ├── eras_router.py
│   ├── regiones_router.py
│   └── habitats_router.py
├── template/
│   ├── base.html             ← Plantilla base
│   ├── dinosaurios.html      ← Listado
│   ├── nuevo_dinosaurio.html ← Crear
│   └── ... (más plantillas)
├── sql/
│   └── create_complete_database.sql ← Migraciones
├── main.py                   ← Punto de entrada
├── run_migrations.py         ← Setup BD
└── seed_dinosaurios.py       ← Datos de prueba
```

---

## 🔐 Seguridad

✅ Contraseñas hasheadas con bcrypt
✅ SQL injection prevención (prepared statements)
✅ Sesiones de 7 días
✅ Control de acceso por rol

---

## 💡 Próximas Mejoras

1. 🔍 Búsqueda y filtros
2. 📊 Estadísticas (dinosaurio más pesado, etc)
3. 📸 Galería de imágenes
4. 💬 Sistema de comentarios
5. 📥 Importar/exportar CSV
6. 🧪 Tests automatizados
7. 🔌 API REST completa

---

## ❓ Preguntas Frecuentes

**¿Puedo cambiar de usuario a admin?**
Sí, directamente en la BD:
```sql
UPDATE usuarios SET rol='admin' WHERE username='mi_usuario';
```

**¿Cómo agrego más dinosaurios?**
1. Opción A: Interfaz web (como admin)
2. Opción B: Modifica `seed_dinosaurios.py` y ejecuta

**¿Puedo usar otra BD?**
Sí, modifica `data/database.py` con tu conexión.

**¿Se borra todo si ejecuto migrations de nuevo?**
No, son idempotentes. Puedes ejecutar sin miedo.

---

## 📞 Soporte

Si algo no funciona:
1. Revisa los logs en terminal
2. Verifica `verificar_estructura.py`
3. Asegúrate que BD está accesible
4. Revisa los comentarios en el código

---

**¡Disfruta explorando el Museo de Dinosaurios! 🦖**
