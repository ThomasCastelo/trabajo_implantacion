from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from data.database import database
from data.comentario_repository import ComentarioRepository
from domain.model.Comentario import Comentario
from utils.dependencies import require_auth
from typing import Optional

router = APIRouter(prefix="/comentarios", tags=["comentarios"])
comentario_repo = ComentarioRepository()


@router.post("/crear")
async def crear_comentario(
    request: Request,
    dinosaurio_id: int = Form(...),
    contenido: str = Form(...),
    comentario_padre_id: Optional[int] = Form(None),
    usuario: dict = Depends(require_auth)
):
    """Crear un nuevo comentario o respuesta"""
    db = database
    
    comentario = Comentario(
        id=0,
        dinosaurio_id=dinosaurio_id,
        usuario_id=usuario.get("id"),
        contenido=contenido,
        comentario_padre_id=comentario_padre_id
    )
    
    comentario_repo.insertar_comentario(db, comentario)
    
    return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)


@router.post("/{id}/actualizar")
async def actualizar_comentario(
    request: Request,
    id: int,
    dinosaurio_id: int = Form(...),
    contenido: str = Form(...),
    usuario: dict = Depends(require_auth)
):
    """Actualizar un comentario (solo el autor o admin)"""
    db = database
    
    # Obtener el comentario para verificar el autor
    cursor = db.cursor()
    cursor.execute("SELECT usuario_id FROM comentarios WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    
    # Verificar si el comentario existe
    if not result:
        return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)
    
    usuario_id = result[0]
    es_autor = usuario_id == usuario.get("id")
    es_admin = usuario.get("rol") == "admin"
    
    # Solo el autor o un admin pueden actualizar el comentario
    if es_autor or es_admin:
        comentario_repo.actualizar_comentario(db, id, contenido)
    
    return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)


@router.post("/{id}/borrar")
async def borrar_comentario(
    request: Request,
    id: int,
    dinosaurio_id: int = Form(...),
    usuario: dict = Depends(require_auth)
):
    """Borrar un comentario (solo el autor o admin)"""
    db = database
    
    # Obtener el comentario para verificar el autor
    cursor = db.cursor()
    cursor.execute("SELECT usuario_id FROM comentarios WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    
    # Verificar si el comentario existe
    if not result:
        return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)
    
    usuario_id = result[0]
    es_autor = usuario_id == usuario.get("id")
    es_admin = usuario.get("rol") == "admin"
    
    # Solo el autor o un admin pueden borrar el comentario
    if es_autor or es_admin:
        comentario_repo.borrar_comentario(db, id)
    
    return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)


@router.post("/{id}/votar")
async def votar_comentario(
    request: Request,
    id: int,
    dinosaurio_id: int = Form(...),
    tipo_voto: str = Form(...),
    usuario: dict = Depends(require_auth)
):
    """Agregar o actualizar un voto en un comentario"""
    db = database
    usuario_id = usuario.get("id")
    
    # Validar tipo de voto
    if tipo_voto not in ['positivo', 'negativo']:
        return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)
    
    # Obtener el voto actual del usuario
    comentario_repo.agregar_voto(db, id, usuario_id, tipo_voto)
    
    return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)


@router.post("/{id}/quitar-voto")
async def quitar_voto(
    request: Request,
    id: int,
    dinosaurio_id: int = Form(...),
    usuario: dict = Depends(require_auth)
):
    """Elimina el voto de un usuario en un comentario"""
    db = database
    usuario_id = usuario.get("id")
    
    comentario_repo.eliminar_voto(db, id, usuario_id)
    
    return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)

