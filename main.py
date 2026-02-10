from typing import Annotated
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional
from data.database import database
from data.dinosaurio_repository import DinosaurioRepository
from domain.model.Dinosaurio import Dinosaurio
from utils.dependencies import require_auth, require_auth_admin
from routers import auth_router, dinosaurios_router, eras_router, regiones_router, habitats_router, usuarios_router, comentarios_router
import uvicorn

# Crear la aplicación FastAPI
app = FastAPI(
    title="🦖 Museo de Dinosaurios - AUTO-UPDATE FUNCIONANDO ✅", 
    description="Sistema de gestión de dinosaurios con CI/CD completo",
    version="2.0.0"
)

# ⭐ IMPORTANTE: Agregar el middleware de sesiones
app.add_middleware(
    SessionMiddleware,
    secret_key="tu_clave_secreta_muy_segura_cambiala_en_produccion",
    session_cookie="session",
    max_age=3600 * 24 * 7,  # 7 días
    same_site="lax",
    https_only=False  # Cambiar a True en producción con HTTPS
)

# Configurar las plantillas
templates = Jinja2Templates(directory="template")

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Incluir los routers
app.include_router(auth_router.router)
app.include_router(dinosaurios_router.router)
app.include_router(eras_router.router)
app.include_router(regiones_router.router)
app.include_router(habitats_router.router)
app.include_router(usuarios_router.router)
app.include_router(comentarios_router.router)

#RUTA RAIZ
@app.get("/")
async def inicio(request: Request, usuario: dict = Depends(require_auth)):
    """Página de inicio - Requiere autenticación"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "usuario": usuario
    })

# RUTA INSERTAR
@app.get("/insert_dinosaurios")
async def insert_dinosaurios(request: Request, usuario: dict = Depends(require_auth_admin)):
    """Formulario para insertar dinosaurio - Solo admin"""
    if usuario.get("username") != "admin":
        return templates.TemplateResponse("403.html", {
            "request": request,
            "usuario": usuario
        })
    
    return templates.TemplateResponse("insert_dinosaurios.html", {
        "request": request,
        "usuario": usuario
    })

# RUTA INSERTAR
@app.post("/do_insertar_dinosaurio")
async def do_insertar_dinosaurios(
    request: Request,
    nombre: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_auth)
):
    """Inserta un dinosaurio - Requiere autenticación admin"""
    if usuario.get("username") != "admin":
        return templates.TemplateResponse("403.html", {
            "request": request,
            "usuario": usuario
        })
    
    dinosaurios_repo = DinosaurioRepository()
    dinosaurio = Dinosaurio(0, nombre)
    dinosaurios_repo.insertar_dinosaurio(database, dinosaurio)

    return templates.TemplateResponse("do_insert_dinosaurios.html", {
        "request": request,
        "usuario": usuario
    })


# RUTA ACTUALIZAR
@app.get("/actualizar")
async def actualizar_dinosaurios(request: Request, usuario: dict = Depends(require_auth)):
    """Mostrar formulario para actualizar un dinosaurio - Solo admin"""
    if usuario.get("username") != "admin":
        return templates.TemplateResponse("403.html", {
            "request": request,
            "usuario": usuario
        })
    
    dinosaurios_repo = DinosaurioRepository()
    dinosaurios = dinosaurios_repo.get_all(database)

    return templates.TemplateResponse("actualizar_dinosaurios.html", {
        "request": request,
        "dinosaurios": dinosaurios,
        "usuario": usuario
    })


@app.post("/do_actualizar_dinosaurio")
async def do_actualizar_dinosaurio(
    request: Request,
    id: Annotated[str, Form()],
    nombre: Annotated[str, Form()] = None,
    usuario: dict = Depends(require_auth)
):
    """Procesar actualización - Solo admin"""
    if usuario.get("username") != "admin":
        return templates.TemplateResponse("403.html", {
            "request": request,
            "usuario": usuario
        })
    
    dinosaurios_repo = DinosaurioRepository()
    dinosaurio = Dinosaurio(int(id), nombre)
    dinosaurios_repo.actualizar_dinosaurio(database, dinosaurio)

    return templates.TemplateResponse("do_actualizar_dinosaurio.html", {
        "request": request,
        "usuario": usuario
    })


# RUTA Borrar
@app.get("/borrar")
async def borrar_dinosaurios(request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para borrar dinosaurios - Solo admin"""
    if usuario.get("username") != "admin":
        return templates.TemplateResponse("403.html", {
            "request": request,
            "usuario": usuario
        })
    
    dinosaurios_repo = DinosaurioRepository()
    dinosaurios = dinosaurios_repo.get_all(database)

    return templates.TemplateResponse("borrar_dinosaurios.html", {
        "request": request,
        "dinosaurios": dinosaurios,
        "usuario": usuario
    })


# RUTA BORRAR
@app.post("/do_borrar_dinosaurio")
async def do_borrar_dinosaurio(
    request: Request,
    id: Annotated[str, Form()],
    usuario: dict = Depends(require_auth)
):
    """Borra un dinosaurio - Solo admin"""
    if usuario.get("username") != "admin":
        return templates.TemplateResponse("403.html", {
            "request": request,
            "usuario": usuario
        })
    
    dinosaurios_repo = DinosaurioRepository()
    dinosaurios_repo.borrar_dinosaurio(database, int(id))

    return templates.TemplateResponse("do_borrar_dinosaurios.html", {
        "request": request,
        "usuario": usuario
    })


# RUTAS GET - Nota: Las rutas de dinosaurios, eras, regiones y habitats
# están implementadas en sus respectivos routers (dinosaurios_router.py, etc.)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
