class Dinosaurio:
    def __init__(self, id: int, nombre: str, descripcion: str = None, tipo: str = None, 
                 peso_kg: float = None, altura_metros: float = None, longitud_metros: float = None,
                 dieta: str = None, era_id: int = None, region_id: int = None, creador_id: int = None,
                 imagen: str = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo = tipo
        self.peso_kg = peso_kg
        self.altura_metros = altura_metros
        self.longitud_metros = longitud_metros
        self.dieta = dieta
        self.era_id = era_id
        self.region_id = region_id
        self.creador_id = creador_id
        self.imagen = imagen
        self.habitats = []  # Lista de habitats asociados
