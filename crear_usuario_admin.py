"""
Script para crear el usuario admin inicial en la base de datos de dinosaurios
"""
import sys
import os

# Agregar la ruta del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.database import database
from data.usuario_repository import UsuarioRepository

def crear_usuario_admin():
    """Crea el usuario admin en la base de datos"""
    usuario_repo = UsuarioRepository()
    
    # Verificar si ya existe el usuario admin
    admin_existente = usuario_repo.get_by_username(database, "admin")
    if admin_existente:
        print("✓ El usuario 'admin' ya existe en la base de datos")
        return
    
    # Crear el usuario admin
    try:
        usuario_repo.insertar_usuario(database, "admin", "admin123", "admin@dinosaurios.local")
        print("✓ Usuario 'admin' creado exitosamente")
        print("  Usuario: admin")
        print("  Contraseña: admin123")
        print("  Email: admin@dinosaurios.local")
        print("\n⚠️  IMPORTANTE: Cambia la contraseña después de la primera vez")
    except Exception as e:
        print(f"✗ Error al crear el usuario admin: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    print("🦖 Creando usuario admin...")
    crear_usuario_admin()
