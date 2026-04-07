# controller/dashboard_controller.py - Controller layer for dashboard endpoints

from fastapi import HTTPException
from mocks.dashboard_mock import dashboard_mock_data


def fetch_dashboard_data():
    """
    Fetches the dashboard data from the mock module.
    Returns the data or raises an HTTPException if unavailable.
    """
    try:
        if dashboard_mock_data:
            return dashboard_mock_data
        raise HTTPException(status_code=404, detail="Mock data not found")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
