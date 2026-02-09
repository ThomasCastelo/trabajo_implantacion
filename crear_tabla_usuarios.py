"""
Script para crear la tabla de usuarios en la base de datos
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.database import database

def crear_tabla_usuarios():
    """Crea la tabla de usuarios en la base de datos"""
    cursor = database.cursor()
    
    sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARBINARY(255) NOT NULL,
        email VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    
    try:
        cursor.execute(sql)
        database.commit()
        print("✓ Tabla 'usuarios' creada exitosamente")
    except Exception as e:
        print(f"✗ Error al crear la tabla: {str(e)}")
        return False
    finally:
        cursor.close()
    
    return True


if __name__ == "__main__":
    print("🦖 Creando tabla de usuarios...")
    crear_tabla_usuarios()
