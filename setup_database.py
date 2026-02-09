"""
Script para crear la tabla de usuarios directamente en la BD thomas
"""
import mysql.connector

def crear_tabla_usuarios():
    """Crea la tabla de usuarios en la BD thomas"""
    
    # Conectar directamente a la BD thomas
    try:
        db = mysql.connector.connect(
            host='informatica.iesquevedo.es',
            port=3333,
            user='root',
            password='1asir',
            database='thomas',
            ssl_disabled=True
        )
        
        cursor = db.cursor()
        
        # Crear la tabla
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
        
        cursor.execute(sql)
        
        # Crear índice
        try:
            cursor.execute("CREATE INDEX idx_username ON usuarios(username)")
        except:
            pass  # El índice ya puede existir
        
        db.commit()
        cursor.close()
        db.close()
        
        print("✓ Tabla 'usuarios' creada exitosamente en la BD thomas")
        return True
        
    except Exception as e:
        print(f"✗ Error al crear la tabla: {str(e)}")
        return False


if __name__ == "__main__":
    print("🦖 Creando tabla de usuarios en la BD thomas...")
    crear_tabla_usuarios()
