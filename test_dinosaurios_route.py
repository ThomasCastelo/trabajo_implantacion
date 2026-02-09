import sys
sys.path.insert(0, 'c:\\implantacion\\fastapi_plantillascomunes')

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Intentar acceder a la ruta de dinosaurios
try:
    response = client.get("/dinosaurios/")
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text[:500]}")
    else:
        print("✅ La ruta funciona correctamente")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
