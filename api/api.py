from fastapi import FastAPI 
from api.routers.test import router as test_router
from api.routers.user import router as getPerson_router
app = FastAPI(title="API app")

app.include_router(test_router)
app.include_router(getPerson_router)