from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_SECRET = "mi-clave-secreta-123"

def verify_api_key(x_api_key: str = Header(default=None)):
    """Verifica si la petición contiene el x-api-key y si es correcto."""
    if not x_api_key or x_api_key != API_KEY_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key

@app.get("/health")
def health_check():
    """Endpoint público que devuelve el estado del servidor."""
    return {"status": "ok"}

@app.get("/api/data")
def get_protected_data(api_key: str = Depends(verify_api_key)):
    """Endpoint protegido (GET) que devuelve un JSON estático[cite: 1]."""
    return {
        "message": "Protected data",
        "course": "Security Exercise",
        "status": "success"
    }

@app.post("/api/data")
def post_protected_data(api_key: str = Depends(verify_api_key)):
    """Endpoint protegido (POST) que devuelve un mensaje de confirmación[cite: 1]."""
    return {"message": "POST received"}