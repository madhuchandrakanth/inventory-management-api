from fastapi import APIRouter
from controller.dashboard_controller import fetch_dashboard_data

# Create a dedicated router for the Dashboard
dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@dashboard_router.get("/")
def get_dashboard_data():
    """
    Handle GET requests for /dashboard.
    This routes cleanly through the APIRouter.
    TODO: Integrate your dashboard_service logic here!
    """
    return fetch_dashboard_data()
    