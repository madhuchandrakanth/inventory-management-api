from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.dashboard_routes import dashboard_router
from routes.users_routes import user_router
from routes.shops_routes import shop_router
from database import engine, Base

# Create the FastAPI application
app = FastAPI(
    title="Inventory Management API",
    description="API for managing inventory, users, and shops",
    version="1.0.0",
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}


# Register routers
app.include_router(dashboard_router)
app.include_router(user_router)
app.include_router(shop_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)