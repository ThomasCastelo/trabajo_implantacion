from typing import Annotated, Optional
from fastapi import APIRouter, Request, Form, Depends, File, UploadFile, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import shutil
import os
from pathlib import Path
from data.database import database
from data.dinosaurio_repository import DinosaurioRepository
from data.era_repository import EraRepository
from data.region_repository import RegionRepository
from data.habitat_repository import HabitatRepository
from domain.model.Dinosaurio import Dinosaurio
from domain.model.Era import Era
from domain.model.Region import Region
from domain.model.Habitat import Habitat
from utils.dependencies import require_auth, require_auth_admin

router = APIRouter(prefix="/dinosaurios", tags=["dinosaurios"])
templates = Jinja2Templates(directory="template")


def _parse_float(value: Optional[str]) -> Optional[float]:
    if value is None or value == "":
        return None
    return float(value)


def _parse_int(value: Optional[str]) -> Optional[int]:
    if value is None or value == "":
        return None
    return int(value)

# =====================================================
# LISTAR DINOSAURIOS
# =====================================================
@router.get("/", response_class=HTMLResponse)
async def listar_dinosaurios(
    request: Request, 
    usuario: dict = Depends(require_auth),
    busqueda: Optional[str] = Query(None),
    era_id: Optional[str] = Query(None),
    region_id: Optional[str] = Query(None),
    dieta: Optional[str] = Query(None)
):
    """Lista todos los dinosaurios con filtros opcionales"""
    dino_repo = DinosaurioRepository()
    era_repo = EraRepository()
    region_repo = RegionRepository()
    habitat_repo = HabitatRepository()
    
    # Convertir era_id y region_id de string a int si no están vacíos
    era_id_int = int(era_id) if era_id and era_id.strip() else None
    region_id_int = int(region_id) if region_id and region_id.strip() else None
    
    # Obtener dinosaurios con filtros
    dinosaurios = dino_repo.get_all(database, busqueda=busqueda, era_id=era_id_int, 
                                    region_id=region_id_int, dieta=dieta)
    
    # Enriquecer cada dinosaurio con sus relaciones
    for dino in dinosaurios:
        if dino.era_id:
            dino.era = era_repo.get_by_id(database, dino.era_id)
        if dino.region_id:
            dino.region = region_repo.get_by_id(database, dino.region_id)
        dino.habitats = habitat_repo.get_habitats_by_dinosaurio(database, dino.id)
    
    # Obtener todas las eras y regiones para los filtros
    todas_eras = era_repo.get_all(database, busqueda=None)
    todas_regiones = region_repo.get_all(database, busqueda=None)
    
    return templates.TemplateResponse("dinosaurios.html", {
        "request": request,
        "usuario": usuario,
        "dinosaurios": dinosaurios,
        "todas_eras": todas_eras,
        "todas_regiones": todas_regiones,
        "filtros": {
            "busqueda": busqueda or "",
            "era_id": era_id_int,
            "region_id": region_id_int,
            "dieta": dieta or ""
        }
    })

# =====================================================
# VER DETALLE DE UN DINOSAURIO
# =====================================================
@router.get("/{dinosaurio_id}", response_class=HTMLResponse)
async def ver_dinosaurio(dinosaurio_id: int, request: Request, usuario: dict = Depends(require_auth)):
    """Ve los detalles de un dinosaurio específico"""
    from data.comentario_repository import ComentarioRepository
    
    dino_repo = DinosaurioRepository()
    era_repo = EraRepository()
    region_repo = RegionRepository()
    habitat_repo = HabitatRepository()
    comentario_repo = ComentarioRepository()
    
    dinosaurio = dino_repo.get_by_id(database, dinosaurio_id)
    if not dinosaurio:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": "Dinosaurio no encontrado"
        })
    
    # Enriquecer con relaciones
    if dinosaurio.era_id:
        dinosaurio.era = era_repo.get_by_id(database, dinosaurio.era_id)
    if dinosaurio.region_id:
        dinosaurio.region = region_repo.get_by_id(database, dinosaurio.region_id)
    dinosaurio.habitats = habitat_repo.get_habitats_by_dinosaurio(database, dinosaurio.id)
    
    # Obtener comentarios (pasar usuario_id para cargar votos del usuario)
    comentarios = comentario_repo.get_by_dinosaurio(database, dinosaurio_id, usuario.get("id"))
    
    return templates.TemplateResponse("ver_dinosaurio.html", {
        "request": request,
        "usuario": usuario,
        "dinosaurio": dinosaurio,
        "comentarios": comentarios
    })

