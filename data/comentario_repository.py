from typing import List
from domain.model.Comentario import Comentario


class ComentarioRepository:

    def get_by_dinosaurio(self, db, dinosaurio_id: int, usuario_id: int = None) -> List[Comentario]:
        """Obtiene todos los comentarios de un dinosaurio (solo padres, sin respuestas)"""
        cursor = db.cursor()
        cursor.execute("""
            SELECT c.id, c.dinosaurio_id, c.usuario_id, c.contenido, c.fecha_creacion, 
                   c.comentario_padre_id, u.username, c.fecha_modificacion
            FROM comentarios c
            JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.dinosaurio_id = %s AND c.comentario_padre_id IS NULL
            ORDER BY c.fecha_creacion DESC
        """, (dinosaurio_id,))
        comentarios_db = cursor.fetchall()
        comentarios: List[Comentario] = []
        for com in comentarios_db:
            comentario = Comentario(
                id=com[0],
                dinosaurio_id=com[1],
                usuario_id=com[2],
                contenido=com[3],
                fecha_creacion=str(com[4]) if com[4] else None,
                comentario_padre_id=com[5],
                usuario_nombre=com[6],
                fecha_modificacion=str(com[7]) if com[7] else None
            )
            # Cargar votos
            votos = self.get_votos(db, comentario.id, usuario_id)
            comentario.votos_positivos = votos['positivos']
            comentario.votos_negativos = votos['negativos']
            comentario.voto_usuario = votos['voto_usuario']
            
            # Cargar respuestas
            comentario.respuestas = self.get_respuestas(db, comentario.id, usuario_id)
            comentarios.append(comentario)
        cursor.close()
        return comentarios

    def get_respuestas(self, db, comentario_padre_id: int, usuario_id: int = None) -> List[Comentario]:
        """Obtiene las respuestas de un comentario"""
        cursor = db.cursor()
        cursor.execute("""
            SELECT c.id, c.dinosaurio_id, c.usuario_id, c.contenido, c.fecha_creacion, 
                   c.comentario_padre_id, u.username, c.fecha_modificacion
            FROM comentarios c
            JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.comentario_padre_id = %s
            ORDER BY c.fecha_creacion ASC
        """, (comentario_padre_id,))
        respuestas_db = cursor.fetchall()
        respuestas: List[Comentario] = []
        for resp in respuestas_db:
            respuesta = Comentario(
                id=resp[0],
                dinosaurio_id=resp[1],
                usuario_id=resp[2],
                contenido=resp[3],
                fecha_creacion=str(resp[4]) if resp[4] else None,
                comentario_padre_id=resp[5],
                usuario_nombre=resp[6],
                fecha_modificacion=str(resp[7]) if resp[7] else None
            )
            # Cargar votos
            votos = self.get_votos(db, respuesta.id, usuario_id)
            respuesta.votos_positivos = votos['positivos']
            respuesta.votos_negativos = votos['negativos']
            respuesta.voto_usuario = votos['voto_usuario']
            
            respuestas.append(respuesta)
        cursor.close()
        return respuestas

    def insertar_comentario(self, db, comentario: Comentario) -> int:
        """Inserta un nuevo comentario"""
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO comentarios (dinosaurio_id, usuario_id, contenido, comentario_padre_id)
            VALUES (%s, %s, %s, %s)
        """, (comentario.dinosaurio_id, comentario.usuario_id, comentario.contenido, comentario.comentario_padre_id))
        db.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        return nuevo_id

    def actualizar_comentario(self, db, id: int, contenido: str) -> None:
        """Actualiza el contenido de un comentario"""
        cursor = db.cursor()
        cursor.execute("""
            UPDATE comentarios 
            SET contenido = %s, fecha_modificacion = NOW()
            WHERE id = %s
        """, (contenido, id))
        db.commit()
        cursor.close()

    def borrar_comentario(self, db, id: int) -> None:
        """Borra un comentario (y sus respuestas por CASCADE)"""
        cursor = db.cursor()
        cursor.execute("DELETE FROM comentarios WHERE id = %s", (id,))
        db.commit()
        cursor.close()

    def contar_comentarios(self, db, dinosaurio_id: int) -> int:
        """Cuenta el total de comentarios (incluyendo respuestas) de un dinosaurio"""
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM comentarios WHERE dinosaurio_id = %s", (dinosaurio_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def get_votos(self, db, comentario_id: int, usuario_id: int = None) -> dict:
        """Obtiene el conteo de votos y el voto del usuario actual"""
        cursor = db.cursor()
        
        # Contar votos positivos y negativos
        cursor.execute("""
            SELECT tipo_voto, COUNT(*) 
            FROM comentario_votos 
            WHERE comentario_id = %s
            GROUP BY tipo_voto
        """, (comentario_id,))
        votos_resultado = cursor.fetchall()
        
        votos_positivos = 0
        votos_negativos = 0
        for tipo, count in votos_resultado:
            if tipo == 'positivo':
                votos_positivos = count
            elif tipo == 'negativo':
                votos_negativos = count
        
        # Obtener el voto del usuario actual si existe
        voto_usuario = None
        if usuario_id:
            cursor.execute("""
                SELECT tipo_voto 
                FROM comentario_votos 
                WHERE comentario_id = %s AND usuario_id = %s
            """, (comentario_id, usuario_id))
            resultado = cursor.fetchone()
            if resultado:
                voto_usuario = resultado[0]
        
        cursor.close()
        return {
            'positivos': votos_positivos,
            'negativos': votos_negativos,
            'voto_usuario': voto_usuario
        }

    def agregar_voto(self, db, comentario_id: int, usuario_id: int, tipo_voto: str) -> None:
        """Agrega o actualiza un voto en un comentario"""
        cursor = db.cursor()
        
        # Verificar si ya existe un voto
        cursor.execute("""
            SELECT id FROM comentario_votos 
            WHERE comentario_id = %s AND usuario_id = %s
        """, (comentario_id, usuario_id))
        resultado = cursor.fetchone()
        
        if resultado:
            # Actualizar voto existente
            cursor.execute("""
                UPDATE comentario_votos 
                SET tipo_voto = %s 
                WHERE comentario_id = %s AND usuario_id = %s
            """, (tipo_voto, comentario_id, usuario_id))
        else:
            # Insertar nuevo voto
            cursor.execute("""
                INSERT INTO comentario_votos (comentario_id, usuario_id, tipo_voto)
                VALUES (%s, %s, %s)
            """, (comentario_id, usuario_id, tipo_voto))
        
        db.commit()
        cursor.close()

    def eliminar_voto(self, db, comentario_id: int, usuario_id: int) -> None:
        """Elimina el voto de un usuario en un comentario"""
        cursor = db.cursor()
        cursor.execute("""
            DELETE FROM comentario_votos 
            WHERE comentario_id = %s AND usuario_id = %s
        """, (comentario_id, usuario_id))
        db.commit()
        cursor.close()
