class Era:
    def __init__(self, id: int, nombre: str, periodo_inicio: int = None, periodo_fin: int = None, 
                 descripcion: str = None, imagen: str = None):
        self.id = id
        self.nombre = nombre
        self.periodo_inicio = periodo_inicio
        self.periodo_fin = periodo_fin
        self.descripcion = descripcion
        self.imagen = imagen
