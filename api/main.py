from fastapi import FastAPI

from api import models, url_shortner, url_analytics
from api.database import engine

# Map all classes (tables) to database and create any missing tables
models.Base.metadata.create_all(engine)

# Main App
app = FastAPI()


# Root response
@app.get("/")
def read_root():
    return {"message": "Welcome to user api. Please read /docs"}


# Add routers
app.include_router(url_shortner.router, prefix="/api")
app.include_router(url_analytics.router, prefix="/api")
