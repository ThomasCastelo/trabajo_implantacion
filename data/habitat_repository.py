from typing import List, Optional
from domain.model.Habitat import Habitat


class HabitatRepository:

    def get_all(self, db, busqueda: Optional[str] = None, tipo_ambiente: Optional[str] = None) -> List[Habitat]:
        """Obtiene todos los hábitats con filtros opcionales"""
        cursor = db.cursor()
        
        query = "SELECT id, nombre, tipo_ambiente, descripcion, imagen FROM habitats WHERE 1=1"
        params = []
        
        if busqueda:
            query += " AND (nombre LIKE %s OR descripcion LIKE %s)"
            params.extend([f"%{busqueda}%", f"%{busqueda}%"])
        
        if tipo_ambiente:
            query += " AND tipo_ambiente = %s"
            params.append(tipo_ambiente)
        
        query += " ORDER BY nombre"
        
        cursor.execute(query, params)
        habitats_en_db = cursor.fetchall()
        habitats: List[Habitat] = list()
        for habitat in habitats_en_db:
            habitat_obj = Habitat(habitat[0], habitat[1], habitat[2], habitat[3], habitat[4])
            habitats.append(habitat_obj)
        cursor.close()
        return habitats

    def get_by_id(self, db, id: int) -> Habitat:
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, tipo_ambiente, descripcion, imagen FROM habitats WHERE id = %s", (id,))
        habitat_db = cursor.fetchone()
        cursor.close()
        if habitat_db:
            return Habitat(habitat_db[0], habitat_db[1], habitat_db[2], habitat_db[3], habitat_db[4])
        return None

    def insertar_habitat(self, db, habitat: Habitat) -> None:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO habitats (nombre, tipo_ambiente, descripcion, imagen) VALUES (%s, %s, %s, %s)",
            (habitat.nombre, habitat.tipo_ambiente, habitat.descripcion, habitat.imagen)
        )
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Insert no rows affected")
        cursor.close()

    def actualizar_habitat(self, db, habitat: Habitat) -> None:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE habitats SET nombre = %s, tipo_ambiente = %s, descripcion = %s, imagen = %s WHERE id = %s",
            (habitat.nombre, habitat.tipo_ambiente, habitat.descripcion, habitat.imagen, habitat.id)
        )
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Update affected no rows")
        cursor.close()

    def borrar_habitat(self, db, id: int) -> None:
        cursor = db.cursor()
        cursor.execute("DELETE FROM habitats WHERE id = %s", (id,))
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Delete affected no rows")
        cursor.close()

    def get_habitats_by_dinosaurio(self, db, dinosaurio_id: int) -> List[Habitat]:
        """Obtiene todos los habitats asociados a un dinosaurio"""
        cursor = db.cursor()
        cursor.execute("""
            SELECT h.id, h.nombre, h.tipo_ambiente, h.descripcion 
            FROM habitats h
            JOIN dinosaurios_habitats dh ON h.id = dh.habitat_id
            WHERE dh.dinosaurio_id = %s
            ORDER BY h.nombre
        """, (dinosaurio_id,))
        habitats_en_db = cursor.fetchall()
        habitats: List[Habitat] = list()
        for habitat in habitats_en_db:
            habitat_obj = Habitat(habitat[0], habitat[1], habitat[2], habitat[3])
            habitats.append(habitat_obj)
        cursor.close()
        return habitats

