"""
Script para agregar columnas de imagen y tabla de comentarios
"""
from data.database import database

def run_migrations():
    cursor = database.cursor()
    
    try:
        print("Agregando columnas de imagen...")
        
        # Agregar columna imagen a dinosaurios
        try:
            cursor.execute("ALTER TABLE dinosaurios ADD COLUMN imagen VARCHAR(500) NULL")
            print("OK - Columna imagen agregada a dinosaurios")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("- Columna imagen ya existe en dinosaurios")
            else:
                raise
        
        # Agregar columna imagen a eras
        try:
            cursor.execute("ALTER TABLE eras ADD COLUMN imagen VARCHAR(500) NULL")
            print("OK - Columna imagen agregada a eras")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("- Columna imagen ya existe en eras")
            else:
                raise
        
        # Agregar columna imagen a regiones
        try:
            cursor.execute("ALTER TABLE regiones ADD COLUMN imagen VARCHAR(500) NULL")
            print("OK - Columna imagen agregada a regiones")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("- Columna imagen ya existe en regiones")
            else:
                raise
        
        # Agregar columna imagen a habitats
        try:
            cursor.execute("ALTER TABLE habitats ADD COLUMN imagen VARCHAR(500) NULL")
            print("OK - Columna imagen agregada a habitats")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("- Columna imagen ya existe en habitats")
            else:
                raise
        
        database.commit()
        
        print("\nCreando tabla de comentarios...")
        
        # Crear tabla de comentarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comentarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                dinosaurio_id INT NOT NULL,
                usuario_id INT NOT NULL,
                comentario_padre_id INT NULL,
                contenido TEXT NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dinosaurio_id) REFERENCES dinosaurios(id) ON DELETE CASCADE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (comentario_padre_id) REFERENCES comentarios(id) ON DELETE CASCADE,
                INDEX idx_dinosaurio (dinosaurio_id),
                INDEX idx_usuario (usuario_id),
                INDEX idx_padre (comentario_padre_id)
            )
        """)
        database.commit()
        print("OK - Tabla comentarios creada")
        
        print("\nOK - Migraciones completadas exitosamente!")
        
    except Exception as e:
        print(f"\nERROR - Error durante la migracion: {e}")
        database.rollback()
    finally:
        cursor.close()

if __name__ == "__main__":
    run_migrations()
