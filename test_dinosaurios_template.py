#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:\\implantacion\\fastapi_plantillascomunes')

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

try:
    env = Environment(loader=FileSystemLoader('template'))
    template = env.get_template('dinosaurios.html')
    print("✅ Template dinosaurios.html es válido")
    
    # Intentar renderizarlo con datos de prueba
    result = template.render(
        request={},
        usuario={'id': 1, 'username': 'test', 'rol': 'admin'},
        dinosaurios=[],
        todas_eras=[],
        todas_regiones=[],
        filtros={'busqueda': '', 'era_id': None, 'region_id': None, 'dieta': ''}
    )
    print("✅ Template renderiza correctamente")
    
except TemplateSyntaxError as e:
    print(f"❌ Error de sintaxis en el template:")
    print(f"  Línea {e.lineno}: {e.message}")
except Exception as e:
    print(f"❌ Error al renderizar: {e}")
    import traceback
    traceback.print_exc()
