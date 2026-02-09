class Habitat:
    def __init__(self, id: int, nombre: str, tipo_ambiente: str = None, descripcion: str = None,
                 imagen: str = None):
        self.id = id
        self.nombre = nombre
        self.tipo_ambiente = tipo_ambiente
        self.descripcion = descripcion
        self.imagen = imagen
