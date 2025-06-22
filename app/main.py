from fastapi import FastAPI
from app.routes import router
from app.config import configure_logging

configure_logging()

app = FastAPI(title="AI Web Navigator for Blind Users")
app.include_router(router)

def create_app():
    app = FastAPI(title="AI Web Navigator for Blind Users")
    configure_logging()
    app.include_router(router)
    return app