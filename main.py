from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from db.base import Base
from api.routes import auth, products
from contextlib import asynccontextmanager

# Inicializa la base de datos
def create_tables():
    Base.metadata.create_all(bind=engine)

# Lifespan moderno
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al arrancar
    create_tables()
    yield
    # Código que se ejecuta al cerrar (si quieres)
    # Por ejemplo: cerrar conexiones, limpiar recursos, etc.

# Instancia de la app
app = FastAPI(title="Inventory Management API", debug=True, lifespan=lifespan)

# Exponer la carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS (útil si el frontend está en otro dominio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye las rutas
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
