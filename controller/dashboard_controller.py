import importlib.util
import os
from fastapi import HTTPException

def fetch_dashboard_data():
    """
    Fetches the dashboard data from the mock file.
    Returns the data or raises an HTTPException based on the scenario.
    """
    try:
        # Base dir is the parent of 'controller' directory
        base_dir = os.path.dirname(os.path.dirname(__file__))
        mock_path = os.path.join(base_dir, "mocks", "dashboard-mock.py")
        
        spec = importlib.util.spec_from_file_location("dashboard_mock", mock_path)
        if spec is not None:
            loader = spec.loader
            if loader is not None:
                dashboard_mock = importlib.util.module_from_spec(spec)
                loader.exec_module(dashboard_mock)
                
                if hasattr(dashboard_mock, "dashboard_mock_data"):
                    return dashboard_mock.dashboard_mock_data
        
        # If spec/loader failed or data not found
        raise HTTPException(status_code=404, detail="Mock data file or variables not found")
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        # Wrap any other internal server errors cleanly
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
