from fastapi import FastAPI
from .usuarios.router import router as router_usuarios
from .sesiones.router import router as router_sesiones


app = FastAPI()
app.include_router(router_usuarios)
app.include_router(router_sesiones)
