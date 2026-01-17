from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(
    title="API app",
    swagger_ui_parameters={"persistAuthorization": True}
)

from api.routers.test import router as test_router
from api.routers.user import router as user_router
from api.routers.artworks import router as artworks_router
from api.routers.listing import router as listing_router
from api.routers.order import router as order_router

app.include_router(test_router)
app.include_router(user_router)
app.include_router(artworks_router)
app.include_router(listing_router)
app.include_router(order_router)