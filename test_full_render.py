#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:\\implantacion\\fastapi_plantillascomunes')

from jinja2 import Environment, FileSystemLoader
from data.dinosaurio_repository import DinosaurioRepository
from data.era_repository import EraRepository
from data.region_repository import RegionRepository
from data.habitat_repository import HabitatRepository
from data.database import database

try:
    print("=" * 60)
    print("PRUEBA: Renderizar template de dinosaurios")
    print("=" * 60)
    
    # Simular exactamente lo que hace el router
    dino_repo = DinosaurioRepository()
    era_repo = EraRepository()
    region_repo = RegionRepository()
    habitat_repo = HabitatRepository()
    
    print("\n1. Obteniendo dinosaurios...")
    dinosaurios = dino_repo.get_all(database, busqueda=None, era_id=None, region_id=None, dieta=None)
    print(f"   ✅ {len(dinosaurios)} dinosaurios encontrados")
    
    print("\n2. Enriqueciendo dinosaurios...")
    for dino in dinosaurios:
        if dino.era_id:
            dino.era = era_repo.get_by_id(database, dino.era_id)
        if dino.region_id:
            dino.region = region_repo.get_by_id(database, dino.region_id)
        dino.habitats = habitat_repo.get_habitats_by_dinosaurio(database, dino.id)
    print(f"   ✅ Enriquecimiento completado")
    
    print("\n3. Obteniendo eras y regiones...")
    todas_eras = era_repo.get_all(database)
    todas_regiones = region_repo.get_all(database)
    print(f"   ✅ {len(todas_eras)} eras y {len(todas_regiones)} regiones")
    
    print("\n4. Renderizando template...")
    env = Environment(loader=FileSystemLoader('template'))
    template = env.get_template('dinosaurios.html')
    
    context = {
        "request": type('Request', (), {'url': 'http://localhost/dinosaurios/'})(),
        "usuario": {"id": 1, "username": "admin", "rol": "admin"},
        "dinosaurios": dinosaurios,
        "todas_eras": todas_eras,
        "todas_regiones": todas_regiones,
        "filtros": {
            "busqueda": "",
            "era_id": None,
            "region_id": None,
            "dieta": ""
        }
    }
    
    html = template.render(context)
    print(f"   ✅ Template renderizado exitosamente")
    print(f"   ✅ Largo del HTML: {len(html)} caracteres")
    
    print("\n" + "=" * 60)
    print("✅ TODO FUNCIONÓ CORRECTAMENTE")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    print("\nTraceback completo:")
    traceback.print_exc()
