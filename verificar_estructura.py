#!/usr/bin/env python
"""
Script de verificación de la estructura del proyecto
"""

import os
from pathlib import Path

def verificar_estructura():
    """Verifica que todos los archivos necesarios existan"""
    
    base_path = Path(__file__).parent
    
    # Archivos y directorios requeridos
    requeridos = {
        'directorios': [
            'data',
            'domain',
            'domain/model',
            'routers',
            'template',
            'sql',
            'static',
            'utils'
        ],
        'modelos': [
            'domain/model/Dinosaurio.py',
            'domain/model/Usuario.py',
            'domain/model/Era.py',
            'domain/model/Region.py',
            'domain/model/Habitat.py'
        ],
        'repositorios': [
            'data/dinosaurio_repository.py',
            'data/usuario_repository.py',
            'data/era_repository.py',
            'data/region_repository.py',
            'data/habitat_repository.py'
        ],
        'routers': [
            'routers/auth_router.py',
            'routers/dinosaurios_router.py',
            'routers/eras_router.py',
            'routers/regiones_router.py',
            'routers/habitats_router.py'
        ],
        'plantillas': [
            'template/base.html',
            'template/dinosaurios.html',
            'template/ver_dinosaurio.html',
            'template/nuevo_dinosaurio.html',
            'template/editar_dinosaurio.html',
            'template/eras.html',
            'template/nueva_era.html',
            'template/editar_era.html',
            'template/regiones.html',
            'template/nueva_region.html',
            'template/editar_region.html',
            'template/habitats.html',
            'template/nuevo_habitat.html',
            'template/editar_habitat.html'
        ],
        'sql': [
            'sql/create_complete_database.sql'
        ],
        'principales': [
            'main.py',
            'requirements.txt',
            'run_migrations.py',
            'seed_dinosaurios.py'
        ]
    }
    
    print("🦖 Verificando estructura del proyecto...\n")
    
    todos_ok = True
    
    # Verificar directorios
    print("📁 Verificando directorios:")
    for dir_name in requeridos['directorios']:
        dir_path = base_path / dir_name
        status = "✅" if dir_path.exists() else "❌"
        print(f"  {status} {dir_name}")
        if not dir_path.exists():
            todos_ok = False
    
    # Verificar archivos por categoría
    categorias = ['modelos', 'repositorios', 'routers', 'plantillas', 'sql', 'principales']
    
    for categoria in categorias:
        print(f"\n📄 Verificando {categoria}:")
        for archivo in requeridos[categoria]:
            file_path = base_path / archivo
            status = "✅" if file_path.exists() else "❌"
            print(f"  {status} {archivo}")
            if not file_path.exists():
                todos_ok = False
    
    print("\n" + "="*50)
    if todos_ok:
        print("✅ ¡TODAS LAS VERIFICACIONES PASARON!")
        print("\nSiguientes pasos:")
        print("1. Ejecuta: python run_migrations.py")
        print("2. Opcionalmente: python seed_dinosaurios.py")
        print("3. Ejecuta: python main.py")
        print("4. Accede a: http://localhost:8000")
    else:
        print("❌ FALTAN ARCHIVOS O DIRECTORIOS")
        print("Por favor verifica los archivos marcados con ❌")
    print("="*50)
    
    return todos_ok


if __name__ == "__main__":
    verificar_estructura()
