from fastapi import Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from utils.session import obtener_usuario_actual, obtener_sesion


def require_auth(request: Request) -> dict:
    """Dependencia que requiere autenticación"""
    usuario = obtener_usuario_actual(request)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/auth/login"},
            detail="Redirect to login"
        )
    return usuario


def require_auth_admin(request: Request) -> dict:
    """Dependencia que requiere autenticación y rol de admin"""
    usuario = obtener_usuario_actual(request)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/auth/login"},
            detail="Redirect to login"
        )
    
    # Verificar si es admin
    if usuario.get("rol") != "admin" and usuario.get("username") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No autorizado"
        )
    
    return usuario
