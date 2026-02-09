#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:\\implantacion\\fastapi_plantillascomunes')

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

try:
    env = Environment(loader=FileSystemLoader('template'))
    template = env.get_template('ver_dinosaurio.html')
    print("✅ Template ver_dinosaurio.html es válido")
except TemplateSyntaxError as e:
    print(f"❌ Error de sintaxis en el template:")
    print(f"  Línea {e.lineno}: {e.message}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
