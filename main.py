from fastapi import FastAPI
from core.config import config
from api import routes
from db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Session API",
    description="Сервіс для ведення чат-сесій з OpenAI"
)

app.include_router(routes.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Service is running"}
