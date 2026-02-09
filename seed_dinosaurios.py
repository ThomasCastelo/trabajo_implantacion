"""
Script para agregar datos de prueba realistas de dinosaurios
"""
import mysql.connector
from data.database import database
from data.dinosaurio_repository import DinosaurioRepository
from domain.model.Dinosaurio import Dinosaurio

def agregar_datos_prueba():
    """Agrega dinosaurios de prueba a la base de datos"""
    
    dino_repo = DinosaurioRepository()
    
    dinosaurios = [
        Dinosaurio(
            id=0,
            nombre="Tyrannosaurus rex",
            descripcion="El rey de los dinosaurios. Uno de los mayores depredadores terrestres que jamás haya existido.",
            tipo="Saurisquia",
            peso_kg=9000,
            altura_metros=5.6,
            longitud_metros=12.3,
            dieta="Carnívoro",
            era_id=3,  # Cretácico
            region_id=1,  # Montana
            creador_id=1
        ),
        Dinosaurio(
            id=0,
            nombre="Brachiosaurus",
            descripcion="Uno de los dinosaurios más grandes que jamás existió. Un gigante herbívoro de cuello largo.",
            tipo="Saurischia",
            peso_kg=56000,
            altura_metros=13,
            longitud_metros=25,
            dieta="Herbívoro",
            era_id=2,  # Jurásico
            region_id=1,  # Montana
            creador_id=1
        ),
        Dinosaurio(
            id=0,
            nombre="Triceratops",
            descripcion="Dinosaurio herbívoro con tres cuernos distintivos. Fue uno de los últimos dinosaurios antes de la extinción.",
            tipo="Ornithischia",
            peso_kg=6000,
            altura_metros=3,
            longitud_metros=9,
            dieta="Herbívoro",
            era_id=3,  # Cretácico
            region_id=4,  # Alberta
            creador_id=1
        ),
        Dinosaurio(
            id=0,
            nombre="Velociraptor",
            descripcion="Pequeño pero inteligente depredador. Cazaba en manadas coordinadas.",
            tipo="Saurischia",
            peso_kg=15,
            altura_metros=0.5,
            longitud_metros=1.8,
            dieta="Carnívoro",
            era_id=3,  # Cretácico
            region_id=2,  # Liaoning
            creador_id=1
        ),
        Dinosaurio(
            id=0,
            nombre="Stegosaurus",
            descripcion="Herbívoro de tamaño mediano con placas óseas en el lomo. Vivió en el Jurásico.",
            tipo="Ornithischia",
            peso_kg=2000,
            altura_metros=4,
            longitud_metros=9,
            dieta="Herbívoro",
            era_id=2,  # Jurásico
            region_id=1,  # Montana
            creador_id=1
        ),
        Dinosaurio(
            id=0,
            nombre="Argentinosaurus",
            descripcion="Posiblemente el dinosaurio más grande que jamás existió. Descubierto en Argentina.",
            tipo="Saurischia",
            peso_kg=100000,
            altura_metros=18,
            longitud_metros=35,
            dieta="Herbívoro",
            era_id=3,  # Cretácico
            region_id=3,  # Región de Chubut
            creador_id=1
        ),
    ]
    
    try:
        for dino in dinosaurios:
            try:
                dino_repo.insertar_dinosaurio(database, dino)
                print(f"✅ Agregado: {dino.nombre}")
            except Exception as e:
                print(f"⚠️  {dino.nombre} ya existe o error: {str(e)}")
        
        print("\n✅ Datos de prueba insertados correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error al agregar datos de prueba: {str(e)}")
        return False


if __name__ == "__main__":
    print("🦖 Insertando dinosaurios de prueba...")
    agregar_datos_prueba()
