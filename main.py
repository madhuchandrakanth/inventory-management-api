# 1. Import the FastAPI class from the fastapi package. 
# This class provides all the core functionality for routing and data validation.
from fastapi import FastAPI

# import CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Import controller logic
from controller.dashboard_controller import fetch_dashboard_data

# 2. Create an instance of the FastAPI application.
# The 'app' variable is the actual application object that handles incoming web requests.
app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://127.0.0.1:5173", 
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define a "Route" or "Endpoint". 
# The @app.get("/") decorator tells FastAPI that any HTTP GET requests sent to the 
# root URL (like http://localhost:8000/) should be handled by the function below it.
@app.get("/")
def read_root():
    # FastAPI automatically converts Python dictionaries into JSON format 
    # when returning this response back to the client's browser or app.
    return "welcome to the inventory management app!"


# Dashboard API Route
@app.get("/dashboard")
def get_dashboard_data():
    """Route purely responsible for handling the dashboard request and delegating work."""
    return fetch_dashboard_data()

# 4. Start the development server.
# This block ensures the server only starts if you run this script directly 
# (e.g., by typing 'python main.py' in the terminal).
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run starts the web server which listens for traffic. 
    # We use "127.0.0.1" (localhost) so it runs safely on your local machine, on port 8000.
    uvicorn.run(app, host="127.0.0.1", port=8000)