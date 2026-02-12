from typing import List, Optional
from domain.model.Era import Era


class EraRepository:

    def get_all(self, db, busqueda: Optional[str] = None) -> List[Era]:
        """Obtiene todas las eras con búsqueda opcional por nombre"""
        cursor = db.cursor()
        
        query = "SELECT id, nombre, periodo_inicio, periodo_fin, descripcion, imagen FROM eras WHERE 1=1"
        params = []
        
        if busqueda:
            query += " AND (nombre LIKE %s OR descripcion LIKE %s)"
            params.extend([f"%{busqueda}%", f"%{busqueda}%"])
        
        query += " ORDER BY periodo_inicio DESC"
        
        cursor.execute(query, params)
        eras_en_db = cursor.fetchall()
        eras: List[Era] = list()
        for era in eras_en_db:
            era_obj = Era(era[0], era[1], era[2], era[3], era[4], era[5])
            eras.append(era_obj)
        cursor.close()
        return eras

    def get_by_id(self, db, id: int) -> Era:
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, periodo_inicio, periodo_fin, descripcion, imagen FROM eras WHERE id = %s", (id,))
        era_db = cursor.fetchone()
        cursor.close()
        if era_db:
            return Era(era_db[0], era_db[1], era_db[2], era_db[3], era_db[4], era_db[5])
        return None

    def insertar_era(self, db, era: Era) -> None:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO eras (nombre, periodo_inicio, periodo_fin, descripcion, imagen) VALUES (%s, %s, %s, %s, %s)",
            (era.nombre, era.periodo_inicio, era.periodo_fin, era.descripcion, era.imagen)
        )
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Insert no rows affected")
        cursor.close()

    def actualizar_era(self, db, era: Era) -> None:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE eras SET nombre = %s, periodo_inicio = %s, periodo_fin = %s, descripcion = %s, imagen = %s WHERE id = %s",
            (era.nombre, era.periodo_inicio, era.periodo_fin, era.descripcion, era.imagen, era.id)
        )
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Update affected no rows")
        cursor.close()

    def borrar_era(self, db, id: int) -> None:
        cursor = db.cursor()
        cursor.execute("DELETE FROM eras WHERE id = %s", (id,))
        db.commit()
        if cursor.rowcount == 0:
            cursor.close()
            raise RuntimeError("Delete affected no rows")
        cursor.close()
