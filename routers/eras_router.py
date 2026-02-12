from typing import Annotated, Optional
from fastapi import APIRouter, Request, Form, Depends, File, UploadFile, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
from data.database import database
from data.era_repository import EraRepository
from domain.model.Era import Era
from utils.dependencies import require_auth, require_auth_admin

router = APIRouter(prefix="/eras", tags=["eras"])
templates = Jinja2Templates(directory="template")

# =====================================================
# LISTAR ERAS
# =====================================================
@router.get("/", response_class=HTMLResponse)
async def listar_eras(request: Request, usuario: dict = Depends(require_auth),
                     busqueda: Optional[str] = Query(None)):
    """Lista todas las eras geológicas con búsqueda opcional"""
    era_repo = EraRepository()
    eras = era_repo.get_all(database, busqueda=busqueda)
    
    return templates.TemplateResponse("eras.html", {
        "request": request,
        "usuario": usuario,
        "eras": eras,
        "filtros": {"busqueda": busqueda or ""}
    })

# =====================================================
# NUEVA ERA (GET - FORMULARIO)
# =====================================================
@router.get("/nueva/form", response_class=HTMLResponse)
async def form_nueva_era(request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para agregar una nueva era"""
    return templates.TemplateResponse("nueva_era.html", {
        "request": request,
        "usuario": usuario
    })

# =====================================================
# NUEVA ERA (POST)
# =====================================================
@router.post("/nueva")
async def crear_era(
    request: Request,
    nombre: Annotated[str, Form()],
    periodo_inicio: Annotated[int, Form()],
    periodo_fin: Annotated[int, Form()],
    descripcion: Annotated[str, Form()] = None,
    imagen: Optional[UploadFile] = File(None),
    usuario: dict = Depends(require_auth)
):
    """Crea una nueva era geológica"""
    try:
        # Manejar imagen
        imagen_path = None
        if imagen and imagen.filename:
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            file_extension = Path(imagen.filename).suffix
            file_name = f"era_{nombre.replace(' ', '_')}{file_extension}"
            file_path = upload_dir / file_name
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            imagen_path = f"/uploads/{file_name}"
        
        era_repo = EraRepository()
        era = Era(0, nombre, periodo_inicio, periodo_fin, descripcion, imagen_path)
        era_repo.insertar_era(database, era)
        return RedirectResponse(url="/eras/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al crear era: {str(e)}"
        })

# =====================================================
# EDITAR ERA (GET)
# =====================================================
@router.get("/{era_id}/editar", response_class=HTMLResponse)
async def form_editar_era(era_id: int, request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para editar una era"""
    era_repo = EraRepository()
    era = era_repo.get_by_id(database, era_id)
    
    if not era:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": "Era no encontrada"
        })
    
    return templates.TemplateResponse("editar_era.html", {
        "request": request,
        "usuario": usuario,
        "era": era
    })

# =====================================================
# EDITAR ERA (POST)
# =====================================================
@router.post("/{era_id}/editar")
async def actualizar_era(
    era_id: int,
    request: Request,
    nombre: Annotated[str, Form()],
    periodo_inicio: Annotated[int, Form()],
    periodo_fin: Annotated[int, Form()],
    descripcion: Annotated[str, Form()] = None,
    imagen: Optional[UploadFile] = File(None),
    usuario: dict = Depends(require_auth)
):
    """Actualiza una era existente"""
    try:
        era_repo = EraRepository()
        era_actual = era_repo.get_by_id(database, era_id)
        imagen_path = era_actual.imagen if era_actual else None
        
        if imagen and imagen.filename:
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            file_extension = Path(imagen.filename).suffix
            file_name = f"era_{nombre.replace(' ', '_')}{file_extension}"
            file_path = upload_dir / file_name
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            imagen_path = f"/uploads/{file_name}"
        
        era = Era(era_id, nombre, periodo_inicio, periodo_fin, descripcion, imagen_path)
        era_repo.actualizar_era(database, era)
        return RedirectResponse(url="/eras/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al actualizar era: {str(e)}"
        })

# =====================================================
# BORRAR ERA
# =====================================================
@router.get("/{era_id}/borrar")
async def borrar_era(era_id: int, request: Request, usuario: dict = Depends(require_auth_admin)):
    """Borra una era"""
    try:
        era_repo = EraRepository()
        era_repo.borrar_era(database, era_id)
        return RedirectResponse(url="/eras/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al borrar era: {str(e)}"
        })
