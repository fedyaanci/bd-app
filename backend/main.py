from fastapi  import FastAPI
from database import engine, Base
from routers import auth

app = FastAPI(title="PictureMarket")

app.include_router(auth.router, prefix="/api")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)