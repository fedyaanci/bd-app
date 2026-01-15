from fastapi import FastAPI 
from api.routers.test import router as test_router
from api.routers.user import router as user_router
from api.routers.artworks import router as artworks_router
from api.routers.listing import router as listing_router


app = FastAPI(title="API app")

app.include_router(test_router)
app.include_router(user_router)
app.include_router(artworks_router)
app.include_router(listing_router)