# =====================================================
# INSERTAR DINOSAURIO (GET - FORMULARIO)
# =====================================================
@router.get("/nuevo/form", response_class=HTMLResponse)
async def form_nuevo_dinosaurio(request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para insertar un nuevo dinosaurio"""
    era_repo = EraRepository()
    region_repo = RegionRepository()
    habitat_repo = HabitatRepository()
    
    eras = era_repo.get_all(database, busqueda=None)
    regiones = region_repo.get_all(database, busqueda=None)
    habitats = habitat_repo.get_all(database, busqueda=None, tipo_ambiente=None)
    
    return templates.TemplateResponse("nuevo_dinosaurio.html", {
        "request": request,
        "usuario": usuario,
        "eras": eras,
        "regiones": regiones,
        "habitats": habitats
    })

# =====================================================
# INSERTAR DINOSAURIO (POST)
# =====================================================
@router.post("/nuevo")
async def crear_dinosaurio(
    request: Request,
    nombre: Annotated[str, Form()],
    descripcion: Annotated[str, Form()] = None,
    tipo: Annotated[str, Form()] = None,
    peso_kg: Annotated[Optional[str], Form()] = None,
    altura_metros: Annotated[Optional[str], Form()] = None,
    longitud_metros: Annotated[Optional[str], Form()] = None,
    dieta: Annotated[str, Form()] = None,
    era_id: Annotated[Optional[str], Form()] = None,
    region_id: Annotated[Optional[str], Form()] = None,
    habitats_seleccionados: Annotated[list[int], Form()] = None,
    imagen: Optional[UploadFile] = File(None),
    usuario: dict = Depends(require_auth)
):
    """Crea un nuevo dinosaurio"""
    try:
        dino_repo = DinosaurioRepository()
        
        # Manejar subida de imagen
        imagen_path = None
        if imagen and imagen.filename:
            # Crear directorio uploads si no existe
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            
            # Guardar archivo con nombre único
            file_extension = Path(imagen.filename).suffix
            file_name = f"dino_{nombre.replace(' ', '_')}_{usuario.get('id')}{file_extension}"
            file_path = upload_dir / file_name
            
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            
            imagen_path = f"/uploads/{file_name}"
        
        dinosaurio = Dinosaurio(
            id=0,
            nombre=nombre,
            descripcion=descripcion,
            tipo=tipo,
            peso_kg=_parse_float(peso_kg),
            altura_metros=_parse_float(altura_metros),
            longitud_metros=_parse_float(longitud_metros),
            dieta=dieta,
            era_id=_parse_int(era_id),
            region_id=_parse_int(region_id),
            creador_id=usuario.get("id"),
            imagen=imagen_path
        )
        
        dino_id = dino_repo.insertar_dinosaurio(database, dinosaurio)
        
        # Agregar habitats si se seleccionaron
        if habitats_seleccionados:
            for habitat_id in habitats_seleccionados:
                dino_repo.agregar_habitat(database, dino_id, int(habitat_id))
        
        return RedirectResponse(url=f"/dinosaurios/{dino_id}", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al crear dinosaurio: {str(e)}"
        })

# =====================================================
# ACTUALIZAR DINOSAURIO (GET - FORMULARIO)
# =====================================================
@router.get("/{dinosaurio_id}/editar", response_class=HTMLResponse)
async def form_editar_dinosaurio(dinosaurio_id: int, request: Request, usuario: dict = Depends(require_auth)):
    """Formulario para editar un dinosaurio"""
    dino_repo = DinosaurioRepository()
    era_repo = EraRepository()
    region_repo = RegionRepository()
    habitat_repo = HabitatRepository()
    
    dinosaurio = dino_repo.get_by_id(database, dinosaurio_id)
    if not dinosaurio:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": "Dinosaurio no encontrado"
        })
    
    eras = era_repo.get_all(database, busqueda=None)
    regiones = region_repo.get_all(database, busqueda=None)
    habitats = habitat_repo.get_all(database, busqueda=None, tipo_ambiente=None)
    
    # Obtener los hábitats actuales del dinosaurio
    habitats_dinosaurio = habitat_repo.get_habitats_by_dinosaurio(database, dinosaurio_id)
    habitats_seleccionados = [h.id for h in habitats_dinosaurio]
    
    return templates.TemplateResponse("editar_dinosaurio.html", {
        "request": request,
        "usuario": usuario,
        "dinosaurio": dinosaurio,
        "eras": eras,
        "regiones": regiones,
        "habitats": habitats,
        "habitats_seleccionados": habitats_seleccionados
    })

# =====================================================
# ACTUALIZAR DINOSAURIO (POST)
# =====================================================
@router.post("/{dinosaurio_id}/editar")
async def actualizar_dinosaurio(
    dinosaurio_id: int,
    request: Request,
    nombre: Annotated[str, Form()],
    descripcion: Annotated[str, Form()] = None,
    tipo: Annotated[str, Form()] = None,
    peso_kg: Annotated[Optional[str], Form()] = None,
    altura_metros: Annotated[Optional[str], Form()] = None,
    longitud_metros: Annotated[Optional[str], Form()] = None,
    dieta: Annotated[str, Form()] = None,
    era_id: Annotated[Optional[str], Form()] = None,
    region_id: Annotated[Optional[str], Form()] = None,
    habitats_seleccionados: Annotated[list[int], Form()] = None,
    imagen: Optional[UploadFile] = File(None),
    usuario: dict = Depends(require_auth)
):
    """Actualiza un dinosaurio existente"""
    try:
        dino_repo = DinosaurioRepository()
        
        # Obtener dinosaurio actual para mantener imagen si no se sube una nueva
        dino_actual = dino_repo.get_by_id(database, dinosaurio_id)
        imagen_path = dino_actual.imagen if dino_actual else None
        
        # Manejar subida de nueva imagen
        if imagen and imagen.filename:
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            
            file_extension = Path(imagen.filename).suffix
            file_name = f"dino_{nombre.replace(' ', '_')}_{dinosaurio_id}{file_extension}"
            file_path = upload_dir / file_name
            
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)
            
            imagen_path = f"/uploads/{file_name}"
        
        dinosaurio = Dinosaurio(
            id=dinosaurio_id,
            nombre=nombre,
            descripcion=descripcion,
            tipo=tipo,
            peso_kg=_parse_float(peso_kg),
            altura_metros=_parse_float(altura_metros),
            longitud_metros=_parse_float(longitud_metros),
            dieta=dieta,
            era_id=_parse_int(era_id),
            region_id=_parse_int(region_id),
            imagen=imagen_path
        )
        
        dino_repo.actualizar_dinosaurio(database, dinosaurio)
        
        # Actualizar habitats
        habitats_actuales = dino_repo.get_habitats(database, dinosaurio_id)
        habitats_nuevos = [int(h) for h in (habitats_seleccionados or [])]
        
        # Eliminar habitats no seleccionados
        for habitat_id in habitats_actuales:
            if habitat_id not in habitats_nuevos:
                dino_repo.quitar_habitat(database, dinosaurio_id, habitat_id)
        
        # Agregar nuevos habitats
        for habitat_id in habitats_nuevos:
            if habitat_id not in habitats_actuales:
                dino_repo.agregar_habitat(database, dinosaurio_id, habitat_id)
        
        return RedirectResponse(url=f"/dinosaurios/{dinosaurio_id}", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al actualizar dinosaurio: {str(e)}"
        })

# =====================================================
# BORRAR DINOSAURIO
# =====================================================
@router.get("/{dinosaurio_id}/borrar", response_class=HTMLResponse)
async def borrar_dinosaurio(dinosaurio_id: int, request: Request, usuario: dict = Depends(require_auth_admin)):
    """Borra un dinosaurio"""
    try:
        dino_repo = DinosaurioRepository()
        dino_repo.borrar_dinosaurio(database, dinosaurio_id)
        return RedirectResponse(url="/dinosaurios/", status_code=303)
    
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "usuario": usuario,
            "mensaje": f"Error al borrar dinosaurio: {str(e)}"
        })
