class Comentario:
    def __init__(self, id: int, dinosaurio_id: int, usuario_id: int, contenido: str,
                 fecha_creacion: str = None, comentario_padre_id: int = None,
                 usuario_nombre: str = None, fecha_modificacion: str = None,
                 votos_positivos: int = 0, votos_negativos: int = 0, voto_usuario: str = None):
        self.id = id
        self.dinosaurio_id = dinosaurio_id
        self.usuario_id = usuario_id
        self.contenido = contenido
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion  # Fecha de última edición
        self.comentario_padre_id = comentario_padre_id
        self.usuario_nombre = usuario_nombre  # Para mostrar el nombre del usuario
        self.votos_positivos = votos_positivos  # Conteo de votos positivos
        self.votos_negativos = votos_negativos  # Conteo de votos negativos
        self.voto_usuario = voto_usuario  # Tipo de voto del usuario actual ('positivo', 'negativo', None)
        self.respuestas = []  # Lista de comentarios hijos
