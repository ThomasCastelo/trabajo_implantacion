from typing import List, Optional
from domain.model.Dinosaurio import Dinosaurio


class DinosaurioRepository:

    def get_all(self, db, busqueda: Optional[str] = None, era_id: Optional[int] = None, 
                region_id: Optional[int] = None, dieta: Optional[str] = None) -> List[Dinosaurio]:
        """Obtiene todos los dinosaurios con filtros opcionales"""
        cursor = db.cursor()
        
        # Construir query dinámicamente
        query = """
            SELECT id, nombre, descripcion, tipo, peso_kg, altura_metros, longitud_metros, 
                   dieta, era_id, region_id, creador_id, imagen 
            FROM dinosaurios 
            WHERE 1=1
        """
        params = []
        
        # Filtro de búsqueda por nombre o descripción
        if busqueda:
            query += " AND (nombre LIKE %s OR descripcion LIKE %s)"
            params.extend([f"%{busqueda}%", f"%{busqueda}%"])
        
        # Filtro por era
        if era_id:
            query += " AND era_id = %s"
            params.append(era_id)
        
        # Filtro por región
        if region_id:
            query += " AND region_id = %s"
            params.append(region_id)
        
        # Filtro por dieta
        if dieta:
            query += " AND dieta = %s"
            params.append(dieta)
        
        query += " ORDER BY nombre"
        
        cursor.execute(query, params)
        dinosaurios_en_db = cursor.fetchall()
        dinosaurios: List[Dinosaurio] = list()
        for dino in dinosaurios_en_db:
            dinosaurio = Dinosaurio(dino[0], dino[1], dino[2], dino[3], dino[4], dino[5], 
                                   dino[6], dino[7], dino[8], dino[9], dino[10], dino[11])
            dinosaurios.append(dinosaurio)
        cursor.close()
        return dinosaurios

    def get_by_id(self, db, id: int) -> Dinosaurio:
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, tipo, peso_kg, altura_metros, longitud_metros, 
                   dieta, era_id, region_id, creador_id, imagen 
            FROM dinosaurios 
            WHERE id = %s
        """, (id,))
        dino = cursor.fetchone()
        cursor.close()
        if dino:
            return Dinosaurio(dino[0], dino[1], dino[2], dino[3], dino[4], dino[5], 
                            dino[6], dino[7], dino[8], dino[9], dino[10], dino[11])
        return None

    def insertar_dinosaurio(self, db, dinosaurio: Dinosaurio) -> int:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO dinosaurios (nombre, descripcion, tipo, peso_kg, altura_metros, 
                                    longitud_metros, dieta, era_id, region_id, creador_id, imagen) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (dinosaurio.nombre, dinosaurio.descripcion, dinosaurio.tipo, dinosaurio.peso_kg,
              dinosaurio.altura_metros, dinosaurio.longitud_metros, dinosaurio.dieta,
              dinosaurio.era_id, dinosaurio.region_id, dinosaurio.creador_id, dinosaurio.imagen))
        db.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Insert no rows affected")
        
        nuevo_id = cursor.lastrowid
        cursor.close()
        return nuevo_id

    def actualizar_dinosaurio(self, db, dinosaurio: Dinosaurio) -> None:
        cursor = db.cursor()
        cursor.execute("""
            UPDATE dinosaurios 
            SET nombre = %s, descripcion = %s, tipo = %s, peso_kg = %s, altura_metros = %s,
                longitud_metros = %s, dieta = %s, era_id = %s, region_id = %s, imagen = %s
            WHERE id = %s
        """, (dinosaurio.nombre, dinosaurio.descripcion, dinosaurio.tipo, dinosaurio.peso_kg,
              dinosaurio.altura_metros, dinosaurio.longitud_metros, dinosaurio.dieta,
              dinosaurio.era_id, dinosaurio.region_id, dinosaurio.imagen, dinosaurio.id))
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Update affected no rows")
        cursor.close()

    def borrar_dinosaurio(self, db, id: int) -> None:
        cursor = db.cursor()
        # Primero borramos las relaciones N-M
        cursor.execute("DELETE FROM dinosaurios_habitats WHERE dinosaurio_id = %s", (id,))
        # Luego borramos el dinosaurio
        cursor.execute("DELETE FROM dinosaurios WHERE id = %s", (id,))
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Delete affected no rows")
        cursor.close()

    def agregar_habitat(self, db, dinosaurio_id: int, habitat_id: int) -> None:
        """Agrega un habitat a un dinosaurio (relación N-M)"""
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO dinosaurios_habitats (dinosaurio_id, habitat_id) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE dinosaurio_id = dinosaurio_id
        """, (dinosaurio_id, habitat_id))
        db.commit()
        cursor.close()

    def quitar_habitat(self, db, dinosaurio_id: int, habitat_id: int) -> None:
        """Quita un habitat de un dinosaurio"""
        cursor = db.cursor()
        cursor.execute("""
            DELETE FROM dinosaurios_habitats 
            WHERE dinosaurio_id = %s AND habitat_id = %s
        """, (dinosaurio_id, habitat_id))
        db.commit()
        cursor.close()

    def get_habitats(self, db, dinosaurio_id: int) -> List[int]:
        """Obtiene los IDs de habitats asociados a un dinosaurio"""
        cursor = db.cursor()
        cursor.execute("""
            SELECT habitat_id FROM dinosaurios_habitats 
            WHERE dinosaurio_id = %s
        """, (dinosaurio_id,))
        habitats = cursor.fetchall()
        cursor.close()
        return [h[0] for h in habitats] if habitats else []

