class Region:
    def __init__(self, id: int, nombre: str, pais: str = None, continente: str = None, 
                 descripcion: str = None, imagen: str = None):
        self.id = id
        self.nombre = nombre
        self.pais = pais
        self.continente = continente
        self.descripcion = descripcion
        self.imagen = imagen
