#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:\\implantacion\\fastapi_plantillascomunes')

# Simulando una petición
from data.database import database
from data.dinosaurio_repository import DinosaurioRepository
from data.era_repository import EraRepository
from data.region_repository import RegionRepository
from data.habitat_repository import HabitatRepository

try:
    dino_repo = DinosaurioRepository()
    era_repo = EraRepository()
    region_repo = RegionRepository()
    habitat_repo = HabitatRepository()
    
    # Obtener dinosaurios con filtros
    print("Obteniendo dinosaurios...")
    dinosaurios = dino_repo.get_all(database, busqueda=None, era_id=None, region_id=None, dieta=None)
    print(f"✅ {len(dinosaurios)} dinosaurios encontrados")
    
    # Enriquecer
    print("Enriqueciendo dinosaurios...")
    for dino in dinosaurios:
        if dino.era_id:
            dino.era = era_repo.get_by_id(database, dino.era_id)
        if dino.region_id:
            dino.region = region_repo.get_by_id(database, dino.region_id)
        dino.habitats = habitat_repo.get_habitats_by_dinosaurio(database, dino.id)
    print("✅ Enriquecimiento completado")
    
    # Obtener todas las eras y regiones para los filtros
    print("Obteniendo eras y regiones...")
    todas_eras = era_repo.get_all(database)
    todas_regiones = region_repo.get_all(database)
    print(f"✅ {len(todas_eras)} eras y {len(todas_regiones)} regiones")
    
    print("\n✅ TODO FUNCIONA CORRECTAMENTE")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
