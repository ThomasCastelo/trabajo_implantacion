# 🎬 Edición de Comentarios y Sistema de Votos

## ✨ Nuevas Características

Se han implementado dos nuevas funcionalidades principales:

### 1️⃣ Edición de Comentarios
- Los usuarios pueden **editar sus propios comentarios** después de crearlos
- Aparece un badge `(editado)` cuando un comentario ha sido modificado
- Solo el autor del comentario o un admin pueden editar
- Interfaz intuitiva con botón "✎ Editar" que muestra un formulario inline

### 2️⃣ Sistema de Votos (Likes/Dislikes)
- Los usuarios pueden votar comentarios con 👍 (positivo) o 👎 (negativo)
- El voto se puede cambiar en cualquier momento (togglear entre votos o eliminar)
- Se muestra el conteo de votos positivos y negativos
- El voto del usuario actual se resalta en color (verde para positivo, rojo para negativo)
- Funciona para comentarios principales y respuestas

## 📊 Cambios en la Base de Datos

### Nueva Tabla: `comentario_votos`
```sql
CREATE TABLE comentario_votos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comentario_id INT NOT NULL,
    usuario_id INT NOT NULL,
    tipo_voto ENUM('positivo', 'negativo'),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comentario_id) REFERENCES comentarios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY unique_voto (comentario_id, usuario_id)
);
```

### Columna Nueva: `comentarios.fecha_modificacion`
- Registra cuándo se editó un comentario
- Se actualiza automáticamente con `NOW()` al hacer una edición

## 🔄 Cambios en el Backend

### Modelo: `domain/model/Comentario.py`
Nuevos atributos:
- `fecha_modificacion: str` - Fecha de última edición
- `votos_positivos: int` - Conteo de votos positivos
- `votos_negativos: int` - Conteo de votos negativos
- `voto_usuario: str` - Tipo de voto del usuario actual ('positivo', 'negativo', None)

### Repositorio: `data/comentario_repository.py`
Nuevos métodos:
- `actualizar_comentario(db, id, contenido)` - Actualiza el contenido de un comentario
- `get_votos(db, comentario_id, usuario_id)` - Obtiene conteos y voto del usuario
- `agregar_voto(db, comentario_id, usuario_id, tipo_voto)` - Agregar/actualizar voto
- `eliminar_voto(db, comentario_id, usuario_id)` - Eliminar voto

Métodos actualizados:
- `get_by_dinosaurio()` ahora acepta `usuario_id` opcional para cargar los votos del usuario
- `get_respuestas()` ahora acepta `usuario_id` opcional para cargar los votos del usuario

### Router: `routers/comentarios_router.py`
Nuevas rutas:
- `POST /comentarios/{id}/actualizar` - Editar comentario
- `POST /comentarios/{id}/votar` - Agregar/cambiar voto
- `POST /comentarios/{id}/quitar-voto` - Eliminar voto (opcional, mediante cambio de voto)

## 🎨 Cambios en el Frontend

### Template: `template/ver_dinosaurio.html`
Nuevas características visuales:
- **Botón Editar**: Abre formulario inline para editar comentario
- **Botones de Votos**: 👍 y 👎 con conteos en tiempo real
- **Badge de Edición**: Muestra "(editado)" si el comentario ha sido modificado
- **Formulario de Edición**: Aparece/desaparece cuando se hace click en "Editar"
- **Estilos Mejorados**: 
  - Botones de votos resaltados cuando el usuario ha votado
  - Fondo gris para formulario de edición para diferenciar
  - Espaciado mejorado entre acciones

Nueva función JavaScript:
- `toggleEditForm(comentarioId)` - Alterna visibilidad del formulario de edición

## ⚙️ Instalación / Migración

### Paso 1: Ejecutar la migración de base de datos
```bash
python migrate_edit_and_votes.py
```

Esto ejecutará el script SQL que:
- Añade la columna `fecha_modificacion` a la tabla `comentarios`
- Crea la tabla `comentario_votos` con las relaciones necesarias

### Paso 2: Reiniciar la aplicación
```bash
python main.py
```

## 🧪 Pruebas

1. **Editar comentario**:
   - Crear un comentario como usuario
   - Hacer click en "✎ Editar"
   - Modificar el texto
   - Hacer click en "Guardar Cambios"
   - Verificar que aparece "(editado)" al lado de la fecha

2. **Votar comentario**:
   - Hacer click en 👍 o 👎
   - El botón debe cambiar de color
   - El conteo debe aumentar
   - Hacer click nuevamente para cambiar el voto
   - Hacer click en el mismo botón para eliminar el voto

3. **Permisos**:
   - Solo el autor puede editar su comentario
   - Los admins pueden editar/borrar cualquier comentario
   - Cualquier usuario autenticado puede votar

## 🔒 Seguridad

- Backend valida que solo el autor (o admin) pueda editar
- Backend valida que solo el autor (o admin) pueda borrar
- Votos validados contra usuario autenticado
- Tabla de votos con UNIQUE constraint para evitar múltiples votos del mismo usuario

## 📝 Notas

- Los votos no aparecen en base de datos como ediciones (son separados)
- Cada usuario solo puede tener UN voto por comentario (cambiable)
- Los votos se heredan a respuestas (respuestas tienen su propio sistema de votos)
- La columna `fecha_modificacion` solo se llena cuando hay una edición (es NULL inicialmente)
