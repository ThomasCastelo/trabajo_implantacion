#!/usr/bin/env python3
"""
Script para ejecutar la migración de edición y votos en comentarios
Usa la configuración de conexión de database.py
"""
import mysql.connector
import os
import sys

def run_migration():
    """Ejecutar la migración SQL"""
    try:
        # Conectar a MySQL usando los datos de database.py
        connection = mysql.connector.connect(
            host='informatica.iesquevedo.es',
            port=3333,
            user='root',
            password='1asir',
            database='thomas',
            ssl_disabled=True
        )
        
        cursor = connection.cursor()
        
        # Leer el archivo SQL
        sql_file = os.path.join(os.path.dirname(__file__), 'sql', 'add_edit_and_votes.sql')
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Procesar el contenido SQL eliminando comentarios y dividiendo por ;
        sql_lines = []
        for line in sql_content.split('\n'):
            line = line.strip()
            # Eliminar comentarios de línea completa
            if line and not line.startswith('--'):
                sql_lines.append(line)
        
        full_sql = '\n'.join(sql_lines)
        
        # Ejecutar cada statement
        statements_ejecutados = 0
        for statement in full_sql.split(';'):
            statement = statement.strip()
            if statement:  # Ignorar líneas vacías
                print(f"Ejecutando: {statement[:70]}...")
                try:
                    cursor.execute(statement)
                    statements_ejecutados += 1
                except mysql.connector.Error as err:
                    if "already exists" in str(err) or "Duplicate column" in str(err):
                        print(f"⚠️  Ya existe: {statement[:60]}...")
                    else:
                        raise
        
        connection.commit()
        print(f"\n✅ Migración completada exitosamente ({statements_ejecutados} statements ejecutados)")
        print("Se han añadido:")
        print("  - Columna 'fecha_modificacion' a la tabla 'comentarios'")
        print("  - Tabla 'comentario_votos' para votos en comentarios")
        
    except mysql.connector.Error as err:
        print(f"❌ Error de base de datos: {err}")
        return False
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo SQL en: {sql_file}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Migración: Edición y Votos en Comentarios")
    print("=" * 60)
    success = run_migration()
    sys.exit(0 if success else 1)
