from typing import Annotated, Optional
from fastapi import APIRouter, Request, Form, Depends, File, UploadFile, Query
import shutil
from pathlib import Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from data.database import database
from data.habitat_repository import HabitatRepository
from domain.model.Habitat import Habitat
from utils.dependencies import require_auth, require_auth_admin

router = APIRouter(prefix="/habitats", tags=["habitats"])
templates = Jinja2Templates(directory="template")

# =====================================================
# LISTAR HÁBITATS
# =====================================================
@router.get("/", response_class=HTMLResponse)
async def listar_habitats(request: Request, usuario: dict = Depends(require_auth),
                         busqueda: Optional[str] = Query(None), tipo_ambiente: Optional[str] = Query(None)):
    """Lista todos los hábitats disponibles con filtros opcionales"""
    habitat_repo = HabitatRepository()
    habitats = habitat_repo.get_all(database, busqueda=busqueda, tipo_ambiente=tipo_ambiente)
    
    return templates.TemplateResponse("habitats.html", {
        "request": request,
        "usuario": usuario,
        "habitats": habitats,
        "filtros": {"busqueda": busqueda or "", "tipo_ambiente": tipo_ambiente or ""}
    })

# =====================================================
# NUEVO HÁBITAT (GET - FORMULARIO)
# =====================================================
@router.get("/nuevo/form", response_class=HTMLResponse)
async def form_nuevo_habitat(request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para agregar un nuevo hábitat"""
    return templates.TemplateResponse("nuevo_habitat.html", {
        "request": request,
        "usuario": usuario
    })

# =====================================================
# NUEVO HÁBITAT (POST)
# =====================================================
@router.post("/nuevo")
async def crear_habitat(
    request: Request,
    nombre: Annotated[str, Form()],
    tipo_ambiente: Annotated[str, Form()],
    descripcion: Annotated[str, Form()] = None,
    imagen: Optional[UploadFile] = File(None),
    usuario: dict = Depends(require_auth)
):
    """Crea un nuevo hábitat"""
    try:
        imagen_path = None
        if imagen and imagen.filename:
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            file_extension = Path(imagen.filename).suffix
            file_name = f"habitat_{nombre.replace(' ', '_')}{file_extension}"
            file_path = upload_dir / file_name
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            imagen_path = f"/uploads/{file_name}"
        
        habitat_repo = HabitatRepository()
        habitat = Habitat(0, nombre, tipo_ambiente, descripcion, imagen_path)
        habitat_repo.insertar_habitat(database, habitat)
        return RedirectResponse(url="/habitats/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al crear hábitat: {str(e)}"
        })

# =====================================================
# EDITAR HÁBITAT (GET)
# =====================================================
@router.get("/{habitat_id}/editar", response_class=HTMLResponse)
async def form_editar_habitat(habitat_id: int, request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para editar un hábitat"""
    habitat_repo = HabitatRepository()
    habitat = habitat_repo.get_by_id(database, habitat_id)
    
    if not habitat:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": "Hábitat no encontrado"
        })
    
    return templates.TemplateResponse("editar_habitat.html", {
        "request": request,
        "usuario": usuario,
        "habitat": habitat
    })

# =====================================================
# EDITAR HÁBITAT (POST)
# =====================================================
@router.post("/{habitat_id}/editar")
async def actualizar_habitat(
    habitat_id: int,
    request: Request,
    nombre: Annotated[str, Form()],
    tipo_ambiente: Annotated[str, Form()],
    descripcion: Annotated[str, Form()] = None,
    imagen: Optional[UploadFile] = File(None),
    usuario: dict = Depends(require_auth)
):
    """Actualiza un hábitat existente"""
    try:
        habitat_repo = HabitatRepository()
        habitat_actual = habitat_repo.get_by_id(database, habitat_id)
        imagen_path = habitat_actual.imagen if habitat_actual else None
        
        if imagen and imagen.filename:
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            file_extension = Path(imagen.filename).suffix
            file_name = f"habitat_{nombre.replace(' ', '_')}{file_extension}"
            file_path = upload_dir / file_name
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            imagen_path = f"/uploads/{file_name}"
        
        habitat = Habitat(habitat_id, nombre, tipo_ambiente, descripcion, imagen_path)
        habitat_repo.actualizar_habitat(database, habitat)
        return RedirectResponse(url="/habitats/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al actualizar hábitat: {str(e)}"
        })

# =====================================================
# BORRAR HÁBITAT
# =====================================================
@router.get("/{habitat_id}/borrar")
async def borrar_habitat(habitat_id: int, request: Request, usuario: dict = Depends(require_auth_admin)):
    """Borra un hábitat"""
    try:
        habitat_repo = HabitatRepository()
        habitat_repo.borrar_habitat(database, habitat_id)
        return RedirectResponse(url="/habitats/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al borrar hábitat: {str(e)}"
        })
