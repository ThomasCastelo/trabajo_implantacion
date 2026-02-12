from typing import List, Optional
from domain.model.Region import Region


class RegionRepository:

    def get_all(self, db, busqueda: Optional[str] = None, continente: Optional[str] = None) -> List[Region]:
        """Obtiene todas las regiones con filtros opcionales"""
        cursor = db.cursor()
        
        query = "SELECT id, nombre, pais, continente, descripcion, imagen FROM regiones WHERE 1=1"
        params = []
        
        if busqueda:
            query += " AND (nombre LIKE %s OR pais LIKE %s OR descripcion LIKE %s)"
            params.extend([f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"])
        
        if continente:
            query += " AND continente = %s"
            params.append(continente)
        
        query += " ORDER BY nombre"
        
        cursor.execute(query, params)
        regiones_en_db = cursor.fetchall()
        regiones: List[Region] = list()
        for region in regiones_en_db:
            region_obj = Region(region[0], region[1], region[2], region[3], region[4], region[5])
            regiones.append(region_obj)
        cursor.close()
        return regiones

    def get_by_id(self, db, id: int) -> Region:
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, pais, continente, descripcion, imagen FROM regiones WHERE id = %s", (id,))
        region_db = cursor.fetchone()
        cursor.close()
        if region_db:
            return Region(region_db[0], region_db[1], region_db[2], region_db[3], region_db[4], region_db[5])
        return None

    def insertar_region(self, db, region: Region) -> None:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO regiones (nombre, pais, continente, descripcion, imagen) VALUES (%s, %s, %s, %s, %s)",
            (region.nombre, region.pais, region.continente, region.descripcion, region.imagen)
        )
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Insert no rows affected")
        cursor.close()

    def actualizar_region(self, db, region: Region) -> None:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE regiones SET nombre = %s, pais = %s, continente = %s, descripcion = %s, imagen = %s WHERE id = %s",
            (region.nombre, region.pais, region.continente, region.descripcion, region.imagen, region.id)
        )
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Update affected no rows")
        cursor.close()

    def borrar_region(self, db, id: int) -> None:
        cursor = db.cursor()
        cursor.execute("DELETE FROM regiones WHERE id = %s", (id,))
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Delete affected no rows")
        cursor.close()
