from fastapi import FastAPI
from profiles import router as profiles_router

app = FastAPI()

# Include the user profiles router
def setup_routers(app: FastAPI):
    app.include_router(profiles_router, prefix="/profiles", tags=["profiles"])

setup_routers(app)
