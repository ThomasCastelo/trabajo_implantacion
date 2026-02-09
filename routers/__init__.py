# Routers package
from . import auth_router
from . import dinosaurios_router
from . import eras_router
from . import regiones_router
from . import habitats_router
from . import usuarios_router

__all__ = [
    'auth_router',
    'dinosaurios_router',
    'eras_router',
    'regiones_router',
    'habitats_router',
    'usuarios_router'
]