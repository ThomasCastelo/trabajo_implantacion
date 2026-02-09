from typing import Annotated
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from data.usuario_repository import UsuarioRepository
from utils.dependencies import require_auth, require_auth_admin

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
templates = Jinja2Templates(directory="template")


@router.get("/", response_class=HTMLResponse)
async def listar_usuarios(request: Request, usuario: dict = Depends(require_auth_admin)):
    repo = UsuarioRepository()
    usuarios = repo.get_all(database)
    return templates.TemplateResponse("usuarios.html", {
        "request": request,
        "usuario": usuario,
        "usuarios": usuarios
    })


@router.get("/nuevo", response_class=HTMLResponse)
async def form_nuevo_usuario(request: Request, usuario: dict = Depends(require_auth_admin)):
    return templates.TemplateResponse("usuario_form.html", {
        "request": request,
        "usuario": usuario,
        "modo": "nuevo",
        "usuario_obj": None
    })


@router.post("/nuevo")
async def crear_usuario(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    email: Annotated[str, Form()] = None,
    rol: Annotated[str, Form()] = "usuario",
    activo: Annotated[str | None, Form()] = None,
    usuario: dict = Depends(require_auth_admin)
):
    repo = UsuarioRepository()
    try:
        activo_bool = True if activo == "on" else False
        repo.insertar_usuario(database, username, password, email, rol)
        # Actualizar estado activo si fuera necesario
        creado = repo.get_by_username(database, username)
        if creado and not activo_bool:
            repo.actualizar_estado(database, creado.id, False)
        return RedirectResponse(url="/usuarios", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("usuario_form.html", {
            "request": request,
            "usuario": usuario,
            "modo": "nuevo",
            "usuario_obj": None,
            "error": f"Error al crear usuario: {str(e)}"
        })


@router.get("/{user_id}/editar", response_class=HTMLResponse)
async def form_editar_usuario(user_id: int, request: Request, usuario: dict = Depends(require_auth_admin)):
    repo = UsuarioRepository()
    usuario_obj = repo.get_by_id(database, user_id)
    if not usuario_obj:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": "Usuario no encontrado"
        })
    return templates.TemplateResponse("usuario_form.html", {
        "request": request,
        "usuario": usuario,
        "modo": "editar",
        "usuario_obj": usuario_obj
    })


@router.post("/{user_id}/editar")
async def actualizar_usuario(
    user_id: int,
    request: Request,
    username: Annotated[str, Form()],
    email: Annotated[str, Form()] = None,
    rol: Annotated[str, Form()] = "usuario",
    activo: Annotated[str | None, Form()] = None,
    password: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_auth_admin)
):
    repo = UsuarioRepository()
    try:
        activo_bool = True if activo == "on" else False
        repo.actualizar_usuario(database, user_id, username, email, rol, activo_bool)
        if password:
            repo.actualizar_password(database, user_id, password)
        return RedirectResponse(url="/usuarios", status_code=303)
    except Exception as e:
        usuario_obj = repo.get_by_id(database, user_id)
        return templates.TemplateResponse("usuario_form.html", {
            "request": request,
            "usuario": usuario,
            "modo": "editar",
            "usuario_obj": usuario_obj,
            "error": f"Error al actualizar usuario: {str(e)}"
        })


@router.get("/{user_id}/borrar")
async def borrar_usuario(user_id: int, request: Request, usuario: dict = Depends(require_auth_admin)):
    repo = UsuarioRepository()
    try:
        repo.borrar_usuario(database, user_id)
        return RedirectResponse(url="/usuarios", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al borrar usuario: {str(e)}"
        })
