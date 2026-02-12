from domain.model.Usuario import Usuario
import bcrypt


class UsuarioRepository:

    def get_by_username(self, db, username: str) -> Usuario:
        """Obtiene un usuario por su nombre de usuario"""
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password_hash, email, rol, activo FROM usuarios WHERE username = %s", (username,))
        usuario_db = cursor.fetchone()
        cursor.close()
        
        if usuario_db:
            return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], usuario_db[4], usuario_db[5])
        return None

    def get_by_id(self, db, user_id: int) -> Usuario:
        """Obtiene un usuario por su ID"""
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password_hash, email, rol, activo FROM usuarios WHERE id = %s", (user_id,))
        usuario_db = cursor.fetchone()
        cursor.close()
        
        if usuario_db:
            return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], usuario_db[4], usuario_db[5])
        return None

    def get_all(self, db) -> list[Usuario]:
        """Obtiene todos los usuarios"""
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password_hash, email, rol, activo FROM usuarios")
        usuarios_en_db = cursor.fetchall()
        usuarios: list[Usuario] = list()
        
        for usuario in usuarios_en_db:
            usuario_obj = Usuario(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4], usuario[5])
            usuarios.append(usuario_obj)
        cursor.close()
        
        return usuarios

    def insertar_usuario(self, db, username: str, password: str, email: str = None, rol: str = "usuario") -> None:
        """Inserta un nuevo usuario con contraseña hasheada"""
        cursor = db.cursor()
        
        # Hashear la contraseña con bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, email, rol) VALUES (%s, %s, %s, %s)",
            (username, password_hash, email, rol)
        )
        
        db.commit()
        cursor.close()

    def verificar_password(self, password: str, password_hash: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        return bcrypt.checkpw(password.encode('utf-8'), bytes(password_hash))

    def actualizar_password(self, db, user_id: int, nueva_password: str) -> None:
        """Actualiza la contraseña de un usuario"""
        cursor = db.cursor()
        
        # Hashear la nueva contraseña
        password_hash = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            "UPDATE usuarios SET password_hash = %s WHERE id = %s",
            (password_hash, user_id)
        )
        
        db.commit()
        cursor.close()

    def actualizar_rol(self, db, user_id: int, nuevo_rol: str) -> None:
        """Actualiza el rol de un usuario"""
        cursor = db.cursor()
        cursor.execute(
            "UPDATE usuarios SET rol = %s WHERE id = %s",
            (nuevo_rol, user_id)
        )
        db.commit()
        cursor.close()

    def actualizar_estado(self, db, user_id: int, activo: bool) -> None:
        """Activa o desactiva un usuario"""
        cursor = db.cursor()
        cursor.execute(
            "UPDATE usuarios SET activo = %s WHERE id = %s",
            (activo, user_id)
        )
        db.commit()
        cursor.close()

    def actualizar_usuario(self, db, user_id: int, username: str, email: str = None, rol: str = "usuario", activo: bool = True) -> None:
        """Actualiza datos básicos del usuario"""
        cursor = db.cursor()
        cursor.execute(
            "UPDATE usuarios SET username = %s, email = %s, rol = %s, activo = %s WHERE id = %s",
            (username, email, rol, activo, user_id)
        )
        db.commit()
        cursor.close()

    def borrar_usuario(self, db, user_id: int) -> None:
        """Elimina un usuario"""
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        db.commit()
        cursor.close()
