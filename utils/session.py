from fastapi import Request
from typing import Optional

# Clave secreta para firmar las cookies de sesión (cámbiala en producción)
SECRET_KEY = "tu_clave_secreta_muy_segura_cambiala_en_produccion"


def crear_sesion(request: Request, user_id: int, username: str, rol: str):
    """Crea una sesión guardando los datos en request.session"""
    request.session["user_id"] = user_id
    request.session["id"] = user_id
    request.session["username"] = username
    request.session["rol"] = rol
    request.session["authenticated"] = True


def obtener_sesion(request: Request) -> Optional[dict]:
    """Obtiene los datos de la sesión"""
    if not request.session or not request.session.get("authenticated"):
        return None
    
    return {
        "user_id": request.session.get("user_id"),
        "id": request.session.get("id"),
        "username": request.session.get("username"),
        "rol": request.session.get("rol")
    }


def destruir_sesion(request: Request):
    """Destruye la sesión limpiando los datos"""
    request.session.clear()


def usuario_autenticado(request: Request) -> bool:
    """Verifica si hay un usuario autenticado"""
    sesion = obtener_sesion(request)
    return sesion is not None


def obtener_usuario_actual(request: Request) -> Optional[dict]:
    """Obtiene el usuario actual de la sesión y verifica que siga activo en BD"""
    sesion = obtener_sesion(request)
    if not sesion:
        return None
    
    # Verificar que el usuario siga activo en la BD
    try:
        from data.database import database
        from data.usuario_repository import UsuarioRepository
        
        usuario_repo = UsuarioRepository()
        usuario = usuario_repo.get_by_id(database, sesion["user_id"])
        
        # Si el usuario no está activo, destruir sesión
        if usuario and not usuario.activo:
            destruir_sesion(request)
            return None
        
        return sesion
    except:
        # Si hay error en BD, retornar la sesión (fallback)
        return sesion

