from fastapi import FastAPI
from api.routes import analysis_routes, data_routes

app = FastAPI()

app.include_router(analysis_routes.router)
app.include_router(data_routes.router)