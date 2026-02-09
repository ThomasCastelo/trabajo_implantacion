class Usuario:
    def __init__(self, id: int, username: str, password_hash: str, email: str = None, rol: str = "usuario", activo: bool = True):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.rol = rol  # "usuario" o "admin"
        self.activo = activo
    
    def es_admin(self) -> bool:
        return self.rol == "admin"
