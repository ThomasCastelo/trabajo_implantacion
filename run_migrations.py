"""
Script para ejecutar las migraciones SQL en la base de datos
"""
import mysql.connector
from pathlib import Path

def ejecutar_migraciones():
    """Ejecuta el script SQL de crear_complete_database.sql"""
    
    try:
        # Conectar a la BD
        db = mysql.connector.connect(
            host='informatica.iesquevedo.es',
            port=3333,
            user='root',
            password='1asir',
            database='thomas',
            ssl_disabled=True
        )
        
        cursor = db.cursor()
        
        # Leer el archivo SQL
        sql_file = Path(__file__).parent / 'sql' / 'create_complete_database.sql'
        
        if not sql_file.exists():
            print(f"❌ El archivo SQL no existe: {sql_file}")
            return False
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Ejecutar cada statement SQL
        statements = sql_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    db.commit()
                    print(f"✓ Ejecutado: {statement[:60]}...")
                except Exception as e:
                    print(f"⚠️  Error en statement: {str(e)}")
                    db.rollback()
        
        cursor.close()
        db.close()
        
        print("\n✅ Migraciones ejecutadas correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error al ejecutar migraciones: {str(e)}")
        return False


if __name__ == "__main__":
    print("🦖 Iniciando migraciones de base de datos...")
    ejecutar_migraciones()
