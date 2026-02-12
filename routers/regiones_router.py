from typing import Annotated, Optional
from fastapi import APIRouter, Request, Form, Depends, File, UploadFile, Query
import shutil
from pathlib import Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from data.region_repository import RegionRepository
from domain.model.Region import Region
from utils.dependencies import require_auth, require_auth_admin

router = APIRouter(prefix="/regiones", tags=["regiones"])
templates = Jinja2Templates(directory="template")

# =====================================================
# LISTAR REGIONES
# =====================================================
@router.get("/", response_class=HTMLResponse)
async def listar_regiones(request: Request, usuario: dict = Depends(require_auth),
                         busqueda: Optional[str] = Query(None), continente: Optional[str] = Query(None)):
    """Lista todas las regiones geográficas con filtros opcionales"""
    region_repo = RegionRepository()
    regiones = region_repo.get_all(database, busqueda=busqueda, continente=continente)
    
    return templates.TemplateResponse("regiones.html", {
        "request": request,
        "usuario": usuario,
        "regiones": regiones,
        "filtros": {"busqueda": busqueda or "", "continente": continente or ""}
    })

# =====================================================
# NUEVA REGIÓN (GET - FORMULARIO)
# =====================================================
@router.get("/nueva/form", response_class=HTMLResponse)
async def form_nueva_region(request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para agregar una nueva región"""
    return templates.TemplateResponse("nueva_region.html", {
        "request": request,
        "usuario": usuario
    })

# =====================================================
# NUEVA REGIÓN (POST)
# =====================================================
@router.post("/nueva")
async def crear_region(
    request: Request,
    nombre: Annotated[str, Form()],
    pais: Annotated[str, Form()],
    continente: Annotated[str, Form()],
    descripcion: Annotated[str, Form()] = None,
    imagen: Optional[UploadFile] = File(None),
    usuario: dict = Depends(require_auth)
):
    """Crea una nueva región geográfica"""
    try:
        imagen_path = None
        if imagen and imagen.filename:
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            file_extension = Path(imagen.filename).suffix
            file_name = f"region_{nombre.replace(' ', '_')}{file_extension}"
            file_path = upload_dir / file_name
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            imagen_path = f"/uploads/{file_name}"
        
        region_repo = RegionRepository()
        region = Region(0, nombre, pais, continente, descripcion, imagen_path)
        region_repo.insertar_region(database, region)
        return RedirectResponse(url="/regiones/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al crear región: {str(e)}"
        })

# =====================================================
# EDITAR REGIÓN (GET)
# =====================================================
@router.get("/{region_id}/editar", response_class=HTMLResponse)
async def form_editar_region(region_id: int, request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para editar una región"""
    region_repo = RegionRepository()
    region = region_repo.get_by_id(database, region_id)
    
    if not region:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": "Región no encontrada"
        })
    
    return templates.TemplateResponse("editar_region.html", {
        "request": request,
        "usuario": usuario,
        "region": region
    })

# =====================================================
# EDITAR REGIÓN (POST)
# =====================================================
@router.post("/{region_id}/editar")
async def actualizar_region(
    region_id: int,
    request: Request,
    nombre: Annotated[str, Form()],
    pais: Annotated[str, Form()],
    continente: Annotated[str, Form()],
    descripcion: Annotated[str, Form()] = None,
    imagen: Optional[UploadFile] = File(None),
    usuario: dict = Depends(require_auth)
):
    """Actualiza una región existente"""
    try:
        region_repo = RegionRepository()
        region_actual = region_repo.get_by_id(database, region_id)
        imagen_path = region_actual.imagen if region_actual else None
        
        if imagen and imagen.filename:
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            file_extension = Path(imagen.filename).suffix
            file_name = f"region_{nombre.replace(' ', '_')}{file_extension}"
            file_path = upload_dir / file_name
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            imagen_path = f"/uploads/{file_name}"
        
        region = Region(region_id, nombre, pais, continente, descripcion, imagen_path)
        region_repo.actualizar_region(database, region)
        return RedirectResponse(url="/regiones/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al actualizar región: {str(e)}"
        })

# =====================================================
# BORRAR REGIÓN
# =====================================================
@router.get("/{region_id}/borrar")
async def borrar_region(region_id: int, request: Request, usuario: dict = Depends(require_auth_admin)):
    """Borra una región"""
    try:
        region_repo = RegionRepository()
        region_repo.borrar_region(database, region_id)
        return RedirectResponse(url="/regiones/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al borrar región: {str(e)}"
        })
